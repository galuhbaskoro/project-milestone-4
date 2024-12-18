from app.extentions.db import db
from app.models.transactions import Transaction

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(55), nullable=False)
    account_type = db.Column(db.String(55), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user = db.relationship('User', back_populates='accounts')
    outgoing_transactions = db.relationship('Transaction', foreign_keys='Transaction.from_account_id', back_populates='from_account')
    incoming_transactions = db.relationship('Transaction', foreign_keys='Transaction.to_account_id', back_populates='to_account')

    def __repr__(self):
        return f'id: {self.id}, user_id: {self.user_id}, account_number: {self.account_number}, account_type: {self.account_type}, balance: {self.balance}, created_at: {self.created_at}, updated_at: {self.updated_at}, user: {self.user}, outgoing_transactions: {self.outgoing_transactions}, incoming_transactions: {self.incoming_transactions}'
    
    @classmethod

    def find_by_account_number(cls, account_number):
        return cls.query.filter_by(account_number=account_number).first()
    
    def create_account(self):
        db.session.add(self)
        db.session.commit()
    
    def update_account(self):
        db.session.commit()

    def delete_account(self):
        db.session.delete(self)
        db.session.commit()