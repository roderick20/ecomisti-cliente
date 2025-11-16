from flask import session
import uuid
#from werkzeug.security import generate_password_hash, check_password_hash
#from config import Config
from util.database import db
import bcrypt
class Auth:
    
    
# def get_db_connection():
#     return mysql.connector.connect(**Config.DB_CONFIG)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def get_current_user(session):
        if 'user_id' not in session:
            return None        

        query = "SELECT * FROM [dbo].[Personeria] WHERE NroIdentidad = %s"
        data = db.query(query, (session['user_id'],))


        return data

# def audit_update(table, record_id, user_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(f"UPDATE {table} SET editado = NOW(), editado_id = %s WHERE id = %s", 
#                   (user_id, record_id))
#     conn.commit()
#     cursor.close()
#     conn.close()

    @staticmethod
    def login(username, password):
        #query = "SELECT * FROM usuario WHERE username = %s AND habilitado = TRUE"
        query = "SELECT * FROM [dbo].[Personeria] WHERE NroIdentidad = %s AND password = %s"
        data = db.query(query, (username, password))[0]
        print(data)
        if data:
            # stored_hash = data.password.encode('utf-8')  # bcrypt espera bytes
            # if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                
            session['user_id'] = data.PersoneriaID
            session['username'] = data.NroIdentidad
            session['nombre'] = data.Personeria

            print("¡Inicio de sesión exitoso!")
            return True
            # else:
            #     print("Contraseña incorrecta.")
            #     return False
        else:
            print("Usuario no encontrado.")
            return False

        return data[0]

# def register_user(username, email, password, nombre):
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute("SELECT id FROM usuarios WHERE username = %s OR email = %s", (username, email))
#     if cursor.fetchone():
#         cursor.close()
#         conn.close()
#         return False  # Usuario ya existe
    
#     password_hash = generate_password_hash(password)
#     cursor.execute("""
#         INSERT INTO usuarios (username, email, password_hash, nombre) 
#         VALUES (%s, %s, %s, %s)
#     """, (username, email, password_hash, nombre))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return True