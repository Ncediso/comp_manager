import logging
from typing import Dict, Tuple
from ..app_utils.custom_exceptions import NotFound
from ..models.user import Role, RolePermissions

from .permissions_service import PermissionsServices

LOGGER = logging.getLogger(__name__)


class RolesService:

    @classmethod
    def save_new_role(cls, data: Dict) -> Tuple[Dict[str, str], int]:

        role = Role.get_object_by_name(record_name=data['name'])

        if role is not None:
            message = f"The role {data['name']} already exists"
            LOGGER.info(message)
            return {"message": message}, 403

        new_rol = Role.create()
        new_rol.update(**data)
        # new_rol = Role(
        #     name=data['name'],
        #     description=data['description'],
        # )
        # new_rol.save()
        return {"message": f"Role {data['name']} created successfully"}, 201

    @staticmethod
    def get_all_roles():
        return Role.get_all()

    @staticmethod
    def get_all_roles_with_deleted():
        return Role.get_all_with_deleted()

    @staticmethod
    def get_a_role(role_id):
        return Role.get_object_by_id(role_id)

    @classmethod
    def get_role_by_name(cls, role_name):
        return Role.get_object_by_name(role_name)

    @classmethod
    def get_role_permissions(cls, role_id):
        role = cls.get_a_role(role_id)
        permissions = role.permissions
        return permissions

    @classmethod
    def assign_permission(cls, role_id, permission_name):
        role = cls.get_a_role(role_id)
        if not role:
            raise NotFound(f"Role with id {role_id} not found")

        permission = PermissionsServices.get_permission_by_name(permission_name)
        if not permission:
            raise NotFound(f"Permission with name {permission_name} not found")

        role_permission = RolePermissions.query.filter_by(permission_id=permission.get_id(), role_id=role.get_id()).first()
        if not role_permission:
            role_permission = RolePermissions()
            role_permission.permissions_id = permission.get_id(),
            role_permission.role_id = role.get_id()
            role_permission.save()
        else:
            LOGGER.info("User Role already exist")

    @classmethod
    def remove_permission(cls, role_id, permission_name):
        role = cls.get_a_role(role_id)
        if not role:
            raise NotFound(f"Role with id {role_id} not found")

        permission = PermissionsServices.get_permission_by_name(permission_name)
        if not permission:
            raise NotFound(f"Permission with name {permission_name} not found")

        role_permission = RolePermissions.query.filter_by(
            permission_id=permission.get_id(),
            role_id=role.get_id()).first()
        if not role_permission:
            raise NotFound(f"The Role {role_id} does not contain the Permission {permission_name}")

        role_permission.delete()
