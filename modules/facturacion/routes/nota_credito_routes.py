# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

from modules.facturacion.models.nota_credito_model import NotaCredito
from modules.facturacion.models.serie_correlativo_model import SerieCorrelativo

from .. import bp 

@bp.route('/nota_credito/create', methods=['GET', 'POST'])
def nota_credito_create():    
    if request.method == 'POST':
        try:
            result = NotaCredito.create(request.form)
            flash('Producto agregado', 'success')
            return redirect(url_for('facturacion.operacion_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    serie = SerieCorrelativo.get_all_venta()['data']
    print(serie)
    return render_template('/facturacion/nota_credito/create.html', serie = serie)
