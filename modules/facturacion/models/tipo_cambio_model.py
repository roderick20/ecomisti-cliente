from flask import session
from database import db

class TipoCambio:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT * FROM `tipo_cambio`
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }        
        
    @staticmethod
    def get_by_fecha():
        try:
            query = """
                SELECT * FROM `tipo_cambio`
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }      

    @staticmethod
    def create(form_data):
        try:
            fecha = form_data.get('fecha', '').strip()
            compra =  form_data.get('compra', '').strip()
            venta =  form_data.get('venta', '').strip()

            creado_por = session['user_id']
            query = """
                INSERT INTO tipo_cambio ( fecha, compra, venta, creado_por)
                VALUES( %s, %s, %s, %s )
            """
            data = db.execute(query, ( fecha, compra, venta, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }


    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM  tipo_cambios WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
