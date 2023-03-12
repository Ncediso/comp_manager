from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import UserRoleDto
from app.main.services import UserRolesService

api = UserRoleDto.api
assign_role = UserRoleDto.assign_role


@api.route('/')
class UserRolesList(Resource):
    def get(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError


@api.route('/<id>')
class UserRoles(Resource):
    @api.doc('Get user roles')
    def get(self, user_id):
        user_roles = UserRolesService.get_user_roles(user_id)
        if user_roles is None:
            api.abort(404)
        return user_roles

    @api.doc('')
    def put(self, user_id):
        pass

