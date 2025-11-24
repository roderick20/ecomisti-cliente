from flask import Blueprint

bp = Blueprint('orden', __name__, template_folder='templates')

from .routes import orden_routes