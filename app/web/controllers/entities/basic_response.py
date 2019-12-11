from marshmallow import fields, Schema


class BasicResponse:
    def __init__(self, result=None):
        self.result = result


class BasicResponseSchema(Schema):
    result = fields.Raw()
