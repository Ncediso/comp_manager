import logging
from typing import Dict, Tuple, List
from ..app_utils import NotFoundError, AlreadyExistsError

from app.main.models.user import User

LOGGER = logging.getLogger(__name__)


class UserService:

    @classmethod
    def create_admin_user(cls) -> User | None:
        """Creates the admin user."""
        if User.get_all():
            LOGGER.info("Users table is not Empty, You will need an empty user table to create an Admin User")
            return None

        data = {
            'username': 'admin@fawld.com',
            'email': 'admin@fawld.com',
            'password': 'Admin@2011',
            'last_name': 'Fawld',
            'first_name': 'Admin',
            'admin': True
        }

        user = cls.create_user(data)
        return user

    @classmethod
    def create_user(cls, data: Dict[str, str]) -> User:
        email = data['email']
        user = cls.get_user_by_email(data['email'])

        if user is not None:
            message = f"User with username {email} already exists"
            LOGGER.warning(message)
            raise AlreadyExistsError(message)

        new_user = User.create(**data)
        return new_user

    @classmethod
    def get_all_users(cls) -> List[User]:
        return User.get_all()

    @classmethod
    def get_all_users_to_json(cls) -> List[Dict[str, str]]:
        return [user.to_json() for user in cls.get_all_users()]

    @classmethod
    def get_user(cls, user_id) -> User:
        return User.get_object_by_id(user_id)

    @classmethod
    def get_user_by_email(cls, email) -> User:
        user = User.query.filter_by(email=email).first()
        return user
