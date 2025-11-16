# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from modules.facturacion.models.producto_unidad_model import ProductoUnidad

from .. import bp 

@bp.route('/producto_unidad')
def producto_unidad_index():
    result = ProductoUnidad.get_all()
    
    if result['success']:
        return render_template('/facturacion/producto_unidad/index.html', list = result['data'])
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/producto_unidad/create', methods=['GET', 'POST'])
def producto_unidad_create():    
    if request.method == 'POST':
        try:
            result = ProductoUnidad.create(request.form)
            flash('Producto agregado', 'success')
            return redirect(url_for('facturacion.producto_unidad_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    return render_template('/facturacion/producto_unidad/create.html')

@bp.route('/producto_unidad/update/<string:uniqueid>', methods=['GET', 'POST'])
def producto_unidad_update(uniqueid):    
    if request.method == 'POST':
        try:
            result = ProductoUnidad.update(request.form)
            return redirect(url_for('facturacion.producto_unidad_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)

    producto = ProductoUnidad.get_by_uniqueid(uniqueid)

    if producto['success']:
        return render_template('/facturacion/producto_unidad/update.html',
                               producto = producto['data'])
    else:
        return render_template('error.html', error = producto['error'])    

@bp.route('/producto_unidad/delete/<string:uniqueid>', methods=['POST'])
def producto_unidad_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = ProductoUnidad.delete(uniqueid)
            flash('Producto eliminado', 'success')
            return redirect(url_for('facturacion.producto_unidad_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.producto_unidad_index'))