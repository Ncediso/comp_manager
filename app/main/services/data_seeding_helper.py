# from .services_helper import ServiceHelper
from app.main.models import Role
from app.main.services.user_service import UserService
from app.main.services.roles_service import RolesService


DEFAULT_ROLES = {
    "Admin": "Administrator",
    "User": "General User"
}


class DataSeeder(object):

    @classmethod
    def seed_roles(cls):
        for role_name, description in DEFAULT_ROLES.items():
            data = {
                'name': role_name,
                'description': description
            }
            RolesService.save_new_role(data)

    @classmethod
    def seed_admin(cls):
        UserService.create_admin()
        # TODO: Add Admin Role to admin user

    @classmethod
    def seed(cls):
        cls.seed_roles()
        cls.seed_admin()
