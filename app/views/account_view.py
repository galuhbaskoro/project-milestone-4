from flask import Blueprint, request, jsonify
from app.models.accounts import Account
from app.schemas.account_schema import AccountSchema
from flask_jwt_extended import jwt_required, get_jwt

account_bp = Blueprint('account_bp', __name__)

# Create Account
@account_bp.route('/account', methods=['POST'])
@jwt_required()
def create_account():

    claims = get_jwt()
    if claims is None:
        return jsonify({'message': 'You are not authorized'}), 401
    
    data = request.get_json()
    account = Account.find_by_account_number(data['account_number'])

    if account is not None:
        return jsonify({'message': 'Account already exists'}), 409
    
    new_account = Account(
        user_id=data['user_id'], 
        account_number=data['account_number'], 
        account_type=data['account_type'], 
        balance=data['balance']
    )

    new_account.create_account()

    return jsonify({'message': 'Account created successfully'}), 201

# Get All Accounts
@account_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_all_accounts():
    claims = get_jwt()
    if claims['is_admin'] == False:
        return jsonify({'message': 'You are not authorized'}), 401
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    accounts = Account.query.paginate(page=page, per_page=per_page)
    result = AccountSchema().dump(accounts.items, many=True)
    return jsonify({'accounts': result}), 200

# Get Account by ID
@account_bp.route('/account/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    claims = get_jwt()
    if claims['is_admin'] == False or claims['is_admin'] == True:
        account = Account.query.get_or_404(account_id)
        result = AccountSchema().dump(account)
        return jsonify({'account': result}), 200
    return jsonify({'message': 'You are not authorized'}), 401

# Update Account
@account_bp.route('/account/<int:account_id>', methods=['PUT'])
@jwt_required() 
def update_account(account_id):
    claims = get_jwt()
    if claims['is_admin'] == False:
        return jsonify({'message': 'You are not authorized'}), 401
    
    account = Account.query.get_or_404(account_id)
    data = request.get_json()
    account.account_number = data['account_number']
    account.account_type = data['account_type']
    account.update_account()
    return jsonify({'message': 'Account updated successfully'}), 200

# Delete Account
@account_bp.route('/account/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account_by_id(account_id):

    claims = get_jwt()

    if claims['is_admin'] == False:
        return jsonify({'message': 'You are not authorized'}), 401

    account = Account.query.get_or_404(account_id)
    account.delete_account()

    return jsonify({'message': 'Account deleted successfully'}), 200