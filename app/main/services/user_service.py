import datetime
import logging
from typing import Dict, Tuple

from app.main import db
from app.main.models.user import User

LOGGER = logging.getLogger(__name__)


class UserService:
    
    @classmethod
    def create_admin(cls):
        """Creates the admin user."""
        if User.query.all() is None:
            new_user = User(
                username="admin@fawld.com", 
                email="admin@fawld.com",
                password="Admin@2011",
                last_name="Fawld",
                first_name="Admin",
                admin=True)
            
            new_user.save()
            return
            
        LOGGER.info("Users table is not Empty, You will need an empty user table to create an Admin User")

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
        return User.query.all()

    @staticmethod
    def get_a_user(public_id):
        return User.get_object_by_public_id(public_id)

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
