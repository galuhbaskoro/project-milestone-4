from marshmallow import fields, Schema

class TransactionSchema(Schema):
    id = fields.Integer()
    transaction_number = fields.String()
    from_account_id = fields.Integer()
    to_account_id = fields.Integer()
    amount = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    from_account = fields.Nested('AccountSchema', only=['id', 'account_number', 'account_type', 'balance'])
    to_account = fields.Nested('AccountSchema', only=['id', 'account_number', 'account_type', 'balance'])