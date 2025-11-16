# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import db
from modules.facturacion.models.tabla_general_model import TablaGeneral

tabla_general_bp = Blueprint('tabla_general', __name__)

from .. import bp 

@bp.route('/tabla_general')
def tabla_general_index():
    result = TablaGeneral.get_all()
    print(result)
    if result['success']:
        return render_template('/facturacion/tabla_general/index.html', tabla_general = result['data'])
    else:
        return render_template('error.html', error = result['error'])


@bp.route('/tabla_general/create', methods=['GET', 'POST'])
def tabla_general_create():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            parent_id = request.form.get('parent_id', '').strip()
            # if parent_id == '':
            #     parent_id = None
            # else:
            #     try:
            #         parent_id = int(parent_id)
            #     except (ValueError, TypeError):
            #         parent_id = None

            # print(nombre)
            # print(parent_id)
            result = TablaGeneral.create(nombre, parent_id)
            return redirect(url_for('facturacion.tabla_general_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)
    result = TablaGeneral.get_all_select()
    if result['success']:
        return render_template('/facturacion/tabla_general/create.html', tabla_general_parent = result['data'])
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/tabla_general/update', methods=['GET', 'POST'])
def tabla_general_update():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            parent_id = request.form.get('parent_id', '').strip()
            # if parent_id == '':
            #     parent_id = None
            # else:
            #     try:
            #         parent_id = int(parent_id)
            #     except (ValueError, TypeError):
            #         parent_id = None

            # print(nombre)
            # print(parent_id)
            result = TablaGeneral.create(nombre, parent_id)
            return redirect(url_for('facturacion.tabla_general_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)
    result = TablaGeneral.get_all_select()
    if result['success']:
        return render_template('/facturacion/tabla_general/create.html', tabla_general = result['data'])
    else:
        return render_template('error.html', error = result['error'])
        


   