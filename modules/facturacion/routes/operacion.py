# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo


from modules.facturacion.models.operacion_model import Operacion
from modules.facturacion.models.serie_correlativo_model import SerieCorrelativo
from modules.facturacion.models.operacion_configuracion_model import OperacionConfiguracion

from modules.facturacion.models.producto_model import Producto
from modules.facturacion.models.personeria_model import Personeria


from .. import bp 

@bp.route('/operacion')
def operacion_index():
    # Obtener el período actual como fallback
    ahora = datetime.now(ZoneInfo("America/Lima"))
    periodo_actual = ahora.strftime("%m-%Y")  # Ej: "10-2025"

    # Obtener 'periodo' de la URL (query string), o usar el actual si no existe
    periodo = request.args.get('periodo', periodo_actual)

    configuracion = OperacionConfiguracion.get_all()['data']
    resultado = [row for row in configuracion if row.codigo == 'ruc']
    ruc = resultado[0].valor

    try:
        mes, anio = periodo.split('-')
        mes = int(mes)
        anio = int(anio)
        if not (1 <= mes <= 12) or anio < 1900:
            raise ValueError
    except (ValueError, AttributeError):
        # Si el formato es inválido, usar el período actual
        ahora = datetime.now()
        mes = ahora.month
        anio = ahora.year

    result = Operacion.get_all_by_periodo(mes, anio)    
    if result['success']:
        return render_template('/facturacion/operacion/index.html', list = result['data'], periodo = periodo, ruc = ruc)
    else:
        return render_template('error.html', error = result['error'])

@bp.route('/operacion/create', methods=['GET', 'POST'])
def operacion_create():    
    if request.method == 'POST':
        try:
            result = Operacion.create(request.form)
            flash('Producto agregado', 'success')
            return redirect(url_for('facturacion.operacion_index'))
        except Exception as error:
            flash('Error: '+error, 'error')

    serie = SerieCorrelativo.get_all_venta()['data']
    print(serie)
    return render_template('/facturacion/operacion/create.html', serie = serie)

@bp.route('/operacion/search_producto')
def operacion_search_producto():
    q = request.args.get('q', '').strip().lower()
    list = Producto.search(q)['data']
    print(list)
    results = [row_to_dict(row) for row in list]
    return jsonify({"results": results})

@bp.route('/operacion/search_personeria_numero_doc')
def operacion_search_personeria_numero_doc():
    q = request.args.get('q', '').strip().lower()
    print(q)
    list = Personeria.search_by_numero_doc(q)['data']
    print(list)
    return jsonify({"results": list})

@bp.route('/operacion/search_personeria_by_razon_social')
def operacion_search_personeria_by_razon_social():
    q = request.args.get('q', '').strip().lower()
    list = Personeria.search_by_razon_social(q)['data']
    return jsonify({"results": list})

def row_to_dict(row):
    return {
        'id': row.id,
        'text': row.text,
        'codigo': row.codigo,
        'precio_soles': float(row.precio_soles) if row.precio_soles is not None else 0.0,
        'unidad_nombre': row.unidad_nombre
    }