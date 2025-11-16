from flask import session
from database import db
import uuid
from datetime import datetime

class OperacionConfiguracion:
    
    @staticmethod
    def get_all():
        try:
            query = "SELECT * FROM operacion_configuracion"
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }
        

    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = "SELECT * FROM operacion_configuracion WHERE uniqueid = %s"
            data = db.query(query, (uniqueid,))
            return { "success": True, "data": data[0] }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def create(form_data):
        try:
            nombre = form_data.get('nombre', '').strip()
            valor =  form_data.get('valor', '').strip()
            codigo =  form_data.get('codigo', '').strip()
            creado_por = session['user_id']
            query = """
                INSERT INTO operacion_configuracion
                    ( nombre, valor, codigo, creado_por)
                VALUES (%s, %s, %s, %s) 
                    
            """
            data = db.execute(query, ( nombre.upper(), valor, codigo, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def update(form_data):
        try:
            uniqueid = form_data.get('uniqueid', '').strip()
            nombre = form_data.get('nombre', '').strip()
            valor =  form_data.get('valor', '').strip()
            codigo =  form_data.get('codigo', '').strip()
            modificado_por = session['user_id']
            query = """
                UPDATE operacion_configuracion SET
                    nombre = %s, 
                    valor = %s, 
                    codigo = %s,
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( nombre.upper(), valor, codigo, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM operacion_configuracion WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
