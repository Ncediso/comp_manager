import logging
from typing import Dict, Tuple
from functools import wraps
from typing import Callable

from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_jwt_extended import unset_jwt_cookies, set_access_cookies

from ..models import User
from app.main.services.blacklist_service import BlackListServices
from app.main.services.user_service import UserService
from app.main.services.user_roles_service import UserRolesService

from ..app_utils import AlreadyExistsError, NotFoundError, UnauthorizedError, InternalServerError, InvalidUsernameError, InvalidAPIUsageBase
from ..app_utils import get_token_from_header

LOGGER = logging.getLogger(__name__)


class Auth:

    @staticmethod
    def login_user(data: Dict[str, str]):
        try:
            email = data.get('email')
            password = data.get('password')
            db_user = User.query.filter_by(email=email).first()
            if not db_user:
                raise InvalidUsernameError(f'Invalid username. No user with email {email} not found')

            if db_user.check_password(password) is False:
                error = UnauthorizedError("Invalid username or password")
                LOGGER.error(error)
                raise error

            if db_user.is_admin:
                access_token = create_access_token(
                    identity=db_user.email,
                    additional_claims={"is_administrator": True})
                refresh_token = create_refresh_token(
                    identity=db_user.email,
                    additional_claims={"is_administrator": True})
            else:
                access_token = create_access_token(identity=db_user.email)
                refresh_token = create_refresh_token(identity=db_user.email)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "message": "login successful"
            }
            set_access_cookies(make_response(response), access_token)
            return response

        except Exception as e:
            LOGGER.exception(e)
            raise InternalServerError("Failed to login, encounter error. Refresh and try again.")

    @staticmethod
    def logout_user(data: str):
        response = jsonify({"message": "logout successful"})
        unset_jwt_cookies(response)

        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if not auth_token:
            raise NotFoundError("Valid token not found. Provide a valid auth token.")
        payload = User.decode_auth_token(auth_token)
        if isinstance(payload, dict) is False:
            raise UnauthorizedError("The supplied token is invalid")
        return BlackListServices.save_token(token=auth_token)

    @staticmethod
    def is_valid_token_and_user(auth_token) -> bool:
        payload = User.decode_auth_token(auth_token)
        if isinstance(payload, dict) is False:
            raise UnauthorizedError("The supplied token is invalid")
        email = payload['sub']
        user = UserService.get_user_by_email(email)
        if not user:
            raise UnauthorizedError(f"The supplied token is invalid, No user with id {email}")
        return True

    @staticmethod
    def register_user(data: Dict[str, str]) -> User | None:
        new_user = UserService.create_user(data=data)
        if new_user.is_admin():
            role_name = "Admin"
        else:
            role_name = "User"
        UserRolesService.assign_role(new_user.id, role_name)
        return new_user

    @staticmethod
    def refresh_token():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}


def token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        # get the auth token
        auth_token = get_token_from_header()
        if not auth_token:
            raise InvalidAPIUsageBase("No token supplied token for authorization")

        if Auth.is_valid_token_and_user(auth_token) is not True:
            raise NotFoundError(f"User for the supplied token not found")
        return f(*args, **kwargs)
    return decorated


def admin_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        # get the auth token
        auth_token = get_token_from_header()

        # Error will be thrown if the token is invalid
        is_valid = Auth.is_valid_token_and_user(auth_token)
        payload = decode_token(auth_token)
        admin = payload.get('is_administrator')
        if not admin:
            raise UnauthorizedError("Unauthorised token supplied, admin token required.")

        return f(*args, **kwargs)

    return decorated
