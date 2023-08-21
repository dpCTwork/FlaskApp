from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from secrets import token_urlsafe
from datetime import datetime

from app import db, login

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    # User table for this app will have the following columns:
    # user_id, username, email, and password
    # The user_id is the primary key, which means it is the unique identifier for each user
    user_id = db.Column(db.Integer, primary_key=True)
    # Set the username and email to be unique.
    # The unique=True means that the username/email must be unique. No two users can have the same username/email.
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    token = db.Column(db.String(250), unique=True)
    transactions = db.relationship('Transactions', backref='user', lazy=True)

    def __repr__(self):
        # This is the string representation of the User object.
        # This is what will be returned when we query the database for a User object.
        return f'User: {self.username}'
    
    def commit(self):
        # This is a method that commits the User object to the database.
        # We will call this method in our routes.py file.
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        # This method will hash the password
        return generate_password_hash(password)
    
    def check_password(self, password):
        # This method will check the password
        return check_password_hash(self.password, password)
    
    def add_token(self):
        # This method will add a token to the database
        # We will call this method in our routes.py file.
        
        setattr(self, 'token', token_urlsafe(32))


    def get_id(self):
        return str(self.user_id)
        
    
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    merchant = db.Column(db.String(250))
    card = db.Column(db.String(250))
    purchase_type = db.Column(db.String(250))
    purchase_date = db.Column(db.Date)
    amount = db.Column(db.Numeric(6, 2))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Transaction: A {self.card} purchase of ${self.amount} at {self.merchant} on {self.purchase_date} has been added.'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()