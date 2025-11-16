# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import db
from modules.facturacion.models.producto_grupo_model import ProductoGrupo

producto_grupo_bp = Blueprint('producto_grupo', __name__)

from .. import bp 

@bp.route('/producto_grupo')
def producto_grupo_index():
    result = ProductoGrupo.get_all()
    if result['success']:
        return render_template('/facturacion/producto_grupo/index.html', producto_grupo = result['data'])
    else:
        return render_template('error.html', error = result['error'])


@bp.route('/producto_grupo/create', methods=['GET', 'POST'])
def producto_grupo_create():
    if request.method == 'POST':
        try:
            # if parent_id == '':
            #     parent_id = None
            # else:
            #     try:
            #         parent_id = int(parent_id)
            #     except (ValueError, TypeError):
            #         parent_id = None

            # print(nombre)
            # print(parent_id)
            result = ProductoGrupo.create(request.form)
            return redirect(url_for('facturacion.producto_grupo_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)
    result = ProductoGrupo.get_all_select()
    if result['success']:
        return render_template('/facturacion/producto_grupo/create.html', producto_grupo = result['data'])
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/producto_grupo/update/<string:uniqueid>', methods=['GET', 'POST'])
def producto_grupo_update(uniqueid):
    if request.method == 'POST':
        try:
            result = ProductoGrupo.update(request.form)
            return redirect(url_for('facturacion.producto_grupo_index'))
        except Exception as error:
            return render_template('error.html', error = result['error'])
    parents = ProductoGrupo.get_all_select()
    grupo = ProductoGrupo.get_by_uniqueid(uniqueid)
    print(grupo['data'])
    if grupo['success']:
        return render_template('/facturacion/producto_grupo/update.html', 
                               parents = parents['data'],
                               grupo = grupo['data'])
    else:
        return render_template('error.html', error = result['error'])
        
@bp.route('/producto_grupo/delete/<string:uniqueid>', methods=['POST'])
def producto_grupo_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = ProductoGrupo.delete(uniqueid)
            flash('Producto eliminado', 'success')
            return redirect(url_for('facturacion.producto_grupo_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.producto_grupo_index'))

   