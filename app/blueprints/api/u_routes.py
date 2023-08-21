from flask import request, jsonify

from . import api
from app.models import User
from .helpers import token_required


# Verify User
@api.route('/verify', methods=['POST']) # POST request to /api/verify
# @api.post('/verify') also works exactly the same
def verify():
    credentials = request.get_json()
    username = credentials['username']
    password = credentials['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if user.check_password(password):
            return jsonify({'user token': user.token}), 200
        return jsonify({'message': 'Incorrect password.'}), 400
    return jsonify({'message': 'User not found.'}), 404

# Register User
@api.post('/register')
def register():
    user_info = request.get_json()
    first_name = user_info['first_name']
    last_name = user_info['last_name']
    username = user_info['username']
    email = user_info['email']
    password = user_info['password']
    u_username = User.query.filter_by(username=username).first()
    if u_username:
        return jsonify({'message': 'Username already exists.'}), 400
    u_email = User.query.filter_by(email=email).first()
    if u_email:
        return jsonify({'message': 'Email already exists.'}), 400
    user = User(first_name=first_name, last_name=last_name, username=username, email=email)
    setattr(user, 'password', user.hash_password(password))
    user.add_token()
    user.add()
    return jsonify({'message': f"Account created for {username}!"})

# Update user info for a specified user_id
@api.put('/users/update/<user_id>')
@token_required
def api_update_user(user, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        try:
            user_info = request.get_json()
            user.first_name = user_info['first_name']
            user.last_name = user_info['last_name']
            user.username = user_info['username']
            user.email = user_info['email']
            user.add()
            return jsonify({'message': f'User successfully updated for {user.first_name.title()} {user.last_name.title()}!'}), 200
        except:
            return jsonify({'message': 'Invalid entry. User not updated.'}), 400
    return jsonify({'message': 'User not found.'}), 404

# Delete a user from the database by username
@api.delete('users/delete/<user_id>')
@token_required
def api_delete_user(user, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        user.delete()
        return jsonify({'message': f'User deleted!'}), 200
    return jsonify({'message': 'User not found.'}), 404