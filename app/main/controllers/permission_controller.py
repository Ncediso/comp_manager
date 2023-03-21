from flask import jsonify, make_response, request
from flask_restx import Resource
from app.main.app_utils import PermissionDto
from app.main.services import PermissionsServices


api = PermissionDto.api


@api.route('/')
class PermissionsList(Resource):

    @api.doc('list_of_registered_permissions')
    @api.marshal_list_with(PermissionDto.permission, envelope='data', code=200)
    def get(self):
        """Get List of all Permissions"""
        permissions = PermissionsServices.get_all_permissions()
        return permissions

    @api.expect(PermissionDto.new_permission, validate=True)
    @api.doc('create a role')
    # @api.marshal_with(UserDto.user_update, envelope="role", code=200)
    def post(self):
        """Create a new Permission"""
        req_data = request.json
        response, status = PermissionsServices.create_permission(req_data)
        return make_response(jsonify(response), status)
