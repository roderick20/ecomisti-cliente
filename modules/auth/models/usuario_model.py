from flask import session
from util.database import db
import uuid
from datetime import datetime
import bcrypt

class UsuarioModel:

    @staticmethod
    def get_all():
        try:
            query = "SELECT  * FROM usuario"
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) } 

    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = "SELECT  * FROM usuario WHERE uniqueid =  %s"
            data = db.query(query,(uniqueid,))
            return { "success": True, "data": data[0] }
        except Exception as error:
            return { "success": False, "error": str(error) }     
        
    @staticmethod
    def create(form_data):
        try:

            

            username =  form_data.get('username', '').strip()
            email =  form_data.get('email', '').strip()
            password =  form_data.get('password', '').strip()
            nombre =  form_data.get('nombre', '').strip()
            habilitado =  form_data.get('habilitado', '').strip()

            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password_bytes, salt)

            creado_por = session['user_id']
            query = """
                INSERT INTO usuario
                    ( username, email, password, nombre, habilitado, creado_por)
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
            """
            data = db.execute(query, ( username, email, password_hash.decode('utf-8'), nombre, habilitado, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def update(form_data):
        try:
            username =  form_data.get('username', '').strip()
            email =  form_data.get('email', '').strip()
            password_hash =  form_data.get('password_hash', '').strip()
            nombre =  form_data.get('nombre', '').strip()
            activo =  form_data.get('activo', '').strip()

            modificado_por = session['user_id']
            uniqueid =  form_data.get('uniqueid', '').strip()
            query = """
                UPDATE usuario SET
                    username = %s,
                    email = %s,
                    password_hash = %s,
                    nombre = %s,
                    activo = %s,
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( username, email, password_hash, nombre, activo, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM  usuario WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
