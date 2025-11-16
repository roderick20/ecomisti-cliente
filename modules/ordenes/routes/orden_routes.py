# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from modules.ordenes.models.orden_model import OrdenModel
from datetime import date
#task_bp = Blueprint('task', __name__)

from .. import bp 

@bp.route('/orden')
def orden_list():
    return render_template('/ordenes/orden/index.html')
    # result = TareaModel.get_all()    
    # print('task_index')
    # print(result)
    # if result['success']:
    #     return render_template('/task/tarea/index.html', tareas = result['data'], hoy=date.today())
    # else:
    #     return render_template('error.html', error = result['error'])

@bp.route('/getdatatable', methods=['POST'])
def orden_get_table():
    if request.method == 'POST':
        try:
            result = OrdenModel.get_table(request.form)
            return jsonify(result) 
            
        except Exception as error:
            print(error)




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