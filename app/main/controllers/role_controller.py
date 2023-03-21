from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import RoleDto, NotFoundError
from app.main.services import RolesService, PermissionsServices
from app.main.services.auth_helper import token_required, admin_token_required

api = RoleDto.api
_role = RoleDto.role


# TODO: Separate Roles and Permissions
@api.route('/')
class RolesList(Resource):

    @admin_token_required
    @api.doc('list_of_registered_roles')
    @api.marshal_list_with(_role, envelope='data', code=200)
    def get(self):
        """Get List of all Roles"""
        roles = RolesService.get_all_roles()
        roles2 = RolesService.get_all_roles_with_deleted()
        print(roles2)
        return roles

    @api.expect(RoleDto.new_role)
    @api.response(201, 'Role successfully created.')
    @api.doc('create a new role')
    def post(self):
        """Create a new Role"""
        data = request.json
        response, status = RolesService.create_role(data=data)
        return make_response(jsonify(response), status)


@api.route('/<role_id>')
@api.param('role_id', 'The Role identifier')
@api.response(404, 'Role not found.')
class Role(Resource):

    @api.doc('get a role')
    @api.marshal_with(_role, envelope="role", code=200)
    def get(self, role_id):
        """Get a role given its identifier"""
        role = RolesService.get_role(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")
        return role

    @api.expect(_role, validate=True)
    @api.doc('updates a role')
    # @api.marshal_with(UserDto.user_update, envelope="role", code=200)
    def put(self, role_id):
        """Update the role given its identifier"""
        req_data = request.json
        role = RolesService.update_role(role_id, req_data)
        return make_response(jsonify(role), 200)

