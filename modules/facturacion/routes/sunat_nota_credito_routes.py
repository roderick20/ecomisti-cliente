import requests
import base64
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_HALF_UP
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app

# Configuración de la API Lycet


from modules.facturacion.models.operacion_model import Operacion
from modules.facturacion.models.operacion_detalle_model import OperacionDetalle

from modules.facturacion.models.operacion_configuracion_model import OperacionConfiguracion
from modules.facturacion.models.sunat_model import SunatModel
from .. import bp 

# 1. Definir la zona horaria UTC-5
tz_utc_minus_5 = timezone(timedelta(hours=-5))

@bp.route('/sunat_nota_credito/<string:uniqueid>')
def sunat_nota_credito(uniqueid):

    operacion = Operacion.get_by_uniqueid(uniqueid)['data'][0]
    detalle = OperacionDetalle.get_all_by_operacion_id(operacion.id)['data']
    configuracion = OperacionConfiguracion.get_all()['data']

    details = []
    for producto in detalle:
        valor_unitario = producto.precio / (Decimal('1') + Decimal('18') / Decimal('100'))  # = 100.00
        igv_unitario = producto.precio - valor_unitario   

        mto_base_igv = producto.total / (Decimal('1') + Decimal('18') / Decimal('100'))  # = 100.00
        total_igv = producto.total - mto_base_igv   

        details.append({
            'unidad': 'NIU',
            'cantidad':  float(producto.cantidad),
            'codProducto': '',
            'descripcion': producto.nombre,
            'mtoBaseIgv': round(float(mto_base_igv), 2),
            'porcentajeIgv': 18,
            'igv': round(float(total_igv), 2),
            'tipAfeIgv': '10',  # Gravado - Operación onerosa
            'totalImpuestos': round(float(total_igv), 2),
            'mtoValorVenta': round(float(mto_base_igv), 2),
            'mtoValorUnitario': round(float(valor_unitario), 2),
            'mtoPrecioUnitario': round(float(producto.precio), 2)            
        })


    """Endpoint para enviar factura"""
    try:
        # Datos de ejemplo (puedes recibir estos datos del request)
        invoice = {
            'ublVersion': '2.1',
            #'tipoOperacion': '0101',  # Venta - Catalogo.51
            'tipoDoc': '07',  # nota credito - Catalogo.01
            'serie': operacion.serie,
            'correlativo': operacion.correlativo,
            'tipDocAfectado': operacion.tipo_comprobante_ref,
            'numDocfectado': f'{operacion.serie}-{operacion.ref}', # Factura: Serie-Correlativo
            'codMotivo': '01', # // Catalogo. 09
            'desMotivo' :'ANULACION DE LA OPERACION',

            
            'fechaEmision': operacion.fecha_emision.isoformat(timespec='seconds')+"-05:00", #'2025-10-21T12:34:00-05:00',
            'tipoMoneda': 'PEN',
            #'formaPago': {
            #    'tipo': 'Contado'
            #},
            'company': {
                'ruc': SunatModel.getValor(configuracion, 'ruc'),
                'razonSocial': SunatModel.getValor(configuracion, 'razon_social'),
                'nombreComercial': SunatModel.getValor(configuracion, 'nombre_comercial'),
                'address': {
                    'ubigueo': SunatModel.getValor(configuracion, 'ubigueo'),
                    'departamento': SunatModel.getValor(configuracion, 'departamento'),
                    'provincia': SunatModel.getValor(configuracion, 'provincia'),
                    'distrito': SunatModel.getValor(configuracion, 'distrito'),
                    'urbanizacion': '-',
                    'direccion': SunatModel.getValor(configuracion, 'direccion'),
                    'codigoPais': 'PE',
                }
            },
            'client': {
                'tipoDoc': operacion.tipo_doc,  # RUC - Catalogo.06
                'numDoc': operacion.numero_doc,
                'rznSocial': operacion.razon_social
            },
            'mtoOperGravadas': float(operacion.mto_oper_gravadas),
            'mtoIGV': float(operacion.mto_igv),
            'totalImpuestos': float(operacion.mto_igv),
            'valorVenta': float(operacion.mto_oper_gravadas),
            'subTotal': float(operacion.mto_imp_venta),
            'mtoImpVenta': float(operacion.mto_imp_venta),
            'details': details,
            'legends': [
                {
                    'code': '1000',
                    'value': SunatModel.numero_a_soles(float(operacion.mto_imp_venta))
                }
            ]
        }
        
        print(invoice)
        # Si quieres recibir datos del cliente, descomenta:
        # invoice = request.get_json()
        
        # Enviar factura
        bill_result = SunatModel.send_invoice_nota(invoice)
        
        # Guardar XML
        xml_filename = f"{SunatModel.getValor(configuracion, 'ruc')}-01-{operacion.serie}-{operacion.correlativo}.xml"
        print(f'Guardando XML en {xml_filename}')
        SunatModel.save_file(xml_filename, bill_result['xml'])
        
        print(f"Valor Resumen (Hash): {bill_result['hash']}")
        
        # Verificar respuesta de SUNAT
        sunat_response = bill_result['sunatResponse']
        
        if not sunat_response['success']:
            error_message = sunat_response['error']
            print(error_message)
            return redirect(url_for('facturacion.operacion_index'))
            # return jsonify({
            #     'success': False,
            #     'error': error_message
            # }), 400
        
        # Guardar CDR
        cdr_filename = f"R-{SunatModel.getValor(configuracion, 'ruc')}-07-{operacion.serie}-{operacion.correlativo}.zip"
        print(f'Guardando CDR en {cdr_filename}')
        SunatModel.save_file(cdr_filename, sunat_response['cdrZip'], 'base64')
        
        # Procesar respuesta CDR
        cdr_result = sunat_response['cdrResponse']
        codigo_cdr = int(cdr_result['code'])
        
        status = ''
        if codigo_cdr == 0:
            status = 'ACEPTADA'
            Operacion.update_anulado(operacion.uniqueid_ref)
            print('ESTADO: ACEPTADA')
            if len(cdr_result.get('notes', [])) > 0:
                print('CON OBSERVACIONES:')
                print(cdr_result['notes'])
        else:
            status = 'RECHAZADA'
            print('ESTADO: RECHAZADA')
        
        print(f"RESULTADO DESCRIPCION SUNAT: {cdr_result['description']}")

        Operacion.update_estado(uniqueid, status, cdr_result['description'])

        
        
        # return jsonify({
        #     'success': True,
        #     'status': status,
        #     'hash': bill_result['hash'],
        #     'xml_filename': xml_filename,
        #     'cdr_filename': cdr_filename,
        #     'cdr_code': codigo_cdr,
        #     'cdr_description': cdr_result['description'],
        #     'notes': cdr_result.get('notes', [])
        # }), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # return jsonify({
        #     'success': False,
        #     'error': str(e)
        # }), 500
    
    return redirect(url_for('facturacion.operacion_index'))
