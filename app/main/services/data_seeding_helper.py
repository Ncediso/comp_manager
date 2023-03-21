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
      "name": "FA Profiles",
      "description": "Front Arena Components"
    },
    {
      "name": "FA System User",
      "description": "Front Arena System User ",
    },
    {
      "name": "FA System Group",
      "description": "Front Arena System Group ",
    },
    {
      "name": "FA System Organisation",
      "description": "Front Arena System Organisation",
    },
    {
      "name": "FA User Profiles",
      "description": "Front Arena User Profiles - allows users access to Front Arena User Groups",
    },
    {
      "name": "FA Group Profiles",
      "description": "Front Arena Group Profiles - allows users access to Front Arena User Groups",
    },
    {
      "name": "FA Move User to Group",
      "description": "Front Arena Move User to Group - allows users move from one Group to another",
    }
]


class DataSeeder(object):

    @classmethod
    def seed_roles(cls):
        for data in DEFAULT_ROLES:
            RolesService.create_role(data)

    @classmethod
    def seed_admin(cls):
        user = UserService.create_admin_user()
        if user:
            UserRolesService.assign_role(user.id, ADMIN_ROLE_NAME)

    @classmethod
    def seed_permissions(cls):
        for permission_data in DEFAULT_PERMISSIONS:
            PermissionsServices.create_permission(permission_data)

    @classmethod
    def seed(cls):
        cls.seed_permissions()
        cls.seed_roles()
        cls.seed_admin()
