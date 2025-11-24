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

@bp.route('/getplacas', methods=['POST'])
def orden_get_placas():
    print(request)
    if request.method == 'POST':
        try:
            result = OrdenModel.get_placa_personeria_id(request.form)
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

@bp.route('/create', methods=['GET', 'POST'])
def orden_create():  
    #if request.method == 'POST':  
<<<<<<< Updated upstream
    productoGrupo = OrdenModel.getProductoGrupo()
    productos = OrdenModel.getProductos()
    return render_template('/ordenes/orden/create.html', 
                           Transportista = session['nombre'],
                           productoGrupo = productoGrupo, 
                           productos = productos)
=======
    placas = OrdenModel.get_placa_personeria_id(session.get('user_id'))
    return render_template('/ordenes/orden/create.html', 
                           placas = placas)
>>>>>>> Stashed changes

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