# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import db
from modules.facturacion.models.producto_model import Producto
from modules.facturacion.models.producto_unidad_model import ProductoUnidad
from modules.facturacion.models.producto_grupo_model import ProductoGrupo
from modules.facturacion.models.producto_imagen_model import ProductoImagen

producto_grupo_bp = Blueprint('producto', __name__)

from .. import bp 

@bp.route('/producto')
def producto_index():
    result = Producto.get_all()
    
    if result['success']:
        return render_template('/facturacion/producto/index.html', productos = result['data'])
    else:
        return render_template('error.html', error = result['error'])


@bp.route('/producto/create', methods=['GET', 'POST'])
def producto_create():    
    if request.method == 'POST':
        try:
            result = Producto.create(request.form)
            flash('Producto agregado', 'success')
            return redirect(url_for('facturacion.producto_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    producto_grupo = ProductoGrupo.get_all_select()
    producto_unidad = ProductoUnidad.get_all_select()
    if producto_grupo['success']:
        return render_template('/facturacion/producto/create.html', 
                               producto_grupo = producto_grupo['data'],
                               producto_unidad = producto_unidad['data'])
    else:
        return render_template('error.html', error = result['error'])  
    

@bp.route('/producto/update/<string:uniqueid>', methods=['GET', 'POST'])
def producto_update(uniqueid):    
    if request.method == 'POST':
        try:
            result = Producto.update(request.form)
            return redirect(url_for('facturacion.producto_index'))
        except Exception as error:
            print(error)

    producto_grupo = ProductoGrupo.get_all_select()
    producto_unidad = ProductoUnidad.get_all_select()
    print(producto_unidad)
    producto = Producto.get_by_uniqueid(uniqueid)
    imagenes = ProductoImagen.get_all_by_producto_id(producto['data'].id)
    if producto['success']:
        return render_template('/facturacion/producto/update.html', 
                               producto_grupo = producto_grupo['data'],
                               producto_unidad = producto_unidad['data'], 
                               producto = producto['data'], 
                               imagenes = imagenes['data'])
    else:
        return render_template('error.html', error = result['error'])    

@bp.route('/producto/delete/<string:uniqueid>', methods=['POST'])
def producto_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = Producto.delete(uniqueid)
            flash('Producto eliminado', 'success')
            return redirect(url_for('facturacion.producto_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.producto_index'))