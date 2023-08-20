from flask import request, jsonify

from . import api
from app.models import Transactions, User
from .helpers import token_required


# Get all transactions from all users
@api.route('/transactions', methods=['GET'])
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

# Get a single transaction from across all users in database
@api.get('/transactions/<transaction_id>')
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
@api.get('/transactions/<username>')
@token_required
def api_user_transactions(user, username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify([{
            'id': transaction.id,
            'user_id': transaction.user_id,
            'user': transaction.user.username,
            'merchant': transaction.merchant, 
            'card': transaction.card,
            'purchase_type': transaction.purchase_type,
            'purchase_date': transaction.purchase_date,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
            } for transaction in user.transactions])
    return jsonify({'message': 'User not found.'}), 404

# Get a single transaction from a specific user
@api.get('/transactions/<username>/<transaction_id>')
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

# Add a new transaction for a specific user

@api.post('/transactions/')
@token_required
def api_add_transaction(current_user):
    try:
        transaction_info = request.get_json()
        merchant = transaction_info['merchant']
        card = transaction_info['card']
        purchase_type = transaction_info['purchase_type']
        purchase_date = transaction_info['purchase_date']
        amount = transaction_info['amount']
        transaction = Transactions(merchant=merchant, card=card, purchase_type=purchase_type, purchase_date=purchase_date, amount=amount, user_id=current_user.user_id)
        transaction.commit()
        return jsonify({'message': f'Transaction added for {current_user.username}!'}), 201
    except:
        return jsonify({'message': 'Invalid entry. Transaction not added.'}), 400

# Delete a transaction from a specific user

@api.delete('/transactions/<transaction_id>')
@token_required
def api_delete_transaction(current_user, transaction_id):
    transaction = Transactions.query.filter_by(id=transaction_id).first()
    if transaction:
        transaction.delete()
        return jsonify({'message': f'Transaction deleted for {current_user.username}!'}), 200
    return jsonify({'message': 'Transaction not found.'}), 404

# Update a transaction from a specific user
@api.route('/transactions/<transaction_id>', methods=['POST', 'PUT'])
@token_required
def api_update_transaction(current_user, transaction_id):
    transaction = Transactions.query.filter_by(id=transaction_id).first()
    if transaction:
        try:
            transaction_info = request.get_json()
            transaction.merchant = transaction_info['merchant']
            transaction.card = transaction_info['card']
            transaction.purchase_type = transaction_info['purchase_type']
            transaction.purchase_date = transaction_info['purchase_date']
            transaction.amount = transaction_info['amount']
            transaction.commit()
            return jsonify({'message': f'Transaction successfully updated for {current_user.first_name.title()} {current_user.last_name.title()}!'}), 200
        except:
            return jsonify({'message': 'Invalid entry. Transaction not updated.'}), 400
    return jsonify({'message': 'Transaction not found.'}), 404