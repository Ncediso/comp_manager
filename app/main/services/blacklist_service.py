from typing import Dict, Tuple

from app.main import db
from app.main.models import BlacklistToken


class BlackListServices:

    @classmethod
    def save_token(cls, token: str) -> Tuple[Dict[str, str], int]:
        blacklist_token = BlacklistToken(token=token)
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return response_object, 200
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': e
            }
            return response_object, 200
    
    @classmethod
    def is_blacklisted(cls):
        pass
