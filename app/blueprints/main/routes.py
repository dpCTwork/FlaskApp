from flask import render_template, g
from . import bp

from app import app

@bp.route('/')
def home():
    return render_template('index.j2', title='The Budget App')



