from marshmallow import fields, Schema


class IngredientClientSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    calories = fields.Float()


class ReceiptClientSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    calories = fields.Float()
    ingredients = fields.Nested(IngredientClientSchema, many=True)
    steps = fields.List(fields.String())


class UserClientSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    role = fields.String()
    active = fields.Boolean()
    authenticated = fields.Boolean()
    receipts = fields.Nested(ReceiptClientSchema, many=True)
