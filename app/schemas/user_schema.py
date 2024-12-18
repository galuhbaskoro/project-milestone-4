from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    role = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()