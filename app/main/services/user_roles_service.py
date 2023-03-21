import logging
from typing import Dict, Tuple, List
from ..app_utils import NotFoundError

from app.main.models.user import User, UserRoles, RolePermissions, Role
from .roles_service import RolesService
from .user_service import UserService

LOGGER = logging.getLogger(__name__)


class UserRolesService:

    @classmethod
    def get_user_roles(cls, user_id: str) -> List[Role]:
        user = UserService.get_user(user_id)
        if not user:
            raise NotFoundError(f'User with id {user_id} not found')

        return user.roles

    @classmethod
    def assign_role(cls, user_id: str, role_name: str):
        user = UserService.get_user(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")

        role = RolesService.get_role_by_name(role_name)
        if not role:
            raise NotFoundError(f"Role with name {role_name} not found")

        user_role = UserRoles.query.filter_by(user_id=user_id, role_id=role.get_id()).first()
        if not user_role:
            user_role = UserRoles()
            user_role.user_id = user_id
            user_role.role_id = role.get_id()
            user_role.save()
        else:
            LOGGER.info("User Role already exist")

    @classmethod
    def remove_role(cls, user_id: str, role_name: str):

        user = UserService.get_user(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")

        role = RolesService.get_role_by_name(role_name)
        if not role:
            raise NotFoundError(f"Role with name {role_name} not found")

        user_role = UserRoles.query.filter_by(user_id=user_id, role_id=role.get_id()).first()

        if not user_role:
            raise NotFoundError(f"The User {user_id} does not contain the Role {role_name}")

        user_role.delete()
        LOGGER.info("Removed User Role")
