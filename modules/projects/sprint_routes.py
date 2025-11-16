from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import get_db_connection, allowed_file, get_current_user

sprint_bp = Blueprint('sprint', __name__)

@sprint_bp.context_processor
def inject_user():
    return dict(current_user=get_current_user(session))


@sprint_bp.route('/sprint/nuevo/<int:proyecto_id>', methods=['GET', 'POST'])
def nuevo_sprint(proyecto_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        user_id = session['user_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sprints (nombre, proyecto_id, estado, creado_id, editado_id) 
            VALUES (%s, %s, 'abierto', %s, %s)
        """, (nombre, proyecto_id, user_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Sprint creado exitosamente', 'success')
        #return redirect(url_for('main.index'))
        return redirect(url_for('project.proyecto_detlle', proyecto_id=proyecto_id))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre FROM proyectos WHERE id = %s", (proyecto_id,))
    proyecto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('nuevo_sprint.html', proyecto=proyecto, proyecto_id=proyecto_id)

@sprint_bp.route('/sprint/<int:sprint_id>/<int:proyecto_id>/toggle_estado')
def toggle_sprint_estado(sprint_id, proyecto_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT estado FROM sprints WHERE id = %s", (sprint_id,))
    estado_actual = cursor.fetchone()[0]
    nuevo_estado = 'cerrado' if estado_actual == 'abierto' else 'abierto'
    
    cursor.execute("""
        UPDATE sprints SET estado = %s, editado = NOW(), editado_id = %s 
        WHERE id = %s
    """, (nuevo_estado, user_id, sprint_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Sprint {nuevo_estado} exitosamente', 'success')
    # return redirect(url_for('main.index'))
    return redirect(url_for('project.proyecto_detlle', proyecto_id=proyecto_id))