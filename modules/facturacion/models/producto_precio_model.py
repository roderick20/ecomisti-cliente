from flask import session
from database import db
import uuid
from datetime import datetime

class ProductoPrecio:
    
    @staticmethod
    def get_by_producto_uniqueid(uniqueid):
        try:
            query = """
                SELECT  
                    prp.`id`,  prp.`uniqueid`, prp.`producto_id`, prp.`precio_soles`, prp.`precio_dolar`, 
                    prp.`unidad_medida_id`, prp.`habilitado`, prp.`lista_id`,  prp.`creado_por`,  prp.`creado`,  prp.`modificado_por`,  prp.`modificado` 
                FROM `producto_precio` prp
                LEFT JOIN producto pro ON pro.id = prp.producto_id
                WHERE pro.uniqueid =  %s
            """
            data = db.query(query,(uniqueid,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        
    @staticmethod
    def create(form_data):
        try:
            producto_uniqueid = form_data.get('producto_uniqueid', '').strip()
            precio_soles =  form_data.get('precio_soles', '0').strip()
            precio_dolar =  form_data.get('precio_dolar', '0').strip()
            unidad_medida_id = 1 #form_data.get('unidad_medida_id', '').strip()
            habilitado = form_data.get('habilitado') == 'on' 
            lista_id = 1 #form_data.get('lista_id', '').strip()
            creado_por = session['user_id']
            query = """
                INSERT INTO producto_precio
                    ( `producto_id`,`precio_soles`,`precio_dolar`,`unidad_medida_id`,`habilitado`,`lista_id`, creado_por)
                SELECT 
                    (SELECT id FROM producto WHERE uniqueid = %s), %s, %s, %s, %s, %s, %s
            """
            data = db.execute(query, ( producto_uniqueid, precio_soles, precio_dolar, unidad_medida_id, habilitado, lista_id, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def update(form_data):
        try:
            uniqueid = form_data.get('uniqueid', '').strip()
            precio_soles = form_data.get('precio_soles', '').strip()
            precio_dolar =  form_data.get('precio_dolar', '').strip()
            unidad_medida_id =  form_data.get('unidad_medida_id', '').strip()
            habilitado = form_data.get('habilitado') == 'on' 
            lista_id = form_data.get('lista_id', '').strip()            
            modificado_por = session['user_id']
            query = """
                UPDATE producto_precio SET
                    `precio_soles` = %s,
                    `precio_dolar` = %s,
                    `unidad_medida_id` = %s,
                    `habilitado` = %s,
                    `lista_id` = %s,
                     modificado_por = %s
                WHERE uniqueid = %s               
            """
            data = db.execute(query, ( precio_soles, precio_dolar, unidad_medida_id, habilitado, lista_id, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

