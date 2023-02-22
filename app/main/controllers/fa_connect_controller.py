from datetime import datetime, timezone, timedelta
import logging

from flask import jsonify, request
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
        return jsonify({"msg": fa_connection.connection_status()})


@api.route('/connect')
class FAConnectionConnect(Resource):

    @api.doc('front_arena_connection_connect')
    def get(self):
        """Connects to Front Arena"""
        try:
            fa_connection.connect()
            return jsonify({"msg": "Connected successfully"})
        except Exception as error:
            LOGGER.exception(error)
            return jsonify({"msg": "Failed to co"})


@api.route('/disconnect')
class FAConnectionDisconnect(Resource):

    @api.doc('front_arena_connection_status')
    def get(self):
        """Disconnect Connection to Front Arena"""
        if fa_connection.is_connected() is False:
            return jsonify({"msg": "Front Arena is already disconnected"})
        fa_connection.disconnect()
        return jsonify({"msg": "Successfully disconnected from Front Arena"})


@api.route('/test-connection')
class FAConnectionTest(Resource):

    @api.doc('front_arena_connection_test')
    def get(self):
        """Test Connection to Front Arena"""
        if fa_connection.is_connected():
            return jsonify({"msg": "Cannot test connection to Front Arena while there is an existing connection"})
        try:
            connection = FAConnect()
            connection.connect()
            connection.disconnect()
            return jsonify({"msg": "Successfully connected to Front Arena"})
        except Exception as error:
            LOGGER.exception(error)
            return jsonify({"msg": "Failed to connect to Front Arena"})
