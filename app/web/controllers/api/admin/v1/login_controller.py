from flask_restplus import Namespace, reqparse, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.user import User
from app.web.bcrypt import bcrypt
from app.web.controllers.entities.basic_error import BasicError
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session

login_namespace = Namespace('login', description='Login')

login_fields = login_namespace.model('Login', {
    'email': fields.String(example='admin@example.com'),
    'password': fields.String(example='pass'),
})


@login_namespace.route('/', strict_slashes=True)
class LoginResource(Resource):
    def params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        return parser.parse_args()

    @login_namespace.doc(model=login_fields)
    @login_namespace.expect(login_fields, validate=True)
    def post(self) -> dict:
        user_params = self.params()
        user = session.query(User).filter(User.active).filter(User.email == user_params['email']).first()

        if user:
            password = user.password.encode()

            if bcrypt.check_password_hash(password, user_params['password']):
                user.authenticated = True
                session.commit()

                access_token = create_access_token(user.email)
                refresh_token = create_refresh_token(user.email)

                response = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.id
                }

                response = BasicResponse(response)
                return BasicResponseSchema().dump(response)
            else:
                raise BasicError(message='Wrong password.', status=400)

        raise BasicError(message='User not found.', status=400)
