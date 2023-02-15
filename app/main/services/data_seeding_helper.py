# from .services_helper import ServiceHelper
from ..models.user import Role
from .user_service import UserService


class DataSeeder(object):

    @classmethod
    def seed_roles(cls):
        roles = ["Admin", "User", "Line Manager", "Executive"]
        for role_name in roles:
            new_role = Role(name=role_name)
            new_role.save()

    def perform_seeding(self):
        UserService.create_admin()
        self.seed_roles()
