from app.extentions.db import db

class Transaction(db.Model):
    
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_number = db.Column(db.String(55), nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    transaction_type = db.Column(db.String(55), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    from_account = db.relationship('Account', foreign_keys=[from_account_id], back_populates='outgoing_transactions')
    to_account = db.relationship('Account', foreign_keys=[to_account_id], back_populates='incoming_transactions')

    def __repr__(self):
        return f'id: {self.id}, account_id: {self.account_id}, transaction_number: {self.transaction_number}, transaction_type: {self.transaction_type}, amount: {self.amount}, created_at: {self.created_at}, updated_at: {self.updated_at}, from_account: {self.from_account}, to_account: {self.to_account}'

    @classmethod

    def find_by_transaction_number(cls, transaction_number):
        return cls.query.filter_by(transaction_number=transaction_number).first()
    
    def create_transaction(self):
        db.session.add(self)
        db.session.commit()

    def update_transaction(self):
        db.session.commit()
    
    def delete_transaction(self):
        db.session.delete(self)
        db.session.commit()
    
