from flask import request, jsonify

from . import api
from app.models import Transactions, User
from .helpers import token_required



# Get all transactions from all users
@api.route('/transactions/get', methods=['GET'])
@token_required
def api_transactions(user):
    result = []
    transactions = Transactions.query.all()
    for transaction in transactions:
        result.append({
            'id': transaction.id,
            'user_id': transaction.user_id,
            'user': transaction.user.username,
            'merchant': transaction.merchant,
            'card': transaction.card,
            'purchase_type': transaction.purchase_type,
            'purchase_date': transaction.purchase_date,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
        })
    return jsonify(result), 200

# Get a single transaction from across all transactions in database
@api.get('/transactions/get/<transaction_id>')
@token_required
def api_transaction(user, transaction_id):
    transaction = Transactions.query.filter_by(id=transaction_id).first()
    if transaction:
        return jsonify({
            'id': transaction.id,
            'user_id': transaction.user_id,
            'user': transaction.user.username,
            'merchant': transaction.merchant,
            'card': transaction.card,
            'purchase_type': transaction.purchase_type,
            'purchase_date': transaction.purchase_date,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
        })
    return jsonify({'message': 'Transaction not found.'}), 404

# Get all transactions from a specific user
@api.get('/transactions/get/users/<username>')
@token_required
def api_user_transactions(user, username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify([{
            'id': transaction.id,
            'user_id': transaction.user_id,
            'username': transaction.user.username,
            'merchant': transaction.merchant, 
            'card': transaction.card,
            'purchase_type': transaction.purchase_type,
            'purchase_date': transaction.purchase_date,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
            } for transaction in user.transactions])
    return jsonify({'message': 'User not found.'}), 404

# Get a single transaction from a specific user
@api.get('/transactions/get/users/<username>/<transaction_id>')
@token_required
def api_user_transaction(user, username, transaction_id):
    user = User.query.filter_by(username=username).first()
    if user:
        transaction = Transactions.query.filter_by(id=transaction_id).first()
        if transaction:
            return jsonify({
                'id': transaction.id,
                'user_id': transaction.user_id,
                'user': transaction.user.username,
                'merchant': transaction.merchant,
                'card': transaction.card,
                'purchase_type': transaction.purchase_type,
                'purchase_date': transaction.purchase_date,
                'amount': transaction.amount,
                'timestamp': transaction.timestamp
            })
        return jsonify({'message': 'Transaction not found.'}), 404
    return jsonify({'message': 'User not found.'}), 404

    
# Add a new transaction 
@api.post('/transactions/add')
@token_required
def api_add_transaction(user):
    # Receive their post data
    content = request.get_json()

    # Create a transaction instance
    # Add foreign key to user_id
    transaction = Transactions(
        user_id=user.user_id,
        merchant=content['merchant'],
        card=content['card'],
        purchase_type=content['purchase_type'],
        purchase_date=content['purchase_date'],
        amount=content['amount'],
    )
    
    transaction.add()
    return jsonify({'message': f'Transaction added!'}), 201

# Update a transaction by ID
@api.put('/transactions/update/<transaction_id>')
@token_required
def api_update_transaction(user, transaction_id):
    transaction = Transactions.query.filter_by(id=transaction_id).first()
    if transaction:
        try:
            transaction_info = request.get_json()
            transaction.merchant = transaction_info['merchant']
            transaction.card = transaction_info['card']
            transaction.purchase_type = transaction_info['purchase_type']
            transaction.purchase_date = transaction_info['purchase_date']
            transaction.amount = transaction_info['amount']
            transaction.add()
            return jsonify({'message': f'Transaction successfully updated for {user.first_name.title()} {user.last_name.title()}!'}), 200
        except:
            return jsonify({'message': 'Invalid entry. Transaction not updated.'}), 400
    return jsonify({'message': 'Transaction not found.'}), 404

# Delete a transaction from database by transaction ID
@api.delete('/transactions/delete/<transaction_id>')
@token_required
def api_delete_transaction(user, transaction_id):
    transaction = Transactions.query.filter_by(id=transaction_id).first()
    if transaction:
        transaction.delete()
        return jsonify({'message': f'Transaction deleted!'}), 200
    return jsonify({'message': 'Transaction not found.'}), 404


