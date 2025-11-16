from flask import session
from database import db
import uuid
from datetime import datetime

class NotaCredito:

    @staticmethod
    def create(form_data):
        try:

            _serie_id = str(form_data.get('serie_id', '').strip()) 
            _correlativo = str(form_data.get('correlativo', '').strip())

            print(_serie_id)
            print(_correlativo)
            
            query = "SELECT * FROM operacion WHERE serie_id = %s AND correlativo = %s"
            operation = db.query(query, (_serie_id, _correlativo ))[0]

            query = "SELECT * FROM operacion_detalle WHERE operacion_id = %s"
            detalles = db.query(query, (operation.id, ))
            print(detalles)

            query = """SELECT nuevo.id AS id FROM serie_correlativo viejo
                    LEFT JOIN  serie_correlativo nuevo ON viejo.serie = nuevo.serie AND nuevo.tipo_comprobante = '07'
                    WHERE viejo.id = %s"""
            serie = db.query(query, (_serie_id,) )[0]
            print(serie.id)

            serie_id = serie.id

            fecha_emision = datetime.now()
            forma_pago = operation.forma_pago
            tipo_moneda = operation.tipo_moneda
            personeria_id =  operation.personeria_id

            mto_oper_gravadas =  operation.mto_oper_gravadas
            mto_igv = operation.mto_igv
            mto_imp_venta =  operation.mto_imp_venta

            total_impuestos = 0
            valor_venta = 0
            sub_total =  0 
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
                        (serie_id, correlativo, fecha_emision, 
                        forma_pago, tipo_moneda, personeria_id, mto_oper_gravadas,
                        mto_igv, total_impuestos, valor_venta, sub_total,
                        mto_imp_venta, detracion_cod_bien, detracion_cod_medio_pago, detracion_cta_banco,
                        detracion_porcentaje, detracion_mto, creado_por, operation_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    serie_id, correlativo, fecha_emision, 
                    forma_pago, tipo_moneda, personeria_id, mto_oper_gravadas,
                    mto_igv, total_impuestos, valor_venta, sub_total,
                    mto_imp_venta, detracion_cod_bien, detracion_cod_medio_pago, detracion_cta_banco,
                    detracion_porcentaje, detracion_mto, creado_por, operation.id
                ))

                operacion_id = cursor.lastrowid

                query_detalle = """
                    INSERT INTO operacion_detalle
                        (operacion_id, producto_id, cantidad, precio, total, creado_por)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                print('detalle')
                for detalle in detalles:
                    print(detalle)
                    cursor.execute(query_detalle, ( operacion_id, detalle.producto_id, detalle.cantidad, detalle.precio, detalle.total, creado_por ))

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

