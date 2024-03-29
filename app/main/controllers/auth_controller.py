from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple

from flask import jsonify, request, make_response
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.main.services.auth_helper import Auth
from app.main.app_utils import AuthDto
from app.main.app_utils import custom_error_handler

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    
    @api.doc('User login')
    @api.expect(user_auth, validate=True)
    @custom_error_handler()
    def post(self):
        """Login a user"""
        post_data = request.json
        response = Auth.login_user(data=post_data)
        return make_response(jsonify(response), 200)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @jwt_required(refresh=True)
    @api.doc('Logout a user')
    @custom_error_handler()
    def post(self):
        """Logout user from App"""
        auth_header = request.headers.get('Authorization')
        response, status = Auth.logout_user(data=auth_header)
        return make_response(jsonify(response), status)


@api.route('/register')
class Register(Resource):
    """
    Creates a new user by taking 'user_register' input
    """

    @api.doc('Register new user')
    @api.expect(AuthDto.user_register, validate=True)
    @custom_error_handler()
    def post(self):
        """Register a new user"""
        req_data = request.get_json()
        user = Auth.register_user(data=req_data)
        response_object = {
            'message': f"User successfully created",
            'user': user.to_json()
        }
        return make_response(jsonify(response_object), )


@api.route('/refresh')
class RefreshResource(Resource):
    """
    Refreshes the use token
    """

    @api.doc('Refresh a user token')
    @jwt_required(refresh=True)
    @custom_error_handler()
    def post(self):
        """Refresh user token"""
        auth_header = request.headers.get('Authorization')
        response, status = Auth.refresh_token()
        return make_response(jsonify(response), status)
