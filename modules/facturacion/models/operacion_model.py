from flask import session
from database import db
import uuid
from datetime import datetime

class Operacion:
        
    @staticmethod
    def get_all_by_periodo(mes, anio):
        try:
            query = """
            SELECT  
                oper.id, 
                oper.uniqueid, 
                sec.tipo_comprobante,
                sec.serie,
                oper.correlativo,
                oper.fecha_emision,
                per.numero_doc,
                per.razon_social,
                per.tipo_doc,
                CONCAT(TRIM(per.direccion), ' ',UPPER(ubi.dpto), ' ', UPPER(ubi.prov), ' ',UPPER(ubi.distrito)) AS direccion,
                oper.tipo_moneda,
                oper.personeria_id,

                oper.mto_imp_venta,
                oper.mto_igv,
                oper.mto_oper_gravadas,
                usua.nombre,

                per.ubigeo,
                
                oper2.serie_id,
                oper2.correlativo  AS ref,
                                    oper.estado,
                    oper.cdr_result,
                    oper.anulado
            
            FROM operacion oper
            LEFT JOIN serie_correlativo sec ON sec.id = oper.serie_id
            LEFT JOIN personeria per ON per.id = oper.personeria_id
            LEFT JOIN ubigeo ubi ON ubi.ubigeo1 = per.ubigeo
            LEFT JOIN usuario usua ON usua.id = oper.creado_por
            LEFT JOIN operacion oper2 ON oper2.id = oper.operation_id
                WHERE 
                    MONTH(oper.fecha_emision) = %(mes)s
                    AND YEAR(oper.fecha_emision) = %(anio)s
                ORDER BY oper.creado DESC;
            """
            data = db.query(query, {'mes': mes, 'anio': anio})
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   
    
    @staticmethod
    def get_all_by_validado():
        try:
            query = """
SELECT  
    oper.id,                
    sec.tipo_comprobante,
    sec.serie,
    oper.correlativo
FROM operacion oper
LEFT JOIN serie_correlativo sec ON sec.id = oper.serie_id
WHERE oper.validado IS NULL
ORDER BY oper.creado DESC;
            """ #
            data = db.query(query, )
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   
        

    @staticmethod
    def get_all_by_periodo2(mes, anio):
        try:
            query = """
                SELECT  
                    oper.id, 
                    oper.uniqueid, 
                    sec.tipo_comprobante,
                    sec.serie,
                    oper.correlativo,
                    oper.fecha_emision,
                    per.numero_doc,
                    per.razon_social,
                    CONCAT(TRIM(per.direccion), ' ', UPPER(ubi.dpto), ' ', UPPER(ubi.prov), ' ', UPPER(ubi.distrito)) AS direccion,
                    oper.tipo_moneda,
                    oper.personeria_id,
                    oper.mto_imp_venta,
                    oper.mto_igv,
                    oper.mto_oper_gravadas,
                    usua.nombre,
                    per.ubigeo
                FROM operacion oper
                LEFT JOIN serie_correlativo sec ON sec.id = oper.serie_id
                LEFT JOIN personeria per ON per.id = oper.personeria_id
                LEFT JOIN ubigeo ubi ON ubi.ubigeo1 = per.ubigeo
                LEFT JOIN usuario usua ON usua.id = oper.creado_por
                WHERE 
                    MONTH(oper.fecha_emision) = %(mes)s
                    AND YEAR(oper.fecha_emision) = %(anio)s
                ORDER BY oper.creado DESC;
            """
            data = db.query3(query, {'mes': mes, 'anio': anio})
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }   
        
    @staticmethod
    def get_by_id(operacion_id):
        try:
            query = """
                SELECT  `id`,  `uniqueid`,      tipo_doc,
    serie,
    correlativo,
    fecha_emision,
    forma_pago,
    tipo_moneda,
    personeria_id,

    mto_oper_gravadas,
    mto_igv,
    total_impuestos,
    valor_venta,
    sub_total,
    mto_imp_venta,

    detracion_cod_bien,
    detracion_cod_medio_pago,
    detracion_cta_banco,
    detracion_porcentaje ,
    detracion_mto,  `creado_por`,  `creado`,  `modificado_por`,  `modificado` 
                FROM `operacion` 
                WHERE operacion_id =  %s
            """
            data = db.query(query,(operacion_id,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }     

    @staticmethod
    def get_by_uniqueid(uniqueid):
        try:
            query = """
            SELECT  
                oper.id, 
                oper.uniqueid, 
                sec.tipo_comprobante,
                sec.serie,
                oper.correlativo,
                oper.fecha_emision,
                per.numero_doc,
                per.razon_social,
                per.tipo_doc,
                CONCAT(TRIM(per.direccion), ' ',UPPER(ubi.dpto), ' ', UPPER(ubi.prov), ' ',UPPER(ubi.distrito)) AS direccion,
                oper.tipo_moneda,
                oper.personeria_id,

                oper.mto_imp_venta,
                oper.mto_igv,
                oper.mto_oper_gravadas,
                usua.nombre,

                per.ubigeo,
                
                oper2.uniqueid AS uniqueid_ref,
                oper2.serie_id,
                oper2.correlativo  AS ref,
                sec2.tipo_comprobante AS tipo_comprobante_ref
            
            FROM operacion oper
            LEFT JOIN serie_correlativo sec ON sec.id = oper.serie_id
            LEFT JOIN personeria per ON per.id = oper.personeria_id
            LEFT JOIN ubigeo ubi ON ubi.ubigeo1 = per.ubigeo
            LEFT JOIN usuario usua ON usua.id = oper.creado_por
            LEFT JOIN operacion oper2 ON oper2.id = oper.operation_id
            LEFT JOIN serie_correlativo sec2 ON sec2.id = oper2.serie_id

            WHERE oper.uniqueid =  %s
            """
            data = db.query(query,(uniqueid,))
            return { "success": True, "data": data }
        except Exception as error:
            return { "success": False, "error": str(error) }    

    @staticmethod
    def create(form_data):
        try:
            print(form_data)
            serie_id = form_data.get('serie_id', '').strip() 


            fecha = datetime.strptime(form_data.get('fecha_emision', '').strip(), "%Y-%m-%d").date()
            hora_actual = datetime.now().time()
            fecha_emision = datetime.combine(fecha, hora_actual)

            fecha_vencimiento = form_data.get('fecha_vencimiento', '').strip()

            forma_pago = form_data.get('forma_pago').strip() 
            tipo_moneda = form_data.get('tipo_moneda', '').strip()
            personeria_id =  form_data.get('personeria_id', '').strip()

            mto_oper_gravadas =  form_data.get('mto_oper_gravadas', '').strip()
            mto_igv = form_data.get('mto_igv', '').strip()
            # total_impuestos = form_data.get('total_impuestos').strip()
            # valor_venta = form_data.get('valor_venta', '').strip()
            # sub_total =  form_data.get('sub_total', '').strip()
            mto_imp_venta =  form_data.get('mto_imp_venta', '').strip()


            total_impuestos = 0
            valor_venta = 0
            sub_total =  0
     
            
            # detracion_cod_bien = form_data.get('detracion_cod_bien', '').strip()
            # detracion_cod_medio_pago = form_data.get('detracion_cod_medio_pago').strip() 
            # detracion_cta_banco =  form_data.get('detracion_cta_banco', '').strip()
            # detracion_porcentaje = form_data.get('detracion_porcentaje', '').strip()
            # detracion_mto = form_data.get('detracion_mto').strip()



            
            detracion_cod_bien = ''
            detracion_cod_medio_pago = ''
            detracion_cta_banco =  ''
            detracion_porcentaje = 0
            detracion_mto = 0

            creado_por = session['user_id']

            connection = db.get_connection()
            try:
                cursor = connection.cursor(dictionary=True)

                # 1. Incrementar y obtener el nuevo correlativo
                cursor.execute("UPDATE serie_correlativo SET correlativo = correlativo + 1 WHERE id = %s", (serie_id,))
                cursor.execute("SELECT correlativo FROM serie_correlativo WHERE id = %s", (serie_id,))
                result = cursor.fetchone()
                
                if not result:
                    raise ValueError("No se encontró la serie con ID proporcionado")
                
                correlativo = result['correlativo']

                # 2. Insertar la operación usando ese correlativo
                query = """
                    INSERT INTO operacion
                        (serie_id, correlativo, fecha_emision, fecha_vencimiento,
                        forma_pago, tipo_moneda, personeria_id, mto_oper_gravadas,
                        mto_igv, total_impuestos, valor_venta, sub_total,
                        mto_imp_venta, detracion_cod_bien, detracion_cod_medio_pago, detracion_cta_banco,
                        detracion_porcentaje, detracion_mto, creado_por)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    serie_id, correlativo, fecha_emision, fecha_vencimiento,
                    forma_pago, tipo_moneda, personeria_id, mto_oper_gravadas,
                    mto_igv, total_impuestos, valor_venta, sub_total,
                    mto_imp_venta, detracion_cod_bien, detracion_cod_medio_pago, detracion_cta_banco,
                    detracion_porcentaje, detracion_mto, creado_por
                ))

                operacion_id = cursor.lastrowid

                query_detalle = """
                    INSERT INTO operacion_detalle
                        (operacion_id, producto_id, cantidad, precio, total, creado_por)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                productos = form_data.getlist('producto_id[]')
                cantidades = form_data.getlist('cantidad[]')
                precios = form_data.getlist('precio[]')
                totales = form_data.getlist('total[]')
                for i in range(len(productos)):
                    cursor.execute(query_detalle, ( operacion_id, productos[i], cantidades[i], precios[i], totales[i], creado_por ))

                # 3. Confirmar transacción
                connection.commit()

                # Opcional: devolver el correlativo o el ID del nuevo registro
                  # si necesitas el ID autogenerado de la tabla `operacion`
                #print(f"Operación creada con correlativo: {correlativo}, ID: {nuevo_id}")

            except Exception as e:
                connection.rollback()  # deshacer si hay error
                print(f"Error: {e}")
                raise
            finally:
                cursor.close()
                connection.close()


            return { "success": True }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def update_estado(uniqueid, estado, cdr_result):
        try:            
            modificado_por = session['user_id']
            query = """
                UPDATE operacion SET
                    estado = %s, 
                    cdr_result = %s, 
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, ( estado, cdr_result, modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def update_validado(id, codigo, cdr_result):
        try:
            if codigo == '0001':            
                query = "UPDATE operacion SET validado = %s, cdr_result = %s, estado = 'ACEPTADA' WHERE id = %s "
                data = db.execute(query, ( codigo, cdr_result, id))
            if codigo == '0001' or codigo == '0002':            
                query = "UPDATE operacion SET validado = %s, cdr_result = %s, estado = 'RECHAZADA' WHERE id = %s "
                data = db.execute(query, ( codigo, cdr_result, id))
            else:
                query = "UPDATE operacion SET validado = %s WHERE id = %s "
                data = db.execute(query, ( codigo, id))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }

    @staticmethod
    def update_anulado(uniqueid):
        try:            
            modificado_por = session['user_id']
            query = """
                UPDATE operacion SET
                    anulado = 1,
                    modificado_por = %s
                WHERE uniqueid = %s
            """
            data = db.execute(query, (  modificado_por, uniqueid))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
