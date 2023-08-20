from flask import request, jsonify

from . import api
from app.models import User


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
    user.commit()
    return jsonify({'message': f"Account created for {username}!"})
