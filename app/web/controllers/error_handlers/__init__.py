from flask import jsonify, Blueprint

from app.web.controllers.entities.basic_error import BasicError
from app.web.controllers.entities.basic_response import BasicResponse, BasicResponseSchema

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(BasicError)
def basic_error_handler(error):
    basic_response = BasicResponse(error=error)
    response = jsonify(BasicResponseSchema().dump(basic_response))
    response.status_code = error.status
    return response


@blueprint.app_errorhandler(Exception)
def other_error_handler(error):
    print(error)
    basic_error_element = BasicError(parent_error=error)
    basic_response = BasicResponse(error=basic_error_element)
    response = jsonify(BasicResponseSchema().dump(basic_response))
    response.status_code = 500
    return response
