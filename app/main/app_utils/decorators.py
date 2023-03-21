from functools import wraps
from typing import Callable

from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from app.main.services import Auth


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403

        return decorator

    return wrapper
