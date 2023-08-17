from flask import render_template, g
from . import bp
from app.forms import BSTestForm

from app import app

@bp.route('/')
def home():
    return render_template('index.j2', title='The Budget App')

@bp.route('/budgetform')
def budget_form():
    form = BSTestForm()
    email = form.email
    password = form.password
    textarea = form.textarea
    radios = form.radios
    selects = form.selects
    return render_template('budget_form.j2', title='Budget Form', email=email, password=password, textarea=textarea, radios=radios, selects=selects)
    
    # {{ render_field(form.email, placeholder=form.email.label.text) }}
    #               {{ render_field(form.password, placeholder=form.password.label.text) }}
    #               {{ render_field(form.textarea) }}
    #               {{ render_radio_fields(form.radios) }}
    #               {{ render_field(form.selects) }}
    # return render_template('budget_form.j2', title='Budget Form')



