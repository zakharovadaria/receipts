from flask_restplus import Namespace, reqparse, Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.user import User
from app.web.bcrypt import bcrypt
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session

login_namespace = Namespace('login', description='Login')


@login_namespace.route('/', strict_slashes=True)
class LoginResource(Resource):
    def params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        return parser.parse_args()

    def post(self) -> dict:
        user_params = self.params()
        user = session.query(User).filter(User.email == user_params['email']).first()
        password = user.password.encode()

        if bcrypt.check_password_hash(password, user_params['password']):
            user.authenticated = True
            session.commit()

            access_token = create_access_token(user.email)
            refresh_token = create_refresh_token(user.email)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            response = BasicResponse(response)
            return BasicResponseSchema().dump(response)


