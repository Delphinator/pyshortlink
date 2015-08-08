from functools import wraps

from flask import Response, abort, request

from .app import db
from .model import Token


def check_auth(token):
    """This function is called to check if a token is valid."""
    try:
        token = Token.query.filter_by(token=token, deleted=None).one()
        return True
    except db.NoResultFound:
        return False


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'X-Token' not in request.headers or \
                not check_auth(request.headers['X-Token']):
            abort(403)
        return f(*args, **kwargs)
    return decorated
