from database import db
import uuid
from datetime import datetime

class TablaGeneral:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT g1.id, g1.uniqueid, g1.nombre, g1.parent_id,
                       g1.creado, g1.creado_por, g1.modificado, g1.modificado_por,
                       g2.nombre AS parent_nombre
                FROM tabla_general g1
                LEFT JOIN tabla_general g2 ON g1.parent_id = g2.id
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        
    @staticmethod
    def get_all_select():
        try:
            query = """
                SELECT 
                id,
                uniqueid,
                parent_id,
                nombre
                FROM tabla_general
                WHERE parent_id IS NULL
                ORDER BY nombre;
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }      

    @staticmethod
    def get_by_id(id):
        try:
            query = """
                SELECT g1.id, g1.uniqueid, g1.nombre, g1.parent_id,
                       g1.creado, g1.creado_por, g1.modificado, g1.modificado_por,
                       g2.nombre AS parent_nombre
                FROM tabla_general g1
                LEFT JOIN productos_grupo g2 ON g1.parent_id = g2.id
                WHERE g1.id = %s
            """
            data = db.query(query, (id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def exists(id):
        try:
            query = "SELECT 1 FROM tabla_general WHERE id = %s"
            data = db.query(query, (id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def create( nombre, parent_id=None):
        print('create')
        try:
            query = """
                INSERT INTO tabla_general 
                    ( nombre, parent_id, creado_por)
                SELECT                    
                    %s,
                    (SELECT id FROM tabla_general WHERE uniqueid = %s),
                    %s                   
            """
            data = db.execute(query, ( nombre, parent_id, 1))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(cls, id):
        conn = cls._get_connection()
        try:
            query = "DELETE FROM tabla_general WHERE id = %s"
            data = db.query(query, (id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }
