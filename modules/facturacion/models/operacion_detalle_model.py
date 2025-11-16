from flask import session
from database import db
import uuid
from datetime import datetime

class OperacionDetalle:
    
    @staticmethod
    def get_all_by_operacion_id(operacion_id):
        try:
            query = """
                SELECT     
  oper.cantidad,
  oper.precio,
  oper.total,
  pr.nombre
FROM operacion_detalle oper
LEFT JOIN producto pr ON pr.id = oper.producto_id
                WHERE operacion_id =  %s
            """
            data = db.query(query,(operacion_id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        
    @staticmethod
    def create(uniqueid, path):
        try:
            creado_por = session['user_id']
            query = """
                INSERT INTO operacion_detalle
                    (operacion_id, producto_id, cantidad,
                    mto_valor_unitario, mto_valor_venta, mto_base_igv,
                    total_impuestos, mto_precio_unitario, creado_por)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)             
            """
            data = db.execute(query, ( uniqueid, path, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
