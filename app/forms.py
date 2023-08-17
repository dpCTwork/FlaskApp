from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class TransactionForm(FlaskForm):
    merchant = StringField('Merchant', validators=[DataRequired()])
    card = SelectField('Card', choices=['Visa', 'Mastercard', 'American Express', 'Discover'], validators=[DataRequired()])
    purchase_type = RadioField('Purchase Type', choices=['Dining', 'Gas', 'Grocery', 'Entertainment'], validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    enter = SubmitField('Enter Transaction')

    

