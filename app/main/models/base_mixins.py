from datetime import datetime, date
import logging
import uuid
import re

from flask import url_for, current_app

from .. import db


LOGGER = logging.getLogger(__name__)


class SearchUtils(object):
    def add_to_index(index, model):
        if not current_app.elasticsearch:
            return
        payload = {}
        for field in model.__searchable__:
            payload[field] = getattr(model, field)
        current_app.elasticsearch.index(index=index, id=model.id, body=payload)


    def remove_from_index(index, model):
        if not current_app.elasticsearch:
            return
        current_app.elasticsearch.delete(index=index, id=model.id)


    def query_index(index, query, page, per_page):
        if not current_app.elasticsearch:
            return [], 0
        search = current_app.elasticsearch.search(
            index=index,
            body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
                'from': (page - 1) * per_page, 'size': per_page})
        ids = [int(hit['_id']) for hit in search['hits']['hits']]
        return ids, search['hits']['total']['value']
    

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = SearchUtils.query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                SearchUtils.add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                SearchUtils.add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                SearchUtils.remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            SearchUtils.add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""
    
    update_time = db.Column(db.DateTime(timezone=True))
    create_time = db.Column(db.DateTime(timezone=True))
    public_id = db.Column(db.String(100), unique=True)
    
    def __init__(self):
        """"""
        self.update_time = datetime.now()
        self.create_time = datetime.now()
        self.public_id = str(uuid.uuid4())
        
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        instance.create_time = datetime.now()
        instance.update_time = datetime.now()
        instance.save()
        return instance

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.update_time = datetime.now()
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class FunctionsMixin(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self):
        pass
    
    def get_id(self):
        return str(self.id)
    
    def _is_attriute_key(self, key):
        # FIX ME 
        # This logic is not 100% right, it will not enable the inclusion of hidden attribute
        if "password" in key.lower():
            return False
         
        if key.startswith('__') or key.startswith('_'):
            return False
        
        return True
            
    def json(self):
        json_data = {}
        for key, value in self.__dict__.items():
            if callable(value) or self._is_attriute_key(key) is False:
                continue
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            json_data[key] = value
        # data = dict((key, value) for key, value in self.__dict__.items() if not callable(value) and self._is_attriute_key(key))
        return json_data
    
    @classmethod
    def get_object_by_id(cls, record_id):
        return cls.query.filter_by(id=record_id).first()
    
    @classmethod
    def get_object_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
    
    @classmethod
    def get_object_json_by_id(cls, record_id):
        '''function to get object using the id of the object as parameter'''
        return cls.json(cls.query.filter_by(id=record_id).first())
    
    
    @classmethod
    def get_all_objects(cls):
        '''function to get all objects on the table in our database'''
        return [cls.json(item) for item in cls.query.all()]

    # def to_json(self):
    #     passs
    
    def __str__(self):
        return_value = f"{self.__class__.__name__}"
        """"""
        for item, value in self.__dict__.items():
            if callable(value) is False and self._is_attriute_key(item):
                return_value += f"\n  {item}: {value}"
        return return_value
        

class Model(CRUDMixin, FunctionsMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True
    
    def __init__(self):
        LOGGER.info(f"Creating a new {self.__class__.__name__} object")
        
        super().__init__()
        # CRUDMixin().__init__()
        FunctionsMixin().__init__()
        # self.public_id = str(uuid.uuid4())
        
