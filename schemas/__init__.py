from marshmallow import fields, Schema


class IngredientClientSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    calories = fields.Float()
