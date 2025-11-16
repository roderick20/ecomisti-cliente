from flask import Blueprint

bp = Blueprint('task', __name__, template_folder='templates')

from .routes import tarea_routes, tarea_reportpdf_routes