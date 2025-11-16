from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from config import Config
from models import get_db_connection, allowed_file, get_current_user

from database import db

task_bp = Blueprint('task', __name__)

@task_bp.context_processor
def inject_user():
    return dict(current_user=get_current_user(session))

@task_bp.route('/tarea/nueva/<int:sprint_id>/<int:proyecto_id>', methods=['GET', 'POST'])
def nueva_tarea(sprint_id, proyecto_id):
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            prioridad = request.form['prioridad']
            fecha_termino = request.form['fecha_termino']
            asignado_id = request.form.get('asignado_id') or None
            user_id = session['user_id']
            
            archivo_nombre = None
            if 'archivo' in request.files:
                archivo = request.files['archivo']
                if archivo and archivo.filename != '' and allowed_file(archivo.filename):
                    filename = secure_filename(archivo.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    archivo.save(os.path.join(Config.UPLOAD_FOLDER, unique_filename))
                    archivo_nombre = unique_filename
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tareas (titulo, descripcion, sprint_id, asignado_id, estado, prioridad, 
                                archivo_adjunto, creado_id, editado_id,fecha_termino) 
                VALUES (%s, %s, %s, %s, 'abierta', %s, %s, %s, %s, %s)
            """, (titulo, descripcion, sprint_id, asignado_id, prioridad, archivo_nombre, user_id, user_id, fecha_termino))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Tarea creada exitosamente', 'success')
            # return redirect(url_for('main.index'))
            return redirect(url_for('project.proyecto_detlle', proyecto_id=proyecto_id))
        except KeyError as e:
            # Error si falta un campo en el formulario
            flash(f'Error: campo requerido no enviado ({str(e)})', 'danger')
            return render_template('nuevo_proyecto.html')

        except Exception as e:
            # Cualquier otro error (base de datos, conexión, etc.)
            flash(f'Error al crear el proyecto: {str(e)}', 'danger')
            # Opcional: loggear el error real en un archivo para debugging
            print(f"[ERROR] nuevo_proyecto: {e}")  # En producción usa logging
            return render_template('nuevo_proyecto.html')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.nombre as sprint_nombre, p.nombre as proyecto_nombre 
        FROM sprints s 
        JOIN proyectos p ON s.proyecto_id = p.id 
        WHERE s.id = %s
    """, (sprint_id,))
    info = cursor.fetchone()
    
    cursor.execute("SELECT id, nombre, username FROM usuarios WHERE activo = TRUE ORDER BY nombre")
    usuarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('nueva_tarea.html', info=info, sprint_id=sprint_id, usuarios=usuarios)

# http://127.0.0.1:5000/tarea/11/estado/cerrada/6
@task_bp.route('/tarea/<int:tarea_id>/estado/<nuevo_estado>/<int:proyecto_id>')
def cambiar_estado_tarea(tarea_id, nuevo_estado, proyecto_id):
    if nuevo_estado not in ['abierta', 'cancelada', 'cerrada']:
        flash('Estado no válido', 'error')
        # return redirect(url_for('main.index'))
        return redirect(url_for('task.mis_tareas'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas SET estado = %s, editado = NOW(), editado_id = %s 
        WHERE id = %s
    """, (nuevo_estado, user_id, tarea_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Tarea marcada como {nuevo_estado}', 'success')
    #return redirect(url_for('main.index'))
    return redirect(url_for('task.mis_tareas'))

@task_bp.route('/tarea/<int:tarea_id>/asignar/<int:usuario_id>/<int:proyecto_id>')
def asignar_tarea(tarea_id, usuario_id, proyecto_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    
    if not usuario:
        flash('Usuario no encontrado', 'error')
        # return redirect(url_for('main.index'))
        return redirect(url_for('project.proyecto_detlle', proyecto_id=proyecto_id))
    
    cursor.execute("""
        UPDATE tareas SET asignado_id = %s, editado = NOW(), editado_id = %s 
        WHERE id = %s
    """, (usuario_id, user_id, tarea_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Tarea asignada a {usuario["nombre"]}', 'success')
    # return redirect(url_for('main.index'))
    return redirect(url_for('project.proyecto_detlle', proyecto_id=proyecto_id))

@task_bp.route('/tarea/<int:tarea_id>/desasignar')
def desasignar_tarea(tarea_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas SET asignado_id = NULL, editado = NOW(), editado_id = %s 
        WHERE id = %s
    """, (user_id, tarea_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Tarea desasignada', 'success')
    return redirect(url_for('main.index'))

@task_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@task_bp.route('/tarea/<int:tarea_id>')
def ver_tarea(tarea_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, s.nombre as sprint_nombre, p.nombre as proyecto_nombre,
               ua.nombre as asignado_nombre, ua.username as asignado_username,
               uc.nombre as creado_por_nombre, ue.nombre as editado_por_nombre,
               t.creado, t.editado
        FROM tareas t
        JOIN sprints s ON t.sprint_id = s.id
        JOIN proyectos p ON s.proyecto_id = p.id
        LEFT JOIN usuarios ua ON t.asignado_id = ua.id
        LEFT JOIN usuarios uc ON t.creado_id = uc.id
        LEFT JOIN usuarios ue ON t.editado_id = ue.id
        WHERE t.id = %s
    """, (tarea_id,))
    tarea = cursor.fetchone()
    
    cursor.execute("SELECT id, nombre, username FROM usuarios WHERE activo = TRUE ORDER BY nombre")
    usuarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not tarea:
        flash('Tarea no encontrada', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('ver_tarea.html', tarea=tarea, usuarios=usuarios)

@task_bp.route('/mis-tareas')
def mis_tareas():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT t.*, s.nombre as sprint_nombre, p.nombre as proyecto_nombre,
               uc.nombre as creado_por_nombre, p.id as proyecto_id
        FROM tareas t
        JOIN sprints s ON t.sprint_id = s.id
        JOIN proyectos p ON s.proyecto_id = p.id
        LEFT JOIN usuarios uc ON t.creado_id = uc.id
        WHERE t.asignado_id = %s
        ORDER BY t.prioridad = 'urgente' DESC, t.creado DESC
    """, (user_id,))
    tareas = cursor.fetchall()
    
    cursor.close()
    conn.close()

    tareas_abiertas = [t for t in tareas if t.get('estado') == 'abierta']
    
    return render_template('mis_tareas.html', tareas=tareas, tareas_abiertas =tareas_abiertas)

@task_bp.route('/edit/task/<int:task_id>/project/<int:project_id>', methods=['GET', 'POST'])
def edit(task_id, project_id):
    if request.method == 'POST':
        try:
            id = request.form['id']
            project_id = request.form['project_id']
            titulo = request.form['titulo']
            asignado_id = request.form['asignado_id']
            fecha_termino = request.form['fecha_termino']
            
            query = """
                UPDATE tareas SET titulo = %s, asignado_id = %s, fecha_termino = %s WHERE id = %s
            """

            db.execute(query, (titulo, asignado_id, fecha_termino, id))
           
            return redirect(url_for('project.proyecto_detlle', proyecto_id = project_id))
        except Exception as error:
            return render_template('error.html', error = error)

    try:
        query = """
            SELECT t.*, s.nombre as sprint_nombre, p.nombre as proyecto_nombre,
                ua.nombre as asignado_nombre, ua.username as asignado_username,
                uc.nombre as creado_por_nombre, ue.nombre as editado_por_nombre,
                t.creado, t.editado
            FROM tareas t
            JOIN sprints s ON t.sprint_id = s.id
            JOIN proyectos p ON s.proyecto_id = p.id
            LEFT JOIN usuarios ua ON t.asignado_id = ua.id
            LEFT JOIN usuarios uc ON t.creado_id = uc.id
            LEFT JOIN usuarios ue ON t.editado_id = ue.id
            WHERE t.id = %s
        """
        task = db.query(query, (task_id,))
        print(task[0])

        users = db.query("SELECT id, nombre, username FROM usuarios WHERE activo = TRUE ORDER BY nombre")

        return render_template('task/edit.html', task = task[0], users = users, project_id = project_id)
    
    except Exception as error:
        return render_template('error.html', error = error)