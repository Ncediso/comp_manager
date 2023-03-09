import logging
from typing import Dict, Tuple
from ..app_utils import NotFound

from app.main.models.user import User, UserRoles
from .roles_service import RolesService

LOGGER = logging.getLogger(__name__)


class UserService:

    @classmethod
    def create_admin(cls):
        """Creates the admin user."""
        if User.get_all():
            LOGGER.info("Users table is not Empty, You will need an empty user table to create an Admin User")
            return

        new_user = User(
            username="admin@fawld.com",
            email="admin@fawld.com",
            password="Admin@2011",
            last_name="Fawld",
            first_name="Admin",
            admin=True)

        new_user.save()

    @classmethod
    def save_new_user(cls, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        email = data['email']
        user = User.query.filter_by(email=data['email']).first()

        if user is not None:
            message = f"User with username {email} already exists"
            LOGGER.info(message)
            return {"message": message}, 403

        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

        new_user.save()
        return {"message": "User created successfully"}, 201

    @staticmethod
    def get_all_users():
        return User.get_all()

    @staticmethod
    def get_a_user(user_id):
        return User.get_object_by_id(user_id)

    @staticmethod
    def generate_token(user: User) -> Tuple[Dict[str, str], int]:
        try:
            # generate the auth token
            auth_token = User.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'Authorization': auth_token # .decode()
            }
            return response_object, 201
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return response_object, 401

    @classmethod
    def assign_role(cls, user_id, role_name):
        user = cls.get_a_user(user_id)
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
