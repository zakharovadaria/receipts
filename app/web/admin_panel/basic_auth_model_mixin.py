from flask import Response, redirect
from werkzeug.exceptions import HTTPException

from app.web.auth.admin_panel_basic_auth import admin_panel_basic_auth


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class BasicAuthModelMixin:
    def is_accessible(self):
        if not admin_panel_basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(admin_panel_basic_auth.challenge())
