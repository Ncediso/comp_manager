from flask_restx import Api
from flask import Blueprint

from app.main.controllers import user_ns
from app.main.controllers import auth_ns
from app.main.controllers import fa_connect_ns

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
    security='apikey'
)


api.add_namespace(fa_connect_ns, path='/api/fa-connect')
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(user_ns, path='/api/users')
