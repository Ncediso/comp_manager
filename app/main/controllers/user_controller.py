from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.main.app_utils.decorator import admin_token_required
from ..app_utils.dto import UserDto
from ..services.user_service import UserService
from typing import Dict, Tuple

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return UserService.get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return UserService.save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user, envelope="user", code=200)
    def get(self, public_id):
        """Get a user given its identifier"""
        user = UserService.get_a_user(public_id)
        if user is None:
            api.abort(404)
        else:
            return user, 200
    
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
            return user, 200
