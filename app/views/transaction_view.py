from flask import Blueprint, request, jsonify
from app.models.transactions import Transaction
from app.schemas.transaction_schema import TransactionSchema
from flask_jwt_extended import jwt_required, get_jwt

transaction_bp = Blueprint('transaction_bp', __name__)

# Create Transaction
@transaction_bp.route('/transaction', methods=['POST'])
@jwt_required()
def create_transaction():
    claims = get_jwt()
    if claims is None:
        return jsonify({'message': 'You are not authorized'}), 401
    data = request.get_json()
    transaction = Transaction.find_by_transaction_number(data['transaction_number'])

    if transaction is not None:
        return jsonify({'message': 'Transaction already exists'}), 409
    
    new_transaction = Transaction(
        transaction_number=data['transaction_number'], 
        from_account_id=data['from_account_id'], 
        to_account_id=data['to_account_id'], 
        transaction_type=data['transaction_type'], 
        amount=data['amount']
    )

    new_transaction.create_transaction()

    return jsonify({'message': 'Transaction created successfully'}), 201

# Get All Transactions
@transaction_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_all_transactions():
    claims = get_jwt()
    if claims is None:
        return jsonify({'message': 'You are not authorized'}), 401
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    transactions = Transaction.query.paginate(page=page, per_page=per_page)
    result = TransactionSchema().dump(transactions.items, many=True)
    return jsonify({'transactions': result}), 200

# Get Transaction by ID
@transaction_bp.route('/transaction/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    claims = get_jwt()
    if claims is None:
        return jsonify({'message': 'You are not authorized'}), 401
    transaction = Transaction.query.get_or_404(transaction_id)
    result = TransactionSchema().dump(transaction)
    return jsonify({'transaction': result}), 200

# Update Transaction
@transaction_bp.route('/transaction/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    claims = get_jwt()
    if claims is None:
        return jsonify({'message': 'You are not authorized'}), 401
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.get_json()
    transaction.transaction_number = data['transaction_number']
    transaction.from_account_id = data['from_account_id']
    transaction.to_account_id = data['to_account_id']
    transaction.transaction_type = data['transaction_type']
    transaction.amount = data['amount']
    transaction.update_transaction()
    return jsonify({'message': 'Transaction updated successfully'}), 200

# Delete Transaction
@transaction_bp.route('/transaction/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    claims = get_jwt()
    if claims is None:
        return jsonify({'message': 'You are not authorized'}), 401
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction.delete_transaction()
    return jsonify({'message': 'Transaction deleted successfully'}), 200
