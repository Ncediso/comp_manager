"""-------------------------
MODULE:
    app_utils

DESCRIPTION:
    This package
-------------------------
"""

from os import environ

from flask import jsonify, abort

from .dto import AuthDto, UserDto
# from .decorators import token_required, admin_token_required
from .constants import VARS


# May have to move this function to a better place
def json_abort(status_code, data=None):
    response = jsonify(data)
    response.status_code = status_code
    abort(response)


def safe_get_env_var(key):
    try:
        return environ[key]
    except KeyError:
        raise NameError(f"Missing {key} environment variable.")
