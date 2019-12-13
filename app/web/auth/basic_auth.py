import base64

from flask import current_app
from flask_basicauth import BasicAuth as StandardBasicAuth
from flask_restplus import abort


class BasicAuth(StandardBasicAuth):
    role_name = 'user'

    def username_key(self):
        return f'BASIC_AUTH_{self.role_name.upper()}_NAME'

    def password_key(self):
        return f'BASIC_AUTH_{self.role_name.upper()}_PASS'

    def get_token(self):
        username, password = current_app.config[self.username_key()], current_app.config[self.password_key()]
        token = f'{username}:{password}'.encode()
        token = base64.b64encode(token).decode()
        return token

    def check_credentials(self, username, password):
        correct_username = current_app.config[self.username_key()]
        correct_password = current_app.config[self.password_key()]
        return username == correct_username and password == correct_password

    def challenge(self):
        raise abort(401)

