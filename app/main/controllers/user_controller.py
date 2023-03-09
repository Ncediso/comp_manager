from flask import jsonify, make_response, request
from flask_restx import Resource
# from flask_jwt_extended import jwt_required

from app.main.app_utils.decorators import admin_token_required
from app.main.app_utils import UserDto
from app.main.services.user_service import UserService

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data', code=200)
    def get(self):
        """List all registered users"""
        all_users = UserService.get_all_users()
        return make_response(jsonify(all_users), 200)

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        response, status = UserService.save_new_user(data=data)
        return make_response(jsonify(response), status)


@api.route('/<user_id>')
@api.param('user_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(_user, envelope="user", code=200)
    def get(self, user_id):
        """Get a user given its identifier"""
        user = UserService.get_a_user(user_id)
        if user is None:
            api.abort(404)
        else:
            return make_response(jsonify(user), 200)
    
    @api.doc('updates a user')
    @api.marshal_with(UserDto.user_update, envelope="user", code=200)
    def put(self, public_id):
        """Update the user given its identifier"""
        user = UserService.get_a_user(public_id)
        if user is None:
            api.abort(404)
        else:
            req_data = request.get_json()
            user.update(req_data)
            return make_response(jsonify(user), 200)


@api.route('/<id>')
class UserRoles(Resource):
    @api.doc('Get user roles')
    def get(self, user_id):
        user = UserService.get_a_user(user_id)
        if user is None:
            api.abort(404)

    @api.doc('')
    def put(self, user_id):
        pass

