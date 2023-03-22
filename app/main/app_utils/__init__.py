"""-------------------------
MODULE:
    app_utils

DESCRIPTION:
    This package
-------------------------
"""

from functools import wraps
from typing import Callable
from os import environ

from flask import jsonify, abort, request

from .dto import AuthDto, PermissionDto, RoleDto, RolePermissionDto, UserDto, UserRoleDto, FAObjectsDto
# from .decorators import token_required, admin_token_required
from .constants import VARS
from .exceptions import (
    AccessDeniedError,
    AlreadyExistsError,
    BadRequestError,
    BlackListedTokenError,
    InternalServerError,
    InvalidAPIUsageBase,
    NotFoundError,
    UnauthorizedError,
    InvalidUsernameError,
    custom_error_handler,
    FAConnectionError,
    )

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


def get_token_from_header():
    auth_key = 'Authorization'
    if auth_key not in request.headers:
        return None
    auth_token = request.headers.get(auth_key)
    if auth_token:
        auth_token = auth_token.split(" ")[1]
        return auth_token
    return None
