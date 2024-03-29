from datetime import datetime, timedelta
import logging
from typing import Union, Dict
import uuid
from flask_jwt_extended import decode_token

import jwt

from ..models.blacklist import BlacklistToken
from app.main.models.base_mixins import Model
from ..config import key
from ...main import db, flask_bcrypt
# from sqlalchemy.orm import relationship
from ..app_utils import UnauthorizedError, BlackListedTokenError, AccessDeniedError

LOGGER = logging.getLogger(__name__)


class Access:
    USER = 0
    DRIVER = 1
    ADMIN = 2


class User(Model):
    """ User Model for storing user related details """

    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
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

    roles = db.relationship('Role', secondary='user_roles', backref="users", lazy="select")

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

    @staticmethod
    def decode_auth_token(auth_token: str) -> Dict:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        
        try:
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                raise BlackListedTokenError('Token blacklisted. Please supply a valid token')
            payload = decode_token(auth_token)
            return payload
        except jwt.ExpiredSignatureError as error:
            LOGGER.exception(error)
            raise AccessDeniedError('Signature expired. Please supply a valid token')
        except jwt.InvalidTokenError as error:
            LOGGER.exception(error)
            raise AccessDeniedError('Invalid token. Please supply a valid token')
        except Exception as error:
            LOGGER.exception(error)
            raise error

    def __repr__(self):
        return "<User '{}'>".format(self.username)


# Define the Role data-model
class Role(Model):

    __tablename__ = 'roles'

    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(300), nullable=False)
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
    description = db.Column(db.String(300), nullable=False)

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
