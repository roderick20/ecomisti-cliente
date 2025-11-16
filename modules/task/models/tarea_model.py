from flask import session
from database import db
import uuid
from datetime import datetime

class TareaModel:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT  `id`,  `uniqueid`,  `titulo`, LEFT(`descripcion`, 256) AS descripcion,  `fecha_inicio`,  `fecha_fin`,  `sprint_id`,  `estado`,  `prioridad`,  `archivo_adjunto`,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `tareas` 
                WHERE estado = 1
                ORDER BY `fecha_inicio`
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        

        try:
            query = """
                WITH RECURSIVE grupo_path AS (
                    SELECT 
                        id,
                        uniqueid,
                        parent_id,
                        nombre AS path 
                    FROM productos_grupo
                    WHERE parent_id IS NULL

                    UNION ALL

                    SELECT 
                        g.id,
                        g.uniqueid,
                        g.parent_id,
                        CONCAT(gp.path, ' / ', g.nombre) AS path
                    FROM productos_grupo g
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
    def get_by_uniqueid(uniqueid):
        try:
            query = """
                SELECT  `id`,  `uniqueid`,  `titulo`, LEFT(`descripcion`, 256) AS descripcion,  `fecha_inicio`,  `fecha_fin`, `sprint_id`,  `estado`,  `prioridad`,  `archivo_adjunto`,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` FROM `tareas`
                WHERE uniqueid = %s
            """
            data = db.query(query, (uniqueid,))
            return { "success": True, "data": data[0] }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def create(form_data):
        try:
            titulo = form_data.get('titulo', '').strip()
            descripcion =  form_data.get('descripcion', '').strip()
            fecha_inicio =  form_data.get('fecha_inicio', '').strip()
            fecha_fin =  form_data.get('fecha_fin', '').strip()
            sprint_id =  '92de8617-a228-11f0-a5e2-1252b0f41a65' #form_data.get('sprint_id', '').strip()            
            creado_por = session['user_id']
            query = """
                INSERT INTO tareas
                    ( titulo, descripcion, sprint_id, creado_por, fecha_inicio, fecha_fin)
                SELECT 
                    %s, %s, (SELECT id FROM sprints WHERE uniqueid = %s), %s, %s, %s
                """
            data = db.execute(query, ( titulo, descripcion, sprint_id, creado_por, fecha_inicio, fecha_fin))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def update(form_data):
        try:
            uniqueid = form_data.get('uniqueid', '').strip()
            titulo = form_data.get('titulo', '').strip()
            descripcion =  form_data.get('descripcion', '').strip()
            fecha_inicio =  form_data.get('fecha_inicio', '').strip()
            fecha_fin =  form_data.get('fecha_fin', '').strip()
            modificado_por = session['user_id']
            query = """
                UPDATE tareas SET
                    titulo = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    descripcion = %s, 
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( titulo, fecha_inicio, fecha_fin, descripcion, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def update_estado(form_data):
        try:
            uniqueid = form_data.get('uniqueid', '').strip()
            modificado_por = session['user_id']
            query = """
                UPDATE tareas SET
                    estado = 3,
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM tareas WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
