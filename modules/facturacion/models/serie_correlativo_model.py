from flask import session
from database import db

class SerieCorrelativo:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT * FROM `serie_correlativo`
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }    

    @staticmethod
    def get_all_venta():
        try:
            query = """
                SELECT * FROM `serie_correlativo` WHERE tipo_comprobante = '01' OR tipo_comprobante = '03'
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }    
        
    @staticmethod
    def get_all_nota_credito():
        try:
            query = """
                SELECT * FROM `serie_correlativo` WHERE tipo_comprobante = '07'
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   
        
    @staticmethod
    def get_by_fecha():
        try:
            query = """
                SELECT * FROM `serie_correlativo`
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }      

    @staticmethod
    def create(form_data):
        try:
            tipo_comprobante = form_data.get('tipo_comprobante', '').strip()
            serie =  form_data.get('serie', '').strip()
            correlativo =  form_data.get('correlativo', '').strip()

            creado_por = session['user_id']
            query = """
                INSERT INTO serie_correlativo ( tipo_comprobante, serie, correlativo, creado_por)
                VALUES( %s, %s, %s, %s )
            """
            data = db.execute(query, ( tipo_comprobante, serie, correlativo, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def update_correlativo(tipo_doc, serie):
        try:
            creado_por = session['user_id']
            query = """
                UPDATE serie_correlativo SET correlativo + 1 WHERE tipo_doc = %s AND serie = %s
            """
            data = db.execute(query, ( tipo_doc, serie))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }


    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM  serie_correlativo WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
