# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.facturacion.models.tipo_cambio_model import TipoCambio

tipo_cambio_grupo_bp = Blueprint('tipo_cambio', __name__)

from .. import bp 

@bp.route('/tipo_cambio')
def tipo_cambio_index():
    result = TipoCambio.get_all()
    
    if result['success']:
        return render_template('/facturacion/tipo_cambio/index.html', list = result['data'])
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/tipo_cambio/create', methods=['GET', 'POST'])
def tipo_cambio_create():    
    if request.method == 'POST':
        try:
            result = TipoCambio.create(request.form)
            flash('tipo_cambio agregado', 'success')
            return redirect(url_for('facturacion.tipo_cambio_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    return render_template('/facturacion/tipo_cambio/create.html')

@bp.route('/tipo_cambio/update/<string:uniqueid>', methods=['GET', 'POST'])
def tipo_cambio_update(uniqueid):    
    if request.method == 'POST':
        try:
            result = TipoCambio.update(request.form)
            return redirect(url_for('facturacion.tipo_cambio_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)

    tipo_cambio = TipoCambio.get_by_uniqueid(uniqueid)
    if result['success']:
        return render_template('/facturacion/tipo_cambio/update.html', 
                               tipo_cambio = tipo_cambio['data'])
    else:
        return render_template('error.html', error = result['error'])    

@bp.route('/tipo_cambio/delete/<string:uniqueid>', methods=['POST'])
def tipo_cambio_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = TipoCambio.delete(uniqueid)
            flash('tipo_cambio eliminado', 'success')
            return redirect(url_for('facturacion.tipo_cambio_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.tipo_cambio_index'))