import logging
from typing import Dict, Tuple

from ..models.user import Permission, RolePermissions


LOGGER = logging.getLogger(__name__)


class PermissionsServices:

    @classmethod
    def save_new_permission(cls, data: Dict) -> Tuple[Dict[str, str], int]:

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
    def get_a_permission(permission_id):
        return Permission.get_object_by_id(permission_id)

    @classmethod
    def get_permission_by_name(cls, permission_name):
        return Permission.get_object_by_name(permission_name)

    @classmethod
    def get_permissions_by_role(cls, role_id):
        result = Permission.query.filter_by(role_id=role_id).all()
        return result

        # all_permissions = cls.get_all_permissions()
        # return list(filter(lambda perm: perm.role_id == role_id, all_permissions))
