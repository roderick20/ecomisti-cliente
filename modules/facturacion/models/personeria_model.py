from flask import session
from database import db
import uuid
from datetime import datetime

class Personeria:
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT  `id`,  `uniqueid`,      razon_social,
    nombre_comercial,
    tipo_doc,
    numero_doc,
    direccion,
    personeria_tipo,
    contacto,
    telefono,
    email,
    cuenta_detraccion,
    cuenta_cci,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `personeria` 
            """
            data = db.query(query)
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   
        
    @staticmethod
    def get_by_id(id):
        try:
            query = """
                SELECT  `id`,  `uniqueid`,      razon_social,
    nombre_comercial,
    tipo_doc,
    numero_doc,
    personeria_tipo,
    contacto,
    telefono,
    email,
    cuenta_detraccion,
    cuenta_cci,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `personeria` 
                WHERE id =  %s
            """
            data = db.query(query,(id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }     
        
    @staticmethod
    def get_by_numero_doc(numero_doc):
        try:
            query = """
                SELECT  `id`,  `uniqueid`,      razon_social,
    nombre_comercial,
    tipo_doc,
    numero_doc,
    personeria_tipo,
    contacto,
    telefono,
    email,
    cuenta_detraccion,
    cuenta_cci,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `personeria` 
                WHERE numero_doc =  %s
            """
            data = db.query(query,(numero_doc,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }     


    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = """
                SELECT  `id`,  `uniqueid`,      razon_social,
    nombre_comercial,
    tipo_doc,
    numero_doc,
    personeria_tipo,
    contacto,
    telefono,
    email,
    cuenta_detraccion,
    cuenta_cci,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `personeria` 
                WHERE uniqueid =  %s
            """
            data = db.query(query,(uniqueid,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   

    @staticmethod
    def search_by_numero_doc( q ):
        try:
            search_term = f"%{q}%"
            query = """SELECT `id`,  `uniqueid`,      razon_social,
    nombre_comercial,
    tipo_doc,
    numero_doc AS text,
    personeria_tipo,
    contacto,
    telefono,
    email,
    cuenta_detraccion,
    cuenta_cci,  `creado_por`,  `creado`,  `modificado_por`,  `modificado`  FROM `personeria` WHERE numero_doc LIKE  %s"""
            data = db.query(query, (search_term,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   

    @staticmethod
    def search_by_razon_social( q ):
        try:
            search_term = f"%{q}%"
            query = """SELECT `id`,  `uniqueid`,      razon_social AS text,
    nombre_comercial,
    tipo_doc,
    numero_doc,
    personeria_tipo,
    contacto,
    telefono,
    email,
    cuenta_detraccion,
    cuenta_cci,  `creado_por`,  `creado`,  `modificado_por`,  `modificado`  FROM `personeria` WHERE razon_social LIKE  %s"""

            data = db.query(query, (search_term,))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }     
        
    @staticmethod
    def create(form_data):
        try:
            razon_social = form_data.get('razon_social', '').strip()
            nombre_comercial =  ''# form_data.get('nombre_comercial', '').strip()
            tipo_doc = form_data.get('tipo_doc', '').strip()
            numero_doc =  form_data.get('numero_doc', '').strip()
            personeria_tipo = form_data.get('personeria_tipo', '').strip()
            contacto =   ''#form_data.get('contacto', '').strip()
            telefono =  ''#form_data.get('telefono', '').strip()
            email =  ''# form_data.get('email', '').strip()
            cuenta_detraccion =  ''#form_data.get('cuenta_detraccion', '').strip()
            cuenta_cci =  ''#form_data.get('cuenta_cci', '').strip()

            direccion = form_data.get('direccion', '').strip()
            ubigeo =  form_data.get('ubigeo', '').strip()

            creado_por = session['user_id']            
            query = """
                INSERT INTO personeria
                    (razon_social, nombre_comercial, tipo_doc, numero_doc,
                    personeria_tipo, contacto, telefono, email,
                    cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por)
                VALUES( %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s)  
            """
            data = db.execute(query, ( razon_social, nombre_comercial, tipo_doc, numero_doc, 
                                       personeria_tipo, contacto, telefono, email,
                                       cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def create_ruc(razon_social, numero_doc, direccion, ubigeo):
        try:
            #razon_social = form_data.get('razon_social', '').strip()
            nombre_comercial =  ''# form_data.get('nombre_comercial', '').strip()
            tipo_doc = 6 #form_data.get('tipo_doc', '').strip()
            
            #numero_doc =  form_data.get('numero_doc', '').strip()
            personeria_tipo = 1 #form_data.get('personeria_tipo', '').strip()
            contacto =   ''#form_data.get('contacto', '').strip()
            telefono =  ''#form_data.get('telefono', '').strip()
            email =  ''# form_data.get('email', '').strip()
            cuenta_detraccion =  ''#form_data.get('cuenta_detraccion', '').strip()
            cuenta_cci =  ''#form_data.get('cuenta_cci', '').strip()

            #direccion = form_data.get('direccion', '').strip()
            #ubigeo =  form_data.get('ubigeo', '').strip()

            creado_por = session['user_id']            
            query = """
                INSERT INTO personeria
                    (razon_social, nombre_comercial, tipo_doc, numero_doc,
                    personeria_tipo, contacto, telefono, email,
                    cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por)
                VALUES( %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s)  
            """
            data = db.execute(query, ( razon_social, nombre_comercial, tipo_doc, numero_doc, 
                                       personeria_tipo, contacto, telefono, email,
                                       cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def create_dni(razon_social, numero_doc):
        try:
            #razon_social = form_data.get('razon_social', '').strip()
            nombre_comercial =  ''# form_data.get('nombre_comercial', '').strip()
            tipo_doc = 1 #form_data.get('tipo_doc', '').strip()
            
            #numero_doc =  form_data.get('numero_doc', '').strip()
            personeria_tipo = 1 #form_data.get('personeria_tipo', '').strip()
            contacto =   ''#form_data.get('contacto', '').strip()
            telefono =  ''#form_data.get('telefono', '').strip()
            email =  ''# form_data.get('email', '').strip()
            cuenta_detraccion =  ''#form_data.get('cuenta_detraccion', '').strip()
            cuenta_cci =  ''#form_data.get('cuenta_cci', '').strip()

            direccion = ''
            ubigeo =  ''

            creado_por = session['user_id']            
            query = """
                INSERT INTO personeria
                    (razon_social, nombre_comercial, tipo_doc, numero_doc,
                    personeria_tipo, contacto, telefono, email,
                    cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por)
                VALUES( %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s)  
            """
            data = db.execute(query, ( razon_social, nombre_comercial, tipo_doc, numero_doc, 
                                       personeria_tipo, contacto, telefono, email,
                                       cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }


    @staticmethod
    def delete(uniqueid):
        try:
            query = "DELETE FROM personeria WHERE uniqueid = %s"
            data = db.execute(query, ( uniqueid, ))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
