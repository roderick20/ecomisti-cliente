# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import db
from modules.facturacion.models.serie_correlativo_model import SerieCorrelativo


seriel_correlativo_grupo_bp = Blueprint('serie_correlativo', __name__)

from .. import bp 

@bp.route('/serie_correlativo')
def serie_correlativo_index():
    result = SerieCorrelativo.get_all()
    
    if result['success']:
        return render_template('/facturacion/serie_correlativo/index.html', list = result['data'])
    else:
        return render_template('error.html', error = result['error'])


@bp.route('/serie_correlativo/create', methods=['GET', 'POST'])
def serie_correlativo_create():    
    if request.method == 'POST':
        try:
            result = SerieCorrelativo.create(request.form)
            flash('serie_correlativo agregado', 'success')
            return redirect(url_for('facturacion.serie_correlativo_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    return render_template('/facturacion/serie_correlativo/create.html')    

@bp.route('/serie_correlativo/delete/<string:uniqueid>', methods=['POST'])
def serie_correlativo_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = SerieCorrelativo.delete(uniqueid)
            flash('serie_correlativo eliminado', 'success')
            return redirect(url_for('facturacion.serie_correlativo_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.serie_correlativo_index'))