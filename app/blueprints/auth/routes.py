from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User

from . import bp
from app.forms import SignupForm, LoginForm

@bp.route('/signup', methods=['GET', 'POST'])
# By default, the route decorate only allows 'GET' requests. So we have to add 'POST' to the list of methods.
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignupForm()
    if form.validate_on_submit():
        # We will add the database code here later
        # For now, we'll just flash a message with flash()
        username = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not email and not username:
            u = User(username=form.username.data, email=form.email.data, password=form.password.data)
            u.password = u.hash_password(form.password.data)
            u.add_token()
            u.commit()
            flash(f'Account created for {form.username.data}! You can now log in.', 'success')
            return redirect(url_for('main.home'))
        if username:
            flash(f'Username {username} already exists. Please choose another username.', 'warning')
        elif email:
            flash(f'Email {form.email.data} already exists. Please choose another email.', 'warning')
    return render_template('/auth_templates/signup.j2', title='Sign Up', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            flash(f"Welcome, {form.username.data}!", 'success')
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash(f"User {form.username.data} doesn't exist or the password is incorrect.", 'danger')
    return render_template('login.j2', title='Log In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))