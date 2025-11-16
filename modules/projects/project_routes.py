from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import get_db_connection, get_current_user

project_bp = Blueprint('project', __name__)

@project_bp.context_processor
def inject_user():
    return dict(current_user=get_current_user(session))


@project_bp.route('/proyecto/nuevo', methods=['GET', 'POST'])
def nuevo_proyecto():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            user_id = session.get('user_id')  # Usa .get() para evitar KeyError
            
            if not user_id:
                flash('Debes iniciar sesión para crear un proyecto.', 'danger')
                return redirect(url_for('auth.login'))

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proyectos (nombre, estado, creado_id, editado_id) 
                VALUES (%s, 'abierto', %s, %s)
            """, (nombre, user_id, user_id))
            conn.commit()
            cursor.close()
            conn.close()

            flash('Proyecto creado exitosamente', 'success')
            return redirect(url_for('main.index'))

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

    return render_template('nuevo_proyecto.html')

@project_bp.route('/proyecto/<int:proyecto_id>/toggle_estado')
def toggle_proyecto_estado(proyecto_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT estado FROM proyectos WHERE id = %s", (proyecto_id,))
    estado_actual = cursor.fetchone()[0]
    nuevo_estado = 'cerrado' if estado_actual == 'abierto' else 'abierto'
    
    cursor.execute("""
        UPDATE proyectos SET estado = %s, editado = NOW(), editado_id = %s 
        WHERE id = %s
    """, (nuevo_estado, user_id, proyecto_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Proyecto {nuevo_estado} exitosamente', 'success')
    # return redirect(url_for('main.index'))
    return redirect(url_for('project.proyecto_detlle', proyecto_id=proyecto_id))


@project_bp.route('/proyecto/<int:proyecto_id>/detalle')
def proyecto_detlle(proyecto_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT 
        p.id as proyecto_id, p.nombre as proyecto_nombre, p.estado as proyecto_estado,
        p.creado as proyecto_creado, uc_p.nombre as proyecto_creado_por,
        s.id as sprint_id, s.nombre as sprint_nombre, s.estado as sprint_estado,
        s.creado as sprint_creado, uc_s.nombre as sprint_creado_por,
        t.id as tarea_id, t.titulo as tarea_titulo, t.descripcion, 
        t.estado as tarea_estado, t.prioridad, t.creado as tarea_creado, t.fecha_termino,
        t.archivo_adjunto, ua.nombre as asignado_nombre, ua.username as asignado_username,
        uc_t.nombre as tarea_creado_por
    FROM proyectos p
    LEFT JOIN sprints s ON p.id = s.proyecto_id
    LEFT JOIN tareas t ON s.id = t.sprint_id
    LEFT JOIN usuarios ua ON t.asignado_id = ua.id
    LEFT JOIN usuarios uc_p ON p.creado_id = uc_p.id
    LEFT JOIN usuarios uc_s ON s.creado_id = uc_s.id
    LEFT JOIN usuarios uc_t ON t.creado_id = uc_t.id
    WHERE p.id = %s
    ORDER BY p.id, s.id, t.prioridad = 'urgente' DESC, t.creado DESC
    """
    
    cursor.execute(query, (proyecto_id,))
    results = cursor.fetchall()
    
    cursor.execute("SELECT id, nombre, username FROM usuarios WHERE activo = TRUE ORDER BY nombre")
    usuarios = cursor.fetchall()
    
    proyectos = {}
    for row in results:
        pid = row['proyecto_id']
        if pid not in proyectos:
            proyectos[pid] = {
                'id': pid,
                'nombre': row['proyecto_nombre'],
                'estado': row['proyecto_estado'],
                'creado': row['proyecto_creado'],
                'creado_por': row['proyecto_creado_por'],
                'sprints': {}
            }
        
        sid = row['sprint_id']
        if sid and sid not in proyectos[pid]['sprints']:
            proyectos[pid]['sprints'][sid] = {
                'id': sid,
                'nombre': row['sprint_nombre'],
                'estado': row['sprint_estado'],
                'creado': row['sprint_creado'],
                'creado_por': row['sprint_creado_por'],
                'tareas': []
            }
        
        if row['tarea_id'] and sid:
            proyectos[pid]['sprints'][sid]['tareas'].append({
                'id': row['tarea_id'],
                'titulo': row['tarea_titulo'],
                'descripcion': row['descripcion'],
                'estado': row['tarea_estado'],
                'prioridad': row['prioridad'],
                'creado': row['tarea_creado'],
                'creado_por': row['tarea_creado_por'],
                'archivo_adjunto': row['archivo_adjunto'],
                'asignado_nombre': row['asignado_nombre'],
                'asignado_username': row['asignado_username'],
                'fecha_termino': row['fecha_termino']
            })
    
    cursor.close()
    conn.close()
    
    return render_template('detalle_proyecto.html', proyectos=proyectos, usuarios=usuarios)
