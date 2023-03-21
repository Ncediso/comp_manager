from datetime import datetime, timezone, timedelta
import logging

from flask import jsonify, request, make_response
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.main.app_utils import custom_error_handler, FAObjectsDto
from app.main.faconnect import FAConnect
from app.main.fa_operations import FAUserHelper, FAProfilesHelper
from .. import fa_connection

LOGGER = logging.getLogger(__name__)

api = FAObjectsDto.api
# fa_connection = FAConnect()


@api.route('/')
class FAConnectionStatus(Resource):

    @api.doc('front_arena_connection_status')
    @custom_error_handler()
    def get(self):
        """Check Front Arena Connection Status"""
        try:
            connection_status = fa_connection.connection_status()
            make_response(jsonify({"message": connection_status}))
        except Exception as error:
            LOGGER.exception(error)
            return make_response(jsonify({"message": "Failed to check status of Front Arena Connection"}), 500)


@api.route('/connect')
class FAConnectionConnect(Resource):

    @api.doc('front_arena_connection_connect')
    @custom_error_handler()
    def get(self):
        """Connects to Front Arena"""
        try:
            if fa_connection.is_connected():
                return make_response(jsonify({"message": "Front Arena is already connected"}), 200)
            fa_connection.connect()
            return make_response(jsonify({"message": "Connected successfully"}), 200)
        except Exception as error:
            LOGGER.exception(error)
            return make_response(jsonify({"message": "Failed to connect to Front Arena"}), 500)


@api.route('/disconnect')
class FAConnectionDisconnect(Resource):

    @api.doc('front_arena_connection_status')
    @custom_error_handler()
    def get(self):
        """Disconnect Connection to Front Arena"""
        if fa_connection.is_connected() is False:
            return make_response(jsonify({"message": "Front Arena is already disconnected"}), 200)
        fa_connection.disconnect()
        return make_response(jsonify({"message": "Successfully disconnected from Front Arena"}), 200)


@api.route('/test-connection')
class FAConnectionTest(Resource):

    @api.doc('front_arena_connection_test')
    @custom_error_handler()
    def get(self):
        """Test Connection to Front Arena"""
        if fa_connection.is_connected():
            message = {"message": "Cannot test connection to Front Arena while there is an existing connection"}
            return make_response(jsonify(message), 200)
        try:
            connection = FAConnect()
            connection.connect()
            connection.disconnect()
            return make_response(jsonify({"message": "Successfully connected to Front Arena"}), 200)
        except Exception as error:
            LOGGER.exception(error)
            return make_response(jsonify({"message": "Failed to connect to Front Arena"}), 500)


@api.route('/check-configs')
class FAConnectionConfigCheck(Resource):

    @api.doc('front_arena_connection_configs_check')
    @custom_error_handler()
    def get(self):
        """Check Connection Configs for Front Arena"""
        validation_message = fa_connection.validate_environment_variables()
        if validation_message:
            message = {
                "status": "Config Validation Failed",
                "message": "Connection to Front Arena will fail until this config issue is resolved",
                "error": validation_message
            }
            return make_response(jsonify(message), 300)
        message = {
            "status": "Confi validation passed",
            "message": "All configs are set for connecting to Front Arena"
        }
        return make_response(jsonify(message), 200)


@api.route('/fa-profiles')
class FAProfiles(Resource):

    @custom_error_handler()
    @api.doc('list_of_all_user_profiles')
    def get(self):
        """Get all User Profiles"""
        profiles = FAProfilesHelper.get_all_profiles()
        return make_response(jsonify({'data': profiles}), 200)


@api.route('/fa-groups')
class FAGroups(Resource):

    @custom_error_handler()
    @api.doc('list_of_all_user_groups')
    def get(self):
        """Get all User Groups"""
        profiles = FAProfilesHelper.get_all_profiles()
        return make_response(jsonify({'data': profiles}), 200)


@api.route('/user-profiles')
class FAUserProfile(Resource):

    @api.expect(FAObjectsDto.fa_user, validate=True)
    @api.doc('create_all_user_profiles_for_user')
    @custom_error_handler()
    def get(self):
        """Get User Profiles for a Front Arena User Group"""
        data = request.json
        user_id = data['user_id']
        profiles = FAProfilesHelper.get_users_profiles(user_id)
        return make_response(jsonify({'data': profiles}), 200)

    @api.expect(FAObjectsDto.assign_user_profile, validate=True)
    @custom_error_handler()
    @api.doc('assign_user_profiles_to_user')
    def post(self):
        """Assign User Profile to Front Arena User"""
        data = request.json
        group_name = data['user_id']
        profile_name = data['profile_name']
        profiles = FAProfilesHelper.assign_group_profile(group_name, profile_name)
        return make_response(jsonify({'data': profiles}), 200)

    @api.expect(FAObjectsDto.assign_user_profile, validate=True)
    @api.doc('delete user profile link')
    @custom_error_handler()
    def delete(self):
        """Remove User Profile from Front Arena User"""
        data = request.json
        group_name = data['user_id']
        profile_name = data['profile_name']
        profiles = FAProfilesHelper.remove_group_profile(group_name, profile_name)
        return make_response(jsonify({'data': profiles}), 200)


@api.route('/group-profiles')
class FAGroupProfile(Resource):
    @api.expect(FAObjectsDto.fa_group, validate=True)
    @api.doc('create_all_user_profiles_for_user_group')
    @custom_error_handler()
    def get(self):
        """Get User Profiles for a Front Arena User Group"""
        data = request.json
        group_name = data['group_name']
        profiles = FAProfilesHelper.get_group_profiles(group_name)
        return make_response(jsonify({'data': profiles}), 200)

    @api.expect(FAObjectsDto.assign_group_profile, validate=True)
    @api.doc('assign_user_profiles_to_user_group')
    @custom_error_handler()
    def post(self):
        """Assign User Profile from Front Arena User Group"""
        data = request.json
        group_name = data['group_name']
        profile_name = data['profile_name']
        profiles = FAProfilesHelper.assign_group_profile(group_name, profile_name)
        return make_response(jsonify({'data': profiles}), 200)

    @api.expect(FAObjectsDto.assign_group_profile, validate=True)
    @api.doc('create a new user')
    @custom_error_handler()
    def delete(self):
        """Remove User Profile from Front Arena User Group"""
        data = request.json
        group_name = data['group_name']
        profile_name = data['profile_name']
        profiles = FAProfilesHelper.remove_group_profile(group_name, profile_name)
        return make_response(jsonify({'data': profiles}), 200)
