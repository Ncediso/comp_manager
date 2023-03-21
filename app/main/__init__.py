"""-------------------------
MODULE:
    main
DESCRIPTION:
    This package
-------------------------
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# import pyodbc

from .config import config_by_name
from .app_utils import safe_get_env_var
from .faconnect import FAConnect

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
fa_connection = FAConnect()


def create_app(config_name: str) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    CORS(app)
    db.init_app(app)
    flask_bcrypt.init_app(app)

    # client_origin_url = safe_get_env_var("CLIENT_ORIGIN_URL")
    # auth0_audience = safe_get_env_var("AUTH0_AUDIENCE")
    # auth0_domain = safe_get_env_var("AUTH0_DOMAIN")

    ##########################################
    # CORS
    ##########################################

    # CORS(
    #     app,
    #     resources={r"/api/*": {"origins": client_origin_url}},
    #     allow_headers=["Authorization", "Content-Type"],
    #     methods=["GET"],
    #     max_age=86400
    # )

    # auth0_service.initialize(auth0_domain, auth0_audience)

    return app
