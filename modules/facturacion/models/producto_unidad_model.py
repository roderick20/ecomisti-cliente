from flask import session
from database import db
import uuid
from datetime import datetime

class ProductoUnidad:

    @staticmethod
    def get_all():
        try:
            query = """
                SELECT  `id`,  `uniqueid`,  `nombre`, `abreviatura`,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `producto_unidad` 
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) } 
        
    @staticmethod
    def get_all_select():
        try:
            query = "SELECT  id, uniqueid, nombre FROM producto_unidad"
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) } 
         
    @staticmethod
    def get_id(id):
        try:
            query = """
                SELECT  `id`,  `uniqueid`, `nombre`, `abreviatura`,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `producto_unidad` 
                WHERE id =  %s
            """
            data = db.query(query,(id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        
    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = """
                SELECT  `id`,  `uniqueid`, `nombre`, `abreviatura`,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `producto_unidad` 
                WHERE uniqueid =  %s
            """
            data = db.query(query,(uniqueid,))
            return { "success": True, "data": data[0] }
        except Exception as error:
            return { "success": False, "error": str(error) }     
        
    @staticmethod
    def create(form_data):
        try:
            nombre = form_data.get('nombre', '').strip()
            abreviatura =  form_data.get('abreviatura', '').strip()

            creado_por = session['user_id']
            query = """
                INSERT INTO producto_unidad
                    ( nombre, abreviatura, creado_por)
                VALUES 
                    (%s, %s, %s)
            """
            data = db.execute(query, ( nombre, abreviatura, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def update(form_data):
        try:
            nombre = form_data.get('nombre', '').strip()
            abreviatura =  form_data.get('abreviatura', '').strip()
            modificado_por = session['user_id']
            uniqueid =  form_data.get('uniqueid', '').strip()
            query = """
                UPDATE producto_unidad SET
                    nombre = %s,
                    abreviatura = %s,
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( nombre, abreviatura, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM  producto_unidad WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
