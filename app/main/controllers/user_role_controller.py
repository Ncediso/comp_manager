from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import UserRoleDto
from app.main.services import UserRolesService, UserService

api = UserRoleDto.api
assign_role = UserRoleDto.assign_role


@api.route('/')
class UserRolesList(Resource):
    def get(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()


@api.route('/<user_id>')
class UserRoles(Resource):
    @api.doc('Get user roles')
    def get(self, user_id):
        user_roles = UserRolesService.get_user_roles(user_id)
        if user_roles is None:
            api.abort(404)
        return user_roles

    @api.expect(UserRoleDto.assign_role, validate=True)
    def post(self, user_id):
        data = request.json
        if data['role_name']: pass
        role_name = data['role_name']
        user = UserService.get_a_user(user_id)
        if user is None:
            api.abort(404)

        UserRolesService.assign_role(user_id, role_name)
        response = {'msg': f"Role {role_name} successfully assigned to User"}
        return make_response(jsonify(response), 201)

    @api.expect(UserRoleDto.assign_role, validate=True)
    def delete(self, user_id):
        data = request.json
        if data['role_name']: pass
        role_name = data['role_name']
        user = UserService.get_a_user(user_id)
        if user is None:
            api.abort(404)

        UserRolesService.remove_role(user_id, role_name)
        response = {'msg': f"Role {role_name} successfully removed from User"}
        return make_response(jsonify(response), 201)

