from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import RolePermissionDto, PermissionDto
from app.main.services import RolesService, PermissionsServices


api = RolePermissionDto.api


@api.route('/')
@api.param('role_id', 'The Role identifier')
class RolePermissionList(Resource):

    @api.doc('list_of_registered_permissions')
    @api.marshal_list_with(PermissionDto.permission, envelope='data', code=200)
    def get(self, role_id):
        """Get List of all Permissions"""
        permissions = PermissionsServices.get_permissions_by_role(role_id=role_id)
        return permissions

    @api.expect(RolePermissionDto.assign_permission, validate=True)
    def post(self, role_id):
        data = request.json
        if data['permission_name']: pass
        permission_name = data['permission_name']
        role = RolesService.get_a_role(role_id)
        if role is None:
            api.abort(404)

        RolesService.assign_permission(role_id, permission_name)

    @api.expect(RolePermissionDto.assign_permission, validate=True)
    def delete(self, role_id):
        data = request.json
        if data['permission_name']: pass
        permission_name = data['permission_name']
        role = RolesService.get_a_role(role_id)
        if role is None:
            api.abort(404)

        RolesService.remove_permission(role_id, permission_name)



