# from .services_helper import ServiceHelper
from app.main.models import Role
from app.main.services.user_service import UserService
from app.main.services.roles_service import RolesService
from app.main.services.user_roles_service import UserRolesService
from app.main.services.permissions_service import PermissionsServices

ADMIN_ROLE_NAME = 'Admin'

DEFAULT_ROLES = [
    {
        'name': ADMIN_ROLE_NAME,
        'description': 'Administrator'
    },
    {
        'name': 'User',
        'description': "General User"
    },
]


DEFAULT_PERMISSIONS = [
    {
      "name": "FA Components",
      "description": "Front Arena Components "
    },
    {
      "name": "FA System User",
      "description": "Front Arena System User ",
    },
    {
      "name": "FA Group Components",
      "description": "Front Arena Group Components - allows users access to Front Arena User Groups",
    }
]


class DataSeeder(object):

    @classmethod
    def seed_roles(cls):
        for data in DEFAULT_ROLES:
            RolesService.save_new_role(data)

    @classmethod
    def seed_admin(cls):
        user = UserService.create_admin()
        UserRolesService.assign_role(user.id, ADMIN_ROLE_NAME)

    @classmethod
    def seed_permissions(cls):
        for permission_data in DEFAULT_PERMISSIONS:
            PermissionsServices.save_new_permission(permission_data)

    @classmethod
    def seed(cls):
        cls.seed_permissions()
        cls.seed_roles()
        cls.seed_admin()
