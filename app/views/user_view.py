from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
from app.models.users import User
from app.schemas.user_schema import UserSchema
from app.models.token_blocklist import TokenBlocklist

user_bp = Blueprint('user_bp', __name__)

# Register User
@user_bp.route('/auth/register', methods=['POST'])
def register_user(): 
    data = request.get_json()
    user = User.find_by_username(data['username'])
    if user is not None:
        return jsonify({'message': 'User already exists'}), 409
    new_user = User(
        username=data['username'], 
        email=data['email'],
        role=data['role']
    )
    new_user.set_password(data['password'])
    new_user.create_user()
    return jsonify({'message': 'User created successfully'}), 201

# Login User
@user_bp.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.find_by_username(data['username'])
    if user and (user.check_password(data['password'])):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Login successful'
        }), 200
    session.clear()
    return jsonify({
        'message': 'Invalid username or password'
    }), 401

# Logout User
@user_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout_user():
    jti = get_jwt()['jti']
    token_blocklist = TokenBlocklist(jti=jti)
    token_blocklist.save()
    return jsonify({'message': 'Logout successful'}), 200

# Get All Users
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if claims['is_admin'] == False:
        return jsonify({'message': 'You are not authorized'}), 401
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    users = User.query.paginate(page=page, per_page=per_page)
    result = UserSchema().dump(users.items, many=True)
    return jsonify({'users': result}), 200

# Get User by ID
@user_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    claims = get_jwt()
    if claims['is_admin'] == False or claims['is_admin'] == True:
        user = User.query.get_or_404(user_id)
        result = UserSchema().dump(user)
        return jsonify({'user': result}), 200
    session.clear()
    return jsonify({'message': 'You are not authorized'}), 401

# Update User by ID
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    claims = get_jwt()
    if claims['is_admin'] == False:
        return jsonify({'message': 'You are not authorized'}), 401
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    user.role = data['role']
    user.update_user()
    return jsonify({'message': 'User updated successfully'}), 200

# Delete User by ID
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    claims = get_jwt()
    if claims['is_admin'] == False:
        return jsonify({'message': 'You are not authorized'}), 401
    user = User.query.get_or_404(user_id)
    user.delete_user()
    return jsonify({'message': 'User deleted successfully'}), 200