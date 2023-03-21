from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import RolePermissionDto, PermissionDto
from app.main.services import RolesService, PermissionsServices

from ..models.user import RolePermissions
api = RolePermissionDto.api


class RolePermissionList(Resource):

    def get(self):
        return NotImplementedError()

    def put(self):
        raise NotImplementedError()


@api.route('/<role_id>')
@api.param('role_id', 'The Role identifier')
class RolePermission(Resource):

    @api.doc('list_of_registered_permissions')
    @api.marshal_list_with(PermissionDto.permission, envelope='data', code=200)
    def get(self, role_id):
        """Get List of all Permissions"""

        permissions = PermissionsServices.get_role_permissions(role_id=role_id)
        return make_response(jsonify(permissions), 200)

    @api.expect(RolePermissionDto.assign_permission, validate=True)
    def post(self, role_id):
        data = request.json
        permission_name = data['permission_name']
        RolesService.assign_permission(role_id, permission_name)
        response = {'message': f"Permission {permission_name} successfully assigned to Role"}
        return make_response(jsonify(response), 201)

    @api.expect(RolePermissionDto.assign_permission, validate=True)
    def delete(self, role_id):
        data = request.json
        permission_name = data['permission_name']
        RolesService.remove_permission(role_id, permission_name)
        response = {'message': f"Permission {permission_name} successfully removed from Role"}
        return make_response(jsonify(response), 201)



