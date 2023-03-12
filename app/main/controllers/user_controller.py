from flask import jsonify, make_response, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.main.app_utils.decorators import admin_token_required, admin_required
from app.main.app_utils import UserDto
from app.main.services.user_service import UserService

api = UserDto.api
_user = UserDto.user
# _u_de = UserDto.user_detail_list


@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    # @admin_required()
    @api.marshal_list_with(_user, envelope='data', code=200)
    # @jwt_required()
    def get(self):
        """List all registered users"""
        all_users = UserService.get_all_users()
        # all_users = UserService.get_all_users_to_json()
        print(all_users)
        # _users = jsonify(all_users)
        # print(_users)
        # return make_response(all_users, 200)
        return all_users

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
            return user

    @api.expect(_user, validate=True)
    @api.doc('updates a user')
    # @api.marshal_with(UserDto.user_update, envelope="user", code=200)
    def put(self, user_id):
        """Update the user given its identifier"""
        user = UserService.get_a_user(user_id)
        if user is None:
            api.abort(404)
        else:
            req_data = request.get_json()
            user.update(req_data)
            return make_response(jsonify(user), 200)

