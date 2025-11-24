# routes/main.py
from flask import Blueprint, render_template


auth_bp = Blueprint('auth', __name__)

from .. import bp 

@bp.route('/')
def index():    
    return render_template('/auth/main.html')

@bp.route('/error')
def error(error):    
    return render_template('/auth/error.html', error = error)