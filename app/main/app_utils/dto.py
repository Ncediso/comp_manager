# from inspect import _Object
from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier')
    })
    
    user_update = api.model('edit_user_details',{
        "title": fields.String(required=True, min_length=1, max_length=20),
        "first_name": fields.String(required=True, min_length=1, max_length=100),
        "username": fields.String(required=True, min_length=2, max_length=100),
        "email": fields.String(required=True, min_length=4, max_length=255),
        "gender": fields.String(required=True, min_length=4, max_length=6),
        "phone": fields.String(required=True, min_length=7, max_length=20),
        "last_name": fields.String(required=True, min_length=4, max_length=100)
    })
    
    admin_user_update = api.model('admin_edit_user_details', {
        "title": fields.String(required=True, min_length=1, max_length=20),
        "first_name": fields.String(required=True, min_length=1, max_length=100),
        "username": fields.String(required=True, min_length=2, max_length=100),
        "email": fields.String(required=True, min_length=4, max_length=255),
        "gender": fields.String(required=True, min_length=4, max_length=6),
        "phone": fields.String(required=True, min_length=7, max_length=20),
        "last_name": fields.String(required=True, min_length=4, max_length=100),
        "admin": fields.Boolean(),
        "active": fields.Boolean()
    })


class AuthDto:
    api = Namespace('auth', description='Authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

    user_register = api.model('new_user_details', {
        "username": fields.String(required=True, min_length=2, max_length=32),
        "email": fields.String(required=True, min_length=4, max_length=64),
        "password": fields.String(required=True, min_length=4, max_length=16)
    })