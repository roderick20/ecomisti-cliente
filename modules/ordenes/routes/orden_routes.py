# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session

from modules.ordenes.models.orden_model import OrdenModel
from datetime import date
#task_bp = Blueprint('task', __name__)

from .. import bp 

@bp.route('/orden')
def orden_list():
    return render_template('/ordenes/orden/index.html')

@bp.route('/getdatatable', methods=['POST'])
def orden_get_table():
    if request.method == 'POST':
        try:
            result = OrdenModel.get_table(request.form)
            return jsonify(result)             
        except Exception as error:
            print(error)

@bp.route('/getordenservices/<string:uniqueid>', methods=['GET'])
def orden_getordenservices(uniqueid):   
    try:
        result = OrdenModel.get_ordenservice_by_uniqueid(uniqueid)
        return jsonify(result)             
    except Exception as error:
        print(error)

@bp.route('/addservice', methods=['POST'])
def orden_addservice():
    try:
        result = OrdenModel.addservice(request.form)

        return jsonify(result)             
    except Exception as error:
        print(error)

@bp.route('/adddireccion', methods=['POST'])
def orden_adddireccion():
    try:
        result = OrdenModel.addDireccion(request.form)

        return jsonify(result)             
    except Exception as error:
        print(error)

@bp.route('/getdirecciones', methods=['POST'])
def orden_get_direcciones():   
    cliente_id = request.form.get('clienteId')
    try:
        result = OrdenModel.get_direccion_personeria_id(cliente_id)
        return jsonify(result)             
    except Exception as error:
        print(error)

@bp.route('/delete/<string:ordenUniqueId>/<string:servicioUniqueId>', methods=['GET'])
def orden_delete(ordenUniqueId,servicioUniqueId):  
    OrdenModel.servicio_delete(servicioUniqueId)
    return redirect(url_for('orden.orden_update', uniqueid=ordenUniqueId))

@bp.route('/remove', methods=['GET', 'POST'])
def orden_create():  
    if request.method == 'POST':  
        result = OrdenModel.create(request.form)
        return redirect(url_for('.orden_list'))
    placas = OrdenModel.get_placa_personeria_id(session.get('user_id'))
    return render_template('/ordenes/orden/create.html', placas = placas)

@bp.route('/update/<string:uniqueid>', methods=['GET', 'POST'])
def orden_update(uniqueid):  
    result = OrdenModel.get_orden_by_uniqueid(uniqueid)
    ubicaciones = OrdenModel.get_ubicacion()
    return render_template('/ordenes/orden/update.html', order = result, ubicaciones = ubicaciones['data'])

@bp.route('/searchclient')
def search_client():
    search_term = request.args.get('q', '')
    
    # Llamar al método estático (ajustado más abajo)
    result = OrdenModel.searchPersoneria(search_term)
    
    # Convertir resultados a formato esperado por Select2 o similar
    results = [
        {
            'id': row['PersoneriaID'],
            'text': row['Personeria']
        }
        for row in result
    ]
    
    return jsonify({
        'results': results,
        'pagination': {'more': False}
    })


# @bp.route('/task/update/<string:uniqueid>', methods=['GET', 'POST'])
# def task_update(uniqueid):    
#     if request.method == 'POST':
#         try:
#             result = TareaModel.update(request.form)
#             return redirect(url_for('task.task_index'))
#         except Exception as error:
#             print(error)
#     tarea = TareaModel.get_by_uniqueid(uniqueid)
#     if tarea['success']:
#         return render_template('/task/tarea/update.html', tarea = tarea['data'])
#     else:
#         return render_template('error.html', error = result['error'])
    
# @bp.route('/task/update_estado', methods=['POST'])
# def task_update_estado():    
#     try:
#         result = TareaModel.update_estado(request.form)
#         return redirect(url_for('task.task_index'))
#     except Exception as error:
#         print(error)

# @bp.route('/producto/delete/<string:uniqueid>', methods=['POST'])
# def task_delete(uniqueid):
#     if request.method == 'POST':
#         try:
#             result = TareaModel.delete(uniqueid)
#             flash('Producto eliminado', 'success')
#             return redirect(url_for('task.task_index'))
#         except Exception as error:
#             flash('Error: ' + error, 'error')
#             return redirect(url_for('task.task_index'))