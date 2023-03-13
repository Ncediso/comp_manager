import logging
from typing import Dict, Tuple
from ..app_utils import NotFound

from app.main.models.user import User, UserRoles, RolePermissions
from .roles_service import RolesService
from .user_service import UserService

LOGGER = logging.getLogger(__name__)


class UserRolesService:

    @classmethod
    def get_user_roles(cls, user_id):
        user = UserService.get_a_user(user_id)
        if not user:
            raise NotFound(f'User with id {user_id} not found')

        user_roles = UserRoles.query.filter_by(user_id=user_id)
        json_data = [role.to_json() for role in user_roles]
        return json_data

    @classmethod
    def get_role_permissions(cls, role_name):
        role = RolesService.get_role_by_name(role_name)
        if not role:
            raise NotFound(f"Role with name {role_name} not found")

        user_permissions = RolePermissions.query.filter_by(role_id=role.get_id())
        json_data = [permission.to_json() for permission in user_permissions]
        return json_data

    @classmethod
    def assign_role(cls, user_id, role_name):
        user = UserService.get_a_user(user_id)
        if not user:
            raise NotFound(f"User with id {user_id} not found")

        role = RolesService.get_role_by_name(role_name)
        if not role:
            raise NotFound(f"Role with name {role_name} not found")

        user_role = UserRoles.query.filter_by(user_id=user_id, role_id=role.get_id()).first()
        if not user_role:
            user_role = UserRoles()
            user_role.user_id = user_id,
            user_role.role_id = role.get_id()
            user_role.save()
        else:
            LOGGER.info("User Role already exist")

    @classmethod
    def remove_role(cls, user_id, role_name):

        user = UserService.get_a_user(user_id)
        if not user:
            raise NotFound(f"User with id {user_id} not found")

        role = RolesService.get_role_by_name(role_name)
        if not role:
            raise NotFound(f"Role with name {role_name} not found")

        user_role = UserRoles.query.filter_by(user_id=user_id, role_id=role.get_id()).first()

        if not user_role:
            raise NotFound(f"The User {user_id} does not contain the Role {role_name}")

        user_role.delete()
        LOGGER.info("Removed User Role")
