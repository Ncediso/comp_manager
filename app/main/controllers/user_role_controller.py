from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import UserRoleDto, NotFoundError, BadRequestError
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
        json_data = [role.to_json() for role in user_roles]
        return make_response(jsonify(json_data), 200)

    @api.expect(UserRoleDto.assign_role, validate=True)
    def post(self, user_id):
        data = request.json
        if 'role_name' not in data:
            raise BadRequestError("Missing role_name parameter, add correct data and retry.")
        user = UserService.get_user(user_id)
        if user is None:
            raise NotFoundError(f"User with id = {user_id} not found")

        role_name = data['role_name']
        UserRolesService.assign_role(user_id, role_name)
        response = {'message': f"Role {role_name} successfully assigned to User"}
        return make_response(jsonify(response), 201)

    @api.expect(UserRoleDto.assign_role, validate=True)
    def delete(self, user_id):
        data = request.json
        if 'role_name' not in data:
            raise BadRequestError("Missing role_name parameter, add correct data and retry.")

        user = UserService.get_user(user_id)
        if user is None:
            raise NotFoundError(f"User with id = {user_id} not found")

        role_name = data['role_name']
        UserRolesService.remove_role(user_id, role_name)
        response = {'message': f"Role {role_name} successfully removed from User"}
        return make_response(jsonify(response), 201)
