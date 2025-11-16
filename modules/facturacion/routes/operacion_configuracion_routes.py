# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from modules.facturacion.models.operacion_configuracion_model import OperacionConfiguracion

from .. import bp 

@bp.route('/operacion_configuracion')
def operacion_configuracion_index():
    result = OperacionConfiguracion.get_all()    

    resultado = [row for row in result['data'] if row.codigo == 'ruc']

    print(resultado[0].valor)
    if result['success']:
        return render_template('/facturacion/operacion_configuracion/index.html', list = result['data'])
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/operacion_configuracion/create', methods=['GET', 'POST'])
def operacion_configuracion_create():    
    if request.method == 'POST':
        try:
            result = OperacionConfiguracion.create(request.form)
            flash('Producto agregado', 'success')
            return redirect(url_for('facturacion.operacion_configuracion_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    return render_template('/facturacion/operacion_configuracion/create.html')

@bp.route('/operacion_configuracion/update/<string:uniqueid>', methods=['GET', 'POST'])
def operacion_configuracion_update(uniqueid):    
    if request.method == 'POST':
        try:
            result = OperacionConfiguracion.update(request.form)
            return redirect(url_for('facturacion.operacion_configuracion_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)

    configuracion = OperacionConfiguracion.get_by_uniqueid(uniqueid)

    if configuracion['success']:
        return render_template('/facturacion/operacion_configuracion/update.html',
                               configuracion = configuracion['data'])
    else:
        return render_template('error.html', error = configuracion['error'])    

@bp.route('/operacion_configuracion/delete/<string:uniqueid>', methods=['POST'])
def operacion_configuracion_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = OperacionConfiguracion.delete(uniqueid)
            flash('Producto eliminado', 'success')
            return redirect(url_for('facturacion.operacion_configuracion_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.operacion_configuracion_index'))