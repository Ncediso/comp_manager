from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import RoleDto
from app.main.services import RolesService, PermissionsServices

api = RoleDto.api
_role = RoleDto.role


# TODO: Separate Roles and Permissions

@api.route('/')
class RolesList(Resource):

    @api.doc('list_of_registered_roles')
    @api.marshal_list_with(_role, envelope='data', code=200)
    def get(self):
        """Get List of all Roles"""
        roles = RolesService.get_all_roles()
        return roles

    @api.expect(RoleDto.new_role)
    @api.response(201, 'Role successfully created.')
    @api.doc('create a new role')
    def post(self):
        """Create a new Role"""
        data = request.json
        response, status = RolesService.save_new_role(data=data)
        return make_response(jsonify(response), status)


@api.route('/<role_id>')
@api.param('role_id', 'The Role identifier')
@api.response(404, 'Role not found.')
class Role(Resource):

    @api.doc('get a role')
    @api.marshal_with(_role, envelope="role", code=200)
    def get(self, role_id):
        """Get a role given its identifier"""
        role = RolesService.get_a_role(role_id)
        if role is None:
            api.abort(404)
        else:
            return role

    @api.expect(_role, validate=True)
    @api.doc('updates a role')
    # @api.marshal_with(UserDto.user_update, envelope="role", code=200)
    def put(self, role_id):
        """Update the role given its identifier"""
        role = RolesService.get_a_role(role_id)
        if role is None:
            api.abort(404)
        else:
            req_data = request.get_json()
            role.update(req_data)
            return make_response(jsonify(role), 200)


@api.route('/permissions')
class PermissionsList(Resource):

    @api.doc('list_of_registered_permissions')
    @api.marshal_list_with(RoleDto.permission, envelope='data', code=200)
    def get(self):
        """Get List of all Permissions"""
        permissions = PermissionsServices.get_all_permissions()
        return permissions

    @api.expect(RoleDto.new_permission, validate=True)
    @api.doc('create a role')
    # @api.marshal_with(UserDto.user_update, envelope="role", code=200)
    def post(self):
        """Create a new Permission"""
        req_data = request.json
        response, status = PermissionsServices.save_new_permission(req_data)
        return make_response(jsonify(response), status)


@api.route('/<role_id>/permissions')
class RolePermissions(Resource):

    @api.doc('list_of_registered_roles')
    # @api.marshal_list_with(permissions, envelope='data', code=200)
    def get(self, role_id):
        """Get List of all Permissions"""
        permissions = PermissionsServices.get_permissions_by_role(role_id=role_id)
        return permissions

    @api.expect(RoleDto.assign_permission, validate=True)
    def post(self, role_id):
        data = request.json
        if data['role_id']: pass
        if data['permission_name']: pass
        role_id = data['role_id']
        permission_name = data['permission_name']
        role = RolesService.get_a_role(role_id)
        if role is None:
            api.abort(404)

        RolesService.assign_permission(role_id, permission_name)

    @api.expect(RoleDto.assign_permission, validate=True)
    def delete(self):
        pass


