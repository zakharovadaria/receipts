from marshmallow import fields, Schema

from app.web.controllers.entities.basic_error import BasicErrorSchema


class BasicResponse:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error


class BasicResponseSchema(Schema):
    result = fields.Raw()
    error = fields.Nested(BasicErrorSchema)
