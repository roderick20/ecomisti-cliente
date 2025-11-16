from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

from .routes import auth_routes, main_routes, usuario_routes