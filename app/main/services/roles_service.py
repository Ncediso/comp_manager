import logging
from typing import Dict, Tuple, List
from ..app_utils.exceptions import NotFoundError, AlreadyExistsError
from ..models.user import Role, RolePermissions, Permission

from .permissions_service import PermissionsServices

LOGGER = logging.getLogger(__name__)


class RolesService:

    @classmethod
    def create_role(cls, data: Dict) -> Role | None:

        role = Role.get_object_by_name(record_name=data['name'])

        if role is not None:
            message = f"The role {data['name']} already exists"
            LOGGER.info(message)
            raise AlreadyExistsError(message, payload=data)

        new_rol = Role.create()
        new_rol.update(**data)
        # return {"message": f"Role {data['name']} created successfully"}, 201
        return new_rol

    @staticmethod
    def get_all_roles() -> List[Role]:
        return Role.get_all()

    @staticmethod
    def get_all_roles_with_deleted() -> List[Role]:
        return Role.get_all_with_deleted()

    @staticmethod
    def get_role(role_id: str) -> Role:
        return Role.get_object_by_id(role_id)

    @classmethod
    def get_role_by_name(cls, role_name: str) -> Role:
        return Role.get_object_by_name(role_name)

    @classmethod
    def get_role_permissions(cls, role_id: str) -> List[Permission]:
        role = cls.get_role(role_id)
        permissions = role.permissions
        return permissions

    @classmethod
    def assign_permission(cls, role_id: str, permission_name: str):
        role = cls.get_role(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")

        permission = PermissionsServices.get_permission_by_name(permission_name)
        if not permission:
            raise NotFoundError(f"Permission with name {permission_name} not found")

        role_permission = RolePermissions.query.filter_by(
            permission_id=permission.get_id(),
            role_id=role.get_id()).first()

        if not role_permission:
            role_permission = RolePermissions()
            role_permission.permissions_id = permission.get_id(),
            role_permission.role_id = role.get_id()
            role_permission.save()
        else:
            LOGGER.info(f"Role Permission already exist: Permission Name {permission_name}")
            raise AlreadyExistsError("Role Permission already exist", payload={'permission_name': permission})

    @classmethod
    def remove_permission(cls, role_id: str, permission_name: str):
        role = cls.get_role(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")

        permission = PermissionsServices.get_permission_by_name(permission_name)
        if not permission:
            raise NotFoundError(f"Permission with name {permission_name} not found")

        role_permission = RolePermissions.query.filter_by(
            permission_id=permission.get_id(),
            role_id=role.get_id()).first()
        if not role_permission:
            raise NotFoundError(f"The Role {role_id} does not contain the Permission {permission_name}")

        role_permission.delete()
