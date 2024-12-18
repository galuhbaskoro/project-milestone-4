from flask import Flask, jsonify
from flask_migrate import Migrate
from app.extentions.db import db
from app.extentions.jwt import jwt
from app.config.development import DevelopmentConfig
from app.models.users import User
from app.models.token_blocklist import TokenBlocklist
from app.views import user_bp, account_bp, transaction_bp

def create_app():
    
    # app config
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # register database config and migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # register jwt
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(account_bp, url_prefix='/api')
    app.register_blueprint(transaction_bp, url_prefix='/api')

    #  JWT Auth
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.find_by_username(identity) or None

    # JWT Claims Identity
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = User.find_by_username(username=identity)
        if user and user.role == "admin":
            return {"is_admin": True}
        return {"is_admin": False}   

    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Request does not contain valid token", "error": "authorization_header"}), 403

    # Token Blocklist
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return TokenBlocklist.query.filter_by(jti=jwt_data["jti"]).first(), 401

    return app