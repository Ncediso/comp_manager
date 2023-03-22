from functools import wraps

from flask import make_response, jsonify


class InvalidAPIUsageBase(Exception):
    status_code = 400
    message = None
    payload = None

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    def __str__(self):
        data_str = f"{self.message}"
        if self.payload:
            data_str = data_str + f"\n while processing payload {self.payload}"
        return data_str

    def to_response(self):
        response = make_response(jsonify(self.to_dict()), self.status_code)
        return response


class NotFoundError(InvalidAPIUsageBase):
    status_code = 404


class AlreadyExistsError(InvalidAPIUsageBase):
    status_code = 409


class InternalServerError(InvalidAPIUsageBase):
    status_code = 500


class SchemaValidationError(InvalidAPIUsageBase):
    status_code = 400


class UpdateError(InvalidAPIUsageBase):
    status_code = 422


class DeletionError(InvalidAPIUsageBase):
    status_code = 403


class UnauthorizedError(InvalidAPIUsageBase):
    status_code = 401


class InvalidUsernameError(UnauthorizedError):
    pass


class InvalidPasswordError(UnauthorizedError):
    pass


class BlackListedTokenError(InvalidAPIUsageBase):
    status_code = 498


class BadRequestError(InvalidAPIUsageBase):
    pass


class FAConnectionError(InvalidAPIUsageBase):
    status_code = 503


class AccessDeniedError(InvalidAPIUsageBase):
    status_code = 403


def handle_request_errors():
    response = make_response(jsonify({'message': 'All is well'}), 200)
    try:
        raise UnauthorizedError("user not authorised")
    except InvalidAPIUsageBase as error:
        response = error.to_response()
    except Exception as error:
        response = make_response(jsonify({'message': 'An error occurred please try again'}), 500)
    finally:
        return response


def custom_error_handler():
    def wrapper(fn):
        @wraps(fn)
        def inner_function(*args, **kwargs):
            response = None
            try:
                response = fn(*args, **kwargs)
            except InvalidAPIUsageBase as error:
                response = error.to_response()
            except BaseException as error:
                response = make_response(jsonify({'message': f'An error occurred please try again {error}'}), 500)
            finally:
                return response
        return inner_function
    return wrapper
