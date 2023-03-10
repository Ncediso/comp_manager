from datetime import datetime, timedelta
import logging
from typing import Union
import uuid
from flask_jwt_extended import decode_token

import jwt

from ..models.blacklist import BlacklistToken
from app.main.models.base_mixins import Model
from ..config import key
from ...main import db, flask_bcrypt
# from sqlalchemy.orm import relationship


LOGGER = logging.getLogger(__name__)


class Access:
    USER = 0
    DRIVER = 1
    ADMIN = 2


class User(Model):
    """ User Model for storing user related details """

    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(100))
    title = db.Column(db.String(20))

    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    
    password_hash = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, email, password, username, last_name=None, first_name=None, admin=False):
        """"""
        Model.__init__(self)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.username = username
        self.admin = admin
        self.registered_on = datetime.now()

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def get_username(self):
        """Return User Id."""
        return self.username

    def get_email(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def is_active(self):
        """True, as all users are active."""
        return self.active

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def get_initials(self):
        """Return the first letter of Name and Surname."""
        initials = None
        if self.first_name:
            initials = self.first_name[0].upper()
        if self.last_name:
            initials += self.last_name[0].upper()
        if initials is None:
            initials = self.email[0].upper()
        return initials

    def is_admin(self):
        return bool(self.admin)
    
    # def allowed(self, access_level):
    #     return self.access >= access_level

    @staticmethod
    def encode_auth_token(user_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
            
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        
        try:
            # print(auth_token)
            print(1)
            print(decode_token(auth_token))
            print(2)
            payload = jwt.decode(auth_token, key, algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError as error:
            LOGGER.exception(error)
            return 'Invalid token. Please log in again.'
        except Exception as error:

            LOGGER.exception(error)
            raise

    def __repr__(self):
        return "<User '{}'>".format(self.username)


# Define the Role data-model
class Role(Model):

    __tablename__ = 'roles'

    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(300), unique=True)
    permissions = db.relationship('Permission', secondary='role_permissions', backref="roles", lazy="select")

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def jsonify(self):
        perms_json = []
        for perm in self.permissions:
            perms_json.append(perm.to_json())

        data = {
            'id': self.id,
            'name': self.name,
            'permissions': perms_json,
        }
        return data


class Permission(Model):

    __tablename__ = 'permissions'

    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100), unique=True)

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
        return data


# Define the UserRoles association table
# handle many-to-many relation between Role and User
class UserRoles(Model):

    __tablename__ = 'user_roles'

    user_id = db.Column(db.String(100), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.String(100), db.ForeignKey('roles.id', ondelete='CASCADE'))


# handle many-to-many relation between Permission and Role
class RolePermissions(Model):

    __tablename__ = 'role_permissions'

    permissions_id = db.Column(db.String(100), db.ForeignKey("permissions.id"))
    role_id = db.Column(db.String(100), db.ForeignKey("roles.id"))
