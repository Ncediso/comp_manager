import logging
from typing import Dict, Tuple, List

from ..models.user import Permission, RolePermissions, Role
from ..app_utils import NotFoundError

LOGGER = logging.getLogger(__name__)


class PermissionsServices:

    @classmethod
    def create_permission(cls, data: Dict) -> Tuple[Dict[str, str], int]:

        permission = Permission.get_object_by_name(record_name=data['name'])

        if permission is not None:
            message = f"The role {data['name']} already exists"
            LOGGER.info(message)
            return {"message": message}, 403

        new_permission = Permission.create(**data)
        # new_permission.update()
        # permission = Permission(
        #     name=data['name'],
        #     description=data['description'],
        # )
        # new_permission.save()
        return {"message": f"Permission {data['name']} created successfully"}, 201

    @staticmethod
    def get_all_permissions():
        return Permission.get_all()

    @staticmethod
    def get_permission(permission_id):
        return Permission.get_object_by_id(permission_id)

    @classmethod
    def get_permission_by_name(cls, permission_name):
        return Permission.get_object_by_name(permission_name)

    @classmethod
    def get_role_permissions(cls, role_id: str) -> List[Permission]:
        role = Role.get(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")

        permissions = role.permissions
        return permissions
