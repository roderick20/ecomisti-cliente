from flask import session
from database import db
import uuid
from datetime import datetime

class Producto:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT 
                    pr.uniqueid, 
                    pr.nombre, 
                    pu.nombre AS producto_unidad_nombre,
                    pg.nombre AS producto_grupo_name,
                    pr.enlace, 
                    pr.codigo,
                    pr.habilitado,
                    pp.precio_soles,
                    pp.precio_dolar    
                FROM producto pr
                LEFT JOIN producto_grupo pg ON pg.id = pr.producto_grupo_id
                LEFT JOIN producto_precio pp ON pp.producto_id = pr.id
                LEFT JOIN producto_unidad pu ON pu.id = pr.producto_unidad_id
                            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def search( q ):
        try:
            search_term = f"%{q}%"
            query = """
                SELECT 
                    pr.id,                   
                    pr.nombre AS text,
                    pr.codigo,
                    pp.precio_soles,
                    pu.nombre AS unidad_nombre
                FROM producto pr
                LEFT JOIN producto_precio pp ON pp.producto_id = pr.id
                LEFT JOIN producto_unidad pu ON pu.id = pr.producto_unidad_id
                WHERE pr.nombre LIKE %s
            """
            data = db.query(query, (search_term,))
            print(data)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   

    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = """
                SELECT 
                    pr.id,
                    pr.uniqueid, 
                    pr.nombre, 
                    pr.enlace, 
                    pr.producto_grupo_id, 
                    pr.codigo,
                    pr.habilitado,
                    pg.uniqueid AS producto_grupo_uniqueid,
                    pp.uniqueid AS producto_precio_uniqueid,
                    pp.producto_id,
                    pp.precio_soles,
                    pp.precio_dolar,
                    pp.unidad_medida_id,
                    pp.habilitado AS habilitado_precio	  
                FROM producto pr
                LEFT JOIN producto_grupo pg ON pg.id = pr.producto_grupo_id
                LEFT JOIN producto_precio pp ON pp.producto_id = pr.id
                WHERE pr.uniqueid = %s
            """
            data = db.query(query, (uniqueid,))
            return { "success": True, "data": data[0] }
        except Exception as error:
            return { "success": False, "error": str(error) }

    @staticmethod
    def create(form_data):
        try:
            print(form_data)
            nombre = form_data.get('nombre', '').strip().upper()
            producto_grupo_id =  form_data.get('producto_grupo_id', '').strip()
            enlace =  form_data.get('enlace', '').strip()
            codigo = form_data.get('codigo', '').strip()
            habilitado = form_data.get('habilitado') == 'on'
            producto_unidad_id = form_data.get('producto_unidad_id', '').strip()
            creado_por = session['user_id']
            query = """
                INSERT INTO producto
                    ( nombre, enlace, producto_grupo_id, codigo,
                    habilitado, producto_unidad_id, creado_por)
                SELECT 
                    %s, %s, (SELECT id FROM producto_grupo WHERE uniqueid = %s), %s,
                    %s, (SELECT id FROM producto_unidad WHERE uniqueid = %s), %s
            """
            producto_id = db.execute(query, ( nombre, enlace, producto_grupo_id, codigo, habilitado, producto_unidad_id, creado_por))
            #db.execute("SELECT LAST_INSERT_ID()")
            #------------------------------------------------------------------------------------------------------------------            
            precio_soles =  form_data.get('precio_soles', '0').strip()
            precio_dolar =  form_data.get('precio_dolar', '0').strip()
            unidad_medida_id = 1 #form_data.get('unidad_medida_id', '').strip()
            habilitado = 1 
            lista_id = 1 #form_data.get('lista_id', '').strip()

            query = """
                INSERT INTO producto_precio
                    ( `producto_id`,`precio_soles`,`precio_dolar`,`unidad_medida_id`,`habilitado`,`lista_id`, creado_por)
                VALUES 
                    ( %s, %s, %s, %s, %s, %s, %s)
            """
            data = db.execute(query, ( producto_id, precio_soles, precio_dolar, unidad_medida_id, habilitado, lista_id, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def update(form_data):
        try:
            print(form_data.get('uniqueid', '').strip())
            uniqueid = form_data.get('uniqueid', '').strip()
            nombre = form_data.get('nombre', '').strip().upper()
            producto_grupo_id =  form_data.get('producto_grupo_id', '').strip()
            enlace =  form_data.get('enlace', '').strip()
            codigo = form_data.get('codigo', '').strip()
            habilitado = 1 #form_data.get('habilitado') == 'on' 
            producto_unidad_id = form_data.get('producto_unidad_id', '').strip()
            modificado_por = session['user_id']
            query = """
                UPDATE producto SET
                    nombre = %s, 
                    enlace = %s, 
                    producto_grupo_id = (SELECT id FROM producto_grupo WHERE uniqueid = %s),
                    codigo = %s,
                    habilitado = %s,
                    producto_unidad_id = (SELECT id FROM producto_unidad WHERE uniqueid = %s),
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( nombre, enlace, producto_grupo_id, codigo, habilitado, producto_unidad_id, modificado_por, uniqueid))
            # -------------------------------------------------------------------------------------------------------------
            precio_soles =  form_data.get('precio_soles', '').strip()
            precio_dolar =  form_data.get('precio_dolar', '').strip()
            producto_precio_uniqueid =  form_data.get('producto_precio_uniqueid', '').strip()
            
            query = """
                UPDATE producto_precio SET
                    `precio_soles` = %s,
                    `precio_dolar` = %s,
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( precio_soles, precio_dolar, modificado_por, producto_precio_uniqueid))

            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM producto WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
