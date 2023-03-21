from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import UserRoleDto
from app.main.app_utils import custom_error_handler
from app.main.services import UserRolesService, UserService


api = UserRoleDto.api
assign_role = UserRoleDto.assign_role


@api.route('/')
class UserRolesList(Resource):
    @custom_error_handler()
    def get(self):
        raise NotImplementedError()

    @custom_error_handler()
    def put(self):
        raise NotImplementedError()


@api.route('/<user_id>')
class UserRoles(Resource):
    @api.doc('Get user roles')
    @custom_error_handler()
    def get(self, user_id):
        """Get user roles"""
        user_roles = UserRolesService.get_user_roles(user_id)
        json_data = [role.to_json() for role in user_roles]
        return make_response(jsonify(json_data), 200)

    @api.doc('Get user roles')
    @api.expect(UserRoleDto.assign_role, validate=True)
    @custom_error_handler()
    def post(self, user_id):
        data = request.json
        role_name = data['role_name']
        UserRolesService.assign_role(user_id, role_name)
        response = {'message': f"Role {role_name} successfully assigned to User"}
        return make_response(jsonify(response), 201)

    @custom_error_handler()
    @api.expect(UserRoleDto.assign_role, validate=True)
    def delete(self, user_id):
        data = request.json
        role_name = data['role_name']
        UserRolesService.remove_role(user_id, role_name)
        response = {'message': f"Role {role_name} successfully removed from User"}
        return make_response(jsonify(response), 201)
