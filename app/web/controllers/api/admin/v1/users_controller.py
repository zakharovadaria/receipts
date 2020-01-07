from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, reqparse, Resource
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.web.bcrypt import bcrypt
from app.web.controllers.entities.basic_error import BasicError
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema
from db import session
from schemas import UserClientSchema

users_namespace = Namespace('users', description='Users CRUD')


@users_namespace.route('/', strict_slashes=True)
class UsersListResource(Resource):
    method_decorators = [jwt_required]

    def create_params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('role', type=str, required=True)
        parser.add_argument('active', type=bool, required=False)
        return parser.parse_args()

    def get(self) -> dict:
        users = session.query(User).all()
        users = UserClientSchema().dump(users, many=True)
        response = BasicResponse(users)
        return BasicResponseSchema().dump(response)

    def post(self) -> dict:
        create_params = self.create_params()

        hash_password = bcrypt.generate_password_hash(create_params["password"])
        hash_password = hash_password.decode('utf-8')
        create_params["password"] = hash_password

        user = User(**create_params)

        try:
            session.add(user)
            session.commit()

            user = UserClientSchema().dump(user)
            response = BasicResponse(user)
        except IntegrityError:
            session.rollback()
            raise BasicError(message='email is already exist.', status=400)

        return BasicResponseSchema().dump(response)


@users_namespace.route('/<int:id>/', strict_slashes=True)
class UsersResource(Resource):
    method_decorators = [jwt_required]

    def update_params(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, store_missing=False, required=False)
        parser.add_argument('password', type=str, store_missing=False, required=False)
        parser.add_argument('role', type=str, store_missing=False, required=False)
        parser.add_argument('active', type=bool, store_missing=False, required=False)
        return parser.parse_args()

    def get(self, id: int) -> dict:
        user = session.query(User).get(id)
        user = UserClientSchema().dump(user)
        response = BasicResponse(user)
        return BasicResponseSchema().dump(response)

    def put(self, id: int) -> dict:
        user = session.query(User).get(id)

        update_params = self.update_params()
        if update_params.get('password'):
            hash_password = bcrypt.generate_password_hash(update_params["password"])
            hash_password = hash_password.decode('utf-8')
            update_params["password"] = hash_password

        for key, value in update_params.items():
            setattr(user, key, value)

        try:
            session.commit()

            user = UserClientSchema().dump(user)
            response = BasicResponse(user)
        except IntegrityError:
            session.rollback()
            raise BasicError(message='email is already exist.', status=400)

        return BasicResponseSchema().dump(response)
