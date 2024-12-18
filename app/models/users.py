from app.extentions.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(55), unique=True, nullable=False)
    email = db.Column(db.String(55), unique=True, nullable=False)
    role = db.Column(db.String(55), nullable=True, default='customer')
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    accounts = db.relationship('Account', back_populates='user')

    def __repr__(self):
        return f'id: {self.id}, username: {self.username}, email: {self.email}, role: {self.role}, password: {self.password}, created_at: {self.created_at}, updated_at: {self.updated_at}, accounts: {self.accounts}'
    
    def set_password(self, password):
       self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def create_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self):
        db.session.commit()
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()