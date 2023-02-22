from datetime import datetime, timezone, timedelta

from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.main.services.auth_helper import Auth
from ..app_utils.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    
    @api.doc('User login')
    @api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        """Login a user"""
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @jwt_required(refresh=True)
    @api.doc('Logout a user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Logout user from App"""
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


@api.route('/register')
class Register(Resource):
    """
    Creates a new user by taking 'user_register' input
    """

    @api.doc('Register new user')
    @api.expect(AuthDto.user_register, validate=True)
    def post(self):
        """Register a new user"""
        req_data = request.get_json()
        return Auth.register_user(data=req_data)


@api.route('/refresh')
class RefreshResource(Resource):
    """
    Refreshes the use token
    """

    @api.doc('Refresh a user token')
    @jwt_required(refresh=True)
    def post(self):
        """Refresh user token"""
        auth_header = request.headers.get('Authorization')
        return Auth.refresh_token(data=auth_header)
