from flask import session
from database import db
import uuid
from datetime import datetime

class ProductoImagen:
    
    @staticmethod
    def get_all_by_producto_id(producto_id):
        try:
            query = """
                SELECT  `id`,  `uniqueid`,  `producto_id`, `path`,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `producto_imagen` 
                WHERE producto_id =  %s
            """
            data = db.query(query,(producto_id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        
    @staticmethod
    def create(uniqueid, path):
        try:
            creado_por = session['user_id']
            query = """
                INSERT INTO producto_imagen
                    ( producto_id, path, creado_por)
                SELECT 
                    (SELECT id FROM productos WHERE uniqueid = %s), %s, %s
            """
            data = db.execute(query, ( uniqueid, path, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM  producto_imagen WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
