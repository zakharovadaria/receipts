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
