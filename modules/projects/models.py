import mysql.connector
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

def get_db_connection():
    return mysql.connector.connect(**Config.DB_CONFIG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_current_user(session):
    if 'user_id' not in session:
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s AND activo = TRUE", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def audit_update(table, record_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table} SET editado = NOW(), editado_id = %s WHERE id = %s", 
                  (user_id, record_id))
    conn.commit()
    cursor.close()
    conn.close()

# Funciones de autenticación
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s AND activo = TRUE", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    #if user and check_password_hash(user['password_hash'], password):
    if user:
        return user
    return None

def register_user(username, email, password, nombre):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM usuarios WHERE username = %s OR email = %s", (username, email))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False  # Usuario ya existe
    
    password_hash = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO usuarios (username, email, password_hash, nombre) 
        VALUES (%s, %s, %s, %s)
    """, (username, email, password_hash, nombre))
    conn.commit()
    cursor.close()
    conn.close()
    return True