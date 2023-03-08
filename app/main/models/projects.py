from datetime import datetime, timedelta
import logging

import jwt
from typing import Union

from app.main.models import BlacklistToken
from app.main.models import Model
from ..config import key
from .. import db, flask_bcrypt
# from sqlalchemy.orm import relationship


LOGGER = logging.getLogger(__name__)


class Projects(Model):
    """ User Model for storing user related details """
    __tablename__ = "projects"


