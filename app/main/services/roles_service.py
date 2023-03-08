import logging
from typing import Dict, Tuple
from ..models.user import Role


LOGGER = logging.getLogger(__name__)


class RolesService:

    @classmethod
    def save_new_role(cls, data: Dict) -> Tuple[Dict[str, str], int]:

        role = Role.query.filter_by(name=data['name']).first()

        if role is not None:
            message = f"The role {data['name']} already exists"
            LOGGER.info(message)
            return {"message": message}, 403

        new_rol = Role(
            name=data['name'],
            description=data['description'],
        )
        new_rol.save()
        return {"message": f"Role {data['name']} created successfully"}, 201

    @staticmethod
    def get_all_roles():
        return Role.query.all()

    @staticmethod
    def get_a_role(role_id):
        return Role.get_object_by_id(role_id)

    @classmethod
    def get_role_permissions(cls, role_id):
        role = cls.get_a_role(role_id)
        permissions = role.permissions
        return permissions
