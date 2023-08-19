from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class TransactionForm(FlaskForm):
    merchant = StringField('Merchant', validators=[DataRequired()], render_kw={'placeholder': 'e.g. Starbucks'})
    card = SelectField('Card', choices=['Visa', 'Mastercard', 'American Express'], validators=[DataRequired()])
    purchase_type = SelectField('Purchase Type', choices=[('dining', 'Dining'), ('gas', 'Gas'), ('grocery', 'Grocery'), ('entertainment', 'Entertainment')], validators=[DataRequired()])
    purchase_date = DateField('Date of Transaction', validators=[DataRequired()])
    amount = DecimalField('Transaction Amount', places=2, validators=[DataRequired()], render_kw={'placeholder': '0.00'})
    submit = SubmitField('Enter')

    

