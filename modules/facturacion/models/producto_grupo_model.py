from database import db
from flask import session
import uuid
from datetime import datetime

class ProductoGrupo:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT g1.id, g1.uniqueid, g1.nombre, g1.parent_id,
                       g1.creado, g1.creado_por, g1.modificado, g1.modificado_por,
                       g2.nombre AS parent_nombre
                FROM producto_grupo g1
                LEFT JOIN producto_grupo g2 ON g1.parent_id = g2.id
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }    


        
    @staticmethod
    def get_all_select():
        try:
            query = """
                WITH RECURSIVE grupo_path AS (
                    SELECT 
                        id,
                        uniqueid,
                        parent_id,
                        nombre AS path 
                    FROM producto_grupo
                    WHERE parent_id IS NULL

                    UNION ALL

                    SELECT 
                        g.id,
                        g.uniqueid,
                        g.parent_id,
                        CONCAT(gp.path, ' / ', g.nombre) AS path
                    FROM producto_grupo g
                    INNER JOIN grupo_path gp ON g.parent_id = gp.id
                )
                SELECT 
                    uniqueid,
                    path
                FROM grupo_path
                ORDER BY path;
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
                       g2.nombre AS parent_nombre,
                       g2.uniqueid AS parent_uniqueid
                FROM producto_grupo g1
                LEFT JOIN producto_grupo g2 ON g1.parent_id = g2.id
                WHERE g1.id = %s
            """
            data = db.query(query, (id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = """
                SELECT g1.id, g1.uniqueid, g1.nombre, g1.parent_id,
                       g1.creado, g1.creado_por, g1.modificado, g1.modificado_por,
                       g2.nombre AS parent_nombre,
                       g2.uniqueid AS parent_uniqueid
                FROM producto_grupo g1
                LEFT JOIN producto_grupo g2 ON g1.parent_id = g2.id
                WHERE g1.uniqueid = %s
            """
            data = db.query(query, (uniqueid,))
            return { "success": True, "data": data[0] }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def exists(id):
        try:
            query = "SELECT 1 FROM producto_grupo WHERE id = %s"
            data = db.query(query, (id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def create( form_data):
        try:
            nombre = form_data.get('nombre', '').strip()
            parent_id =  form_data.get('parent_id', '').strip()
            creado_por = session['user_id']
        
            query = """
                INSERT INTO producto_grupo 
                    ( nombre, parent_id, creado_por)
                SELECT                    
                    %s,
                    (SELECT id FROM producto_grupo WHERE uniqueid = %s),
                    %s                   
            """
            data = db.execute(query, ( nombre, parent_id, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def update( form_data):
        try:
            print(form_data)
            nombre = form_data.get('nombre', '').strip()
            parent_id =  form_data.get('parent_id', '').strip()
            modificado_por = session['user_id']
            uniqueid = form_data.get('uniqueid', '').strip()
            query = """
                UPDATE producto_grupo SET
                    nombre = %s,
                    parent_id = (
                        SELECT id FROM (
                            SELECT id FROM producto_grupo WHERE uniqueid = %s
                        ) AS temp
                    ),
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( nombre, parent_id, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM  producto_grupo WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }


