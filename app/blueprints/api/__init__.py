from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from app.blueprints.api import t_routes, u_routes