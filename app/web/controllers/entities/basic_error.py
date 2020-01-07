from marshmallow import Schema, fields


class BasicError(Exception):
    def __init__(self, message=None, status=500, parent_error=None):
        self.message = message
        self.status = status
        if parent_error is not None:
            if hasattr(parent_error, 'data') and isinstance(parent_error.data.get('errors'), dict):
                for key, value in parent_error.data['errors'].items():
                    self.message = "{}: {}".format(key, value)
                    break
            else:
                self.name = str(parent_error)


class BasicErrorSchema(Schema):
    message = fields.String()
