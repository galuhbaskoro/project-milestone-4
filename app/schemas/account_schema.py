from marshmallow import fields, Schema

class AccountSchema(Schema):
        id = fields.Integer()
        user_id = fields.Integer()
        account_number = fields.String()
        account_type = fields.String()
        balance = fields.Float()
        created_at = fields.DateTime()
        updated_at = fields.DateTime()
