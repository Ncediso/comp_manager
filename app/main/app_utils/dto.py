# from inspect import _Object
from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description="User related operations")
    user = api.model('user', {
        'id': fields.String(description="user identifier"),
        'email': fields.String(required=True, description="user email address"),
        'username': fields.String(required=True, description="user username"),
        'first_name': fields.String(required=True, min_length=1, max_length=100),
        'last_name': fields.String(required=True, min_length=4, max_length=100),
        'title': fields.String(required=True, min_length=1, max_length=20),
        'gender': fields.String(required=True, min_length=4, max_length=6),
        'phone': fields.String(required=True, min_length=7, max_length=20),
        'active': fields.Boolean(required=True),
        'admin': fields.Boolean(required=True),
        'registered_on': fields.DateTime(required=True, description="Date and Time user was registered on the system"),
        'create_time': fields.DateTime(required=True, description="Date and Time user was created on the system"),
        'update_time': fields.DateTime(required=True, description="Date and Time user was updated on the system"),
    })

    user_update = api.model('edit_user_details', {
        'title': fields.String(required=True, min_length=1, max_length=20),
        'first_name': fields.String(required=True, min_length=1, max_length=100),
        'username': fields.String(required=True, min_length=2, max_length=100),
        'email': fields.String(required=True, min_length=4, max_length=255),
        'gender': fields.String(required=True, min_length=4, max_length=6),
        'phone': fields.String(required=True, min_length=7, max_length=20),
        'last_name': fields.String(required=True, min_length=4, max_length=100)
    })

    # user_detail_list = {
    #     "users": fields.List(fields.Nested(user_update))
    # }

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


class UserRoleDto:
    api = Namespace('user-roles', description='User Roles related operations')

    assign_role = api.model('assign_role', {
        'user_id': fields.String(required=True, description='user identifier'),
        'role_name': fields.String(required=True, description='role name'),
    })


class RoleDto:
    api = Namespace('role', description="Roles and Permissions related operations")
    role = api.model('role', {
        'id': fields.String(description="user identifier"),
        'name': fields.String(required=True, min_length=1, max_length=100),
        'description': fields.String(required=True, min_length=4, max_length=100),
    })

    new_role = api.model('new_role', {
        'name': fields.String(required=True, min_length=1, max_length=100),
        'description': fields.String(required=True, min_length=4, max_length=100),
    })

    assign_permission = api.model('assign_permission', {
        'role_id': fields.String(required=True, min_length=1, max_length=100),
        'permission_name': fields.String(required=True, min_length=4, max_length=100),
    })

    permission = api.model('permission', {
        'id': fields.String(description="permission identifier"),
        'name': fields.String(required=True, min_length=1, max_length=100),
        'description': fields.String(required=True, min_length=4, max_length=100),
        'create_time': fields.DateTime(required=True, description="Date and Time user was created on the system"),
        'update_time': fields.DateTime(required=True, description="Date and Time user was updated on the system"),
    })

    new_permission = api.model('new_permission', {
        'name': fields.String(required=True, min_length=1, max_length=100),
        'description': fields.String(required=True, min_length=4, max_length=100),
    })




