import os
import unittest
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # , MigrateCommand
# from flask_script import Manager

from app import blueprint, api
from app.main import create_app, db
from app.main.models import user, blacklist
from app.main.services.data_seeding_helper import DataSeeder

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

_app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

jwt = JWTManager(_app)
# This is where the duck typing magic comes in
jwt._set_error_handler_callbacks(api)


# Callback function to check if a JWT exists in the database blocklist
# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_payload):
#     token = jwt_payload["jti"]

#     return token is not None

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@_app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


_app.register_blueprint(blueprint)
_app.app_context().push()

# manager = Manager(_app)
migrate = Migrate(_app, db, render_as_batch=True)


# manager.add_command('db', MigrateCommand)
# @manager.command
@_app.cli.command('test')
def run():
    _app.run()


# @manager.command
@_app.cli.command('test')
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@_app.cli.command('db_seed')
def db_seed():
    DataSeeder.seed_roles()
    DataSeeder.seed_services()


if __name__ == '__main__':
    _app.run()
