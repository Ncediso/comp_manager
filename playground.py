from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt, JWTManager
from flask import Flask, jsonify
from functools import wraps

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


def login():
    access_token = create_access_token(
        "admin_user", additional_claims={"is_administrator": True}
    )
    # print(access_token)
    return jsonify(access_token)


@admin_required()
def get_animals():
    return jsonify({"1": "Bull", "2": "Cow", "4": "Chicken"})


with app.app_context() as _app:
    token = login()
    print(token)
    get_animals()
