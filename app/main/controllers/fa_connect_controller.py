from datetime import datetime, timezone, timedelta
import logging

from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from app.main.faconnect import FAConnect

LOGGER = logging.getLogger(__name__)

api = Namespace('fa-connect', description='Front Arena connection related endpoints')
fa_connection = FAConnect()


@api.route('/')
class FAConnectionStatus(Resource):

    @api.doc('front_arena_connection_status')
    def get(self):
        """Check Front Arena Connection Status"""
        try:
            connection_status = fa_connection.connection_status()
            make_response(jsonify({"msg": connection_status}))
        except Exception as error:
            LOGGER.exception(error)
            return jsonify(jsonify({"msg": "Failed to check status of Front Arena Connection"}), 500)


@api.route('/connect')
class FAConnectionConnect(Resource):

    @api.doc('front_arena_connection_connect')
    def get(self):
        """Connects to Front Arena"""
        try:
            if fa_connection.is_connected():
                return make_response(jsonify({"msg": "Front Arena is already connected"}), 200)
            fa_connection.connect()
            return make_response(jsonify({"msg": "Connected successfully"}), 200)
        except Exception as error:
            LOGGER.exception(error)
            return make_response(jsonify({"msg": "Failed to connect to Front Arena"}), 500)


@api.route('/disconnect')
class FAConnectionDisconnect(Resource):

    @api.doc('front_arena_connection_status')
    def get(self):
        """Disconnect Connection to Front Arena"""
        if fa_connection.is_connected() is False:
            return make_response(jsonify({"msg": "Front Arena is already disconnected"}), 200)
        fa_connection.disconnect()
        return make_response(jsonify({"msg": "Successfully disconnected from Front Arena"}), 200)


@api.route('/test-connection')
class FAConnectionTest(Resource):

    @api.doc('front_arena_connection_test')
    def get(self):
        """Test Connection to Front Arena"""
        if fa_connection.is_connected():
            message = {"msg": "Cannot test connection to Front Arena while there is an existing connection"}
            return make_response(jsonify(message), 200)
        try:
            connection = FAConnect()
            connection.connect()
            connection.disconnect()
            return make_response(jsonify({"msg": "Successfully connected to Front Arena"}), 200)
        except Exception as error:
            LOGGER.exception(error)
            return make_response(jsonify({"msg": "Failed to connect to Front Arena"}), 500)


@api.route('/check-configs')
class FAConnectionConfigCheck(Resource):

    @api.doc('front_arena_connection_configs_check')
    def get(self):
        """Check Connection Configs for Front Arena"""
        validation_message = fa_connection.validate_environment_variables()
        if validation_message:
            message = {
                "status": "Config Validation Failed",
                "msg": "Connection to Front Arena will fail until this config issue is resolved",
                "error": validation_message
            }
            return make_response(jsonify(message), 300)
        message = {
            "status": "Confi validation passed",
            "msg": "All configs are set for connecting to Front Arena"
        }
        return make_response(jsonify(message), 200)
