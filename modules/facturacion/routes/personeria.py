# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from modules.facturacion.models.personeria_model import Personeria

from .. import bp 

@bp.route('/personeria')
def personeria_index():
    result = Personeria.get_all()    
    if result['success']:
        return render_template('/facturacion/personeria/index.html', list = result['data'])
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/personeria/create', methods=['GET', 'POST'])
def personeria_create():    
    if request.method == 'POST':
        try:
            result = Personeria.create(request.form)
            flash('Producto agregado', 'success')
            return redirect(url_for('facturacion.personeria_index'))
        except Exception as error:
            flash('Error: '+error, 'error')
    return render_template('/facturacion/personeria/create.html')

@bp.route('/personeria/update/<string:uniqueid>', methods=['GET', 'POST'])
def personeria_update(uniqueid):    
    if request.method == 'POST':
        try:
            result = Personeria.update(request.form)
            return redirect(url_for('facturacion.personeria_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)

    return render_template('/facturacion/personeria/update.html')


@bp.route('/personeria/delete/<string:uniqueid>', methods=['POST'])
def personeria_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = Personeria.delete(uniqueid)
            flash('Producto eliminado', 'success')
            return redirect(url_for('facturacion.personeria_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.personeria_index'))