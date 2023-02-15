from flask_restx import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_ns
from .main.controllers.auth_controller import api as auth_ns

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
    title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey'
)


api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(user_ns, path='/api/users')
