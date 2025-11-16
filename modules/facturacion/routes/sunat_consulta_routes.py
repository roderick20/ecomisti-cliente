import requests
import base64
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_HALF_UP
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
import requests
import json
import os
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
from requests import Session as RequestsSession
# Configuración de la API Lycet


from modules.facturacion.models.operacion_model import Operacion


from modules.facturacion.models.operacion_configuracion_model import OperacionConfiguracion


from .. import bp 

# Clases de datos
class ConsultaCPEToken:
    def __init__(self, access_token, token_type, expires_in):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in

class ConsultaCPEDoc:
    def __init__(self, numRuc, codComp, numeroSerie, numero, fechaEmision, monto):
        self.numRuc = numRuc
        self.codComp = codComp
        self.numeroSerie = numeroSerie
        self.numero = numero
        self.fechaEmision = fechaEmision
        self.monto = monto

@bp.route('/sunat_consulta')
def get_status():
    try:

        configuracion = OperacionConfiguracion.get_all()['data']
        ruc = [row for row in configuracion if row.codigo == 'ruc'][0].valor
        sol_user = [row for row in configuracion if row.codigo == 'sol_user'][0].valor
        sol_pass = [row for row in configuracion if row.codigo == 'sol_pass'][0].valor

        
        # Crear cliente SOAP
        client = create_soap_client(ruc, sol_user, sol_pass )
        
        ventas = Operacion.get_all_by_validado()

        # Obtener ventas no validadas
        for venta in ventas['data']:
            tipo_doc = venta.tipo_comprobante
            serie = venta.serie
            numero = venta.correlativo

            cdr_result = ''

            
        
            response = client.service.getStatus( ruc, tipo_doc, serie, numero )
            code = response.statusCode
            print(f'Documento: {serie}-{numero}, Estado: {code}')
            if code == '0001':
                if tipo_doc == '01':
                    cdr_result = f'La Factura numero {serie}-{numero}, ha sido aceptado'
                elif tipo_doc == '03':
                    cdr_result = f'La Boleta de Venta numero {serie}-{numero}, ha sido aceptado'
                elif tipo_doc == '07':
                    cdr_result = f'La Nota de Crédito numero {serie}-{numero}, ha sido aceptado'
            if code == '0011':
                cdr_result = f'No enviado'

            Operacion.update_validado(venta.id, code, cdr_result)

        return redirect(url_for('facturacion.operacion_index'))

    except Exception as error:
        print(error)

# @cpe_bp.route('/GetStatusCDR/<area_return>/<tipo_comprobante>/<serie_comprobante>/<int:num_comprobante>')
# def get_status_cdr(area_return, tipo_comprobante, serie_comprobante, num_comprobante):
#     """
#     Descarga el CDR (Constancia de Recepción) de SUNAT
#     """
#     try:
#         from extensions import db
        
#         # Obtener configuración
#         dictionary = get_settings_dictionary(db.session)
        
#         # Crear cliente SOAP
#         client = create_soap_client(
#             dictionary["ruc"],
#             dictionary["clave_sol_usuario"],
#             dictionary["clave_sol_password"]
#         )
        
#         # Obtener CDR
#         response = client.service.getStatusCdr(
#             dictionary["ruc"],
#             tipo_comprobante,
#             serie_comprobante,
#             num_comprobante
#         )
        
#         # Guardar archivo CDR
#         bytes_content = response.content
        
#         # Crear directorio si no existe
#         cdr_path = os.path.join(
#             current_app.root_path,
#             'static',
#             'appdata',
#             'invoices',
#             'cdr'
#         )
#         os.makedirs(cdr_path, exist_ok=True)
        
#         # Nombre del archivo
#         filename = f"R-{dictionary['ruc']}-{tipo_comprobante}-{serie_comprobante}-{num_comprobante}.zip"
#         filepath = os.path.join(cdr_path, filename)
        
#         # Escribir archivo
#         with open(filepath, 'wb') as f:
#             f.write(bytes_content)
        
#         return redirect(url_for('sale_list.index', area=area_return))
        
#     except Exception as e:
#         current_app.logger.error(f"Error en GetStatusCDR: {str(e)}")
#         raise

def create_soap_client(ruc, usuario, password):
    """Crea el cliente SOAP para SUNAT"""
    wsdl_url = "https://e-factura.sunat.gob.pe/ol-it-wsconscpegem/billConsultService?wsdl"
    
    # Configurar sesión con autenticación
    session = RequestsSession()
    session.verify = True
    
    # Crear cliente SOAP con autenticación WS-Security
    transport = Transport(session=session)
    client = Client(
        wsdl=wsdl_url,
        transport=transport,
        wsse=UsernameToken(f"{ruc}{usuario}", password)
    )
    
    return client