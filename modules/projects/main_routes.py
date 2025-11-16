from flask import Blueprint, render_template, redirect, url_for, session
from models import get_db_connection, get_current_user

main_bp = Blueprint('main', __name__)

@main_bp.context_processor
def inject_user():
    return dict(current_user=get_current_user(session))

@main_bp.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT 
        p.id as proyecto_id, p.nombre as proyecto_nombre, p.estado as proyecto_estado,
        p.creado as proyecto_creado, uc_p.nombre as proyecto_creado_por,
        s.id as sprint_id, s.nombre as sprint_nombre, s.estado as sprint_estado,
        s.creado as sprint_creado, uc_s.nombre as sprint_creado_por,
        t.id as tarea_id, t.titulo as tarea_titulo, t.descripcion, 
        t.estado as tarea_estado, t.prioridad, t.creado as tarea_creado, 
        t.archivo_adjunto, ua.nombre as asignado_nombre, ua.username as asignado_username,
        uc_t.nombre as tarea_creado_por
    FROM proyectos p
    LEFT JOIN sprints s ON p.id = s.proyecto_id
    LEFT JOIN tareas t ON s.id = t.sprint_id
    LEFT JOIN usuarios ua ON t.asignado_id = ua.id
    LEFT JOIN usuarios uc_p ON p.creado_id = uc_p.id
    LEFT JOIN usuarios uc_s ON s.creado_id = uc_s.id
    LEFT JOIN usuarios uc_t ON t.creado_id = uc_t.id
    ORDER BY p.id, s.id, t.prioridad = 'urgente' DESC, t.creado DESC
    """
    
    cursor.execute(query)
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
                'asignado_username': row['asignado_username']
            })
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', proyectos=proyectos, usuarios=usuarios)

@main_bp.route('/home')
def home():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('auth.login'))