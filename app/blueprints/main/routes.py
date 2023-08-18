from flask import render_template, g, redirect, url_for, flash
from flask_login import current_user, login_required
from . import bp

from app.models import Transactions, User
from app.forms import TransactionForm

from app import app

@bp.route('/')
def home():
    return render_template('index.j2', title='The Budget App')

@bp.route('/budgetform', methods=['GET', 'POST'])
@login_required
def budget_form():
    form = TransactionForm()
    if form.validate_on_submit():
        t = Transactions(merchant=form.merchant.data, card=form.card.data, purchase_type=form.purchase_type.data, purchase_date=form.purchase_date.data, amount=form.amount.data)
        t.commit()
        flash(f'Transaction added for {form.merchant.data}!', 'success')
        return redirect(url_for('main.budget_form', username=current_user.username))
    return render_template('/user_menu/budget_form.j2', title='Budget Form', form=form)   

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
# We can use hyphen instead of underscore because this is just an endpoint that we're specifying to access a user's page.
def transactions():
    # We're going to query the database for the user's posts.
    # We'll use the filter_by() method to filter the posts by the user's username.
    # Can also query by user_id, email, etc.
    user = User.query.filter_by(username=current_user.username).first()
    first_name = User.query.filter_by(username=current_user.username).first().first_name
    return render_template('/user_menu/transactions.j2', title=f"{first_name}'s Transactions", user=user)




