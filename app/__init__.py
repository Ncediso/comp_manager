"""-------------------------
MODULE:
    app
DESCRIPTION:
    This package
-------------------------
"""

from flask import Blueprint
from flask_restx import Api

from app.main.controllers import auth_ns, fa_connect_ns, permission_ns, roles_ns, role_perm_ns, user_ns, user_roles_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='Component Manager for Front Arena',
    version='1.0',
    description='An API with functionality to manage Access Request to Front Arena',
    authorizations=authorizations,
    security='apikey',
)


api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(fa_connect_ns, path='/api/fa-connect')
api.add_namespace(permission_ns, path='/api/permissions')
api.add_namespace(roles_ns, path='/api/roles')
api.add_namespace(role_perm_ns, path='/api/role-perm')
api.add_namespace(user_ns, path='/api/users')
api.add_namespace(user_roles_ns, path='/api/user-roles')
