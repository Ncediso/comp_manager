from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies, set_access_cookies

from app.main.models.user import User
from ..services.blacklist_service import BlackListServices
from ..services.user_service import UserService
from typing import Dict, Tuple
import logging


LOGGER = logging.getLogger(__name__)


class Auth:

    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            # fetch the user data
            email = data.get('email')
            password = data.get('password')
            db_user = User.query.filter_by(email=email).first()
            if db_user and db_user.check_password(password):
                access_token=create_access_token(identity=db_user.email)
                refresh_token=create_refresh_token(identity=db_user.email)
                response = make_response(jsonify({
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "msg": "login successful"}))
                set_access_cookies(response, access_token)
                return response
            else:
                return jsonify({"msg":"Invalid username or password"})

        except Exception as e:
            LOGGER.exception(e)
            response_object = {
                'status': 'fail',
                'msg': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return BlackListServices.save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'msg': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'msg': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'msg': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'msg': 'Provide a valid auth token.'
            }
            return response_object, 401

    @staticmethod
    def register_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        response_object = UserService.save_new_user(data=data)
        return response_object

    @staticmethod
    def refresh_token(data: str):
        current_user=get_jwt_identity()
        new_access_token=create_access_token(identity=current_user)
        return make_response(jsonify({"access_token":new_access_token}),200)