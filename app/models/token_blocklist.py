from app.extentions.db import db

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'TokenBlocklist(id={self.id}, jti={self.jti}, created_at={self.created_at})'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    