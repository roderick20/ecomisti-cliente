from flask import Flask, render_template_string, send_file, make_response
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from reportlab.lib.utils import ImageReader
from datetime import datetime
import qrcode
from PIL import Image

from modules.facturacion.models.operacion_model import Operacion
from modules.facturacion.models.operacion_detalle_model import OperacionDetalle

from .. import bp 

@bp.route('/operacion_pdf_ticket/<string:uniqueid>')
def operacion_pdf_ticket(uniqueid):
    print(uniqueid)
    operacion = Operacion.get_by_uniqueid(uniqueid)
    print(operacion['data'])
    detalle = OperacionDetalle.get_all_by_operacion_id(operacion['data'][0].id)
    print(operacion['data'][0])
    pdf = crear_ticket_pdf(operacion['data'][0], detalle['data'])
    return send_file(
        pdf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'ticket_{TICKET_DATA["factura"]}.pdf'
    )

# Datos del ticket
TICKET_DATA = {
    'farmacia': 'FARMACIA DON FELIX',
    'propietario': 'DE GIRON GONZALES GUILLIAM PAQUITA',
    'descripcion': 'VENTA DE PRODUCTOS FARMACEUTICOS - INYECTABLES Y BAZAR',
    'direccion': 'URB. MILAGROS ZONA C CAL. COSTA RICA 515 MZ 4 LOTE 14',
    'telefono': '95591263',
    'email': 'guilliam_giron10@homail.com',
    'ruc': '10410285172',
    'factura': 'FE01-000045',
    'cliente': 'ESTACION DE SERVICIOS SANTO TOMAS DE LIMA',
    'dni_ruc': '20812410256',
    'direccion_cliente': 'av. venezuela con riva aguero s/n frente universitario San Marcos Lima San Miguel',
    'fecha': '07/12/2024 05:12 P.M.',
    'tipo_pago': 'Efectivo',

    'subtotal': 25.59,
    'igv': 4.61,
    'total': 30.20,
    'vendedor': 'Denis'
}

def crear_ticket_pdf(operacion, detalle):

    """Genera el PDF del ticket"""
    buffer = BytesIO()
    ancho = 80 * mm  # Ancho de ticket térmico
    
    # Calcular altura necesaria basada en el contenido
    altura_base = 50 * mm  # Encabezado y pie
    altura_por_producto = 6 * mm  # Altura aproximada por producto
    altura_cliente = 25 * mm  # Información del cliente
    altura_totales = 35 * mm  # Sección de totales
    altura_qr = 65 * mm  # Código QR
    
    num_productos = len(detalle)
    print(detalle[0])
    # Algunos productos ocupan 2 líneas
    # productos_largos = sum(1 for p in detalle if len(p['nombre']) > 25)
    productos_largos = sum(1 for p in detalle if len(p.nombre) > 25)


    altura_productos = (num_productos * altura_por_producto) + (productos_largos * 3 * mm)
    
    alto = altura_base + altura_cliente + altura_productos + altura_totales + altura_qr


    
    c = canvas.Canvas(buffer, pagesize=(ancho, alto))
    y = alto - 10 * mm
    margen = 5 * mm
    
    # Título
    # c.setFont("Helvetica-Bold", 12)
    # c.drawCentredString(ancho/2, y, "FARMACIA")
    # y -= 5 * mm
    # c.drawCentredString(ancho/2, y, '"Don Félix"')
    # y -= 4 * mm
    # c.setFont("Helvetica-Oblique", 8)
    # c.drawCentredString(ancho/2, y, "Atención Profesional")
    # y -= 7 * mm
    
    # Línea divisoria
    # c.line(margen, y, ancho - margen, y)
    #y -= 5 * mm
    
    # Información de la farmacia
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(ancho/2, y, TICKET_DATA['farmacia'])
    y -= 4 * mm
    
    c.setFont("Helvetica", 7)
    texto_propietario = TICKET_DATA['propietario']
    c.drawCentredString(ancho/2, y, f"DE {texto_propietario.split('DE ')[1]}")
    y -= 4 * mm
    
    c.setFont("Helvetica", 6)
    # Dividir descripción en líneas
    c.drawCentredString(ancho/2, y, "VENTA DE PRODUCTOS FARMACEUTICOS -")
    y -= 3 * mm
    c.drawCentredString(ancho/2, y, "INYECTABLES Y BAZAR")
    y -= 4 * mm
    
    # Dirección
    c.drawCentredString(ancho/2, y, "URB. MILAGROS ZONA C CAL. COSTA")
    y -= 3 * mm
    c.drawCentredString(ancho/2, y, "RICA 515 MZ 4 LOTE 14")
    y -= 4 * mm
    
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(ancho/2, y, f"{TICKET_DATA['telefono']} - {TICKET_DATA['email']}")
    y -= 6 * mm
    
    # RUC y Factura
    c.line(margen, y, ancho - margen, y)
    y -= 5 * mm
    
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(ancho/2, y, f"R.U.C. {TICKET_DATA['ruc']}")
    y -= 5 * mm
    if operacion.tipo_comprobante == '01':
        c.drawCentredString(ancho/2, y, "Factura Electrónica")
    elif operacion.tipo_comprobante == '03':
        c.drawCentredString(ancho/2, y, "Boleta de Venta Electrónica")
    elif operacion.tipo_comprobante == '07':
        c.drawCentredString(ancho/2, y, "Boleta de Venta Electrónica")
    
    
    y -= 4 * mm
    c.drawCentredString(ancho/2, y, f"Nro. {operacion.serie}-{operacion.correlativo.zfill(6)}") #operacion
    y -= 6 * mm
    
    c.line(margen, y, ancho - margen, y)
    y -= 5 * mm
    
    # Información del cliente
    c.setFont("Helvetica", 6)
    c.drawString(margen, y, f"Cliente: {operacion.razon_social}")
    y -= 3 * mm
    #c.drawString(margen + 10*mm, y, TICKET_DATA['cliente'][30:] if len(TICKET_DATA['cliente']) > 30 else "")
    y -= 3 * mm
    
    c.drawString(margen, y, f"Dni - Ruc: {operacion.numero_doc}")
    y -= 3 * mm
    
    c.drawString(margen, y, f"Dirección: {operacion.direccion or ''}")
    y -= 3 * mm
    # c.drawString(margen + 10*mm, y, "aguero s/n frente")
    # y -= 3 * mm
    # c.drawString(margen + 10*mm, y, "universitario San Marcos")
    # y -= 3 * mm
    # c.drawString(margen + 10*mm, y, "Lima San Miguel")
    # y -= 4 * mm
    
    c.drawString(margen, y, f"Fecha Emision: {operacion.fecha_emision}")
    y -= 3 * mm
    c.drawString(margen, y, f"Tipo Pago: Efectivo")
    y -= 6 * mm
    
    # Encabezados de productos
    c.line(margen, y, ancho - margen, y)
    y -= 4 * mm
    
    c.setFont("Helvetica-Bold", 6)
    c.drawString(margen, y, "ARTICULO/PRODUCTO")
    c.drawString(ancho - 25*mm, y, "CANT PRECIO IMPORT")
    y -= 4 * mm
    
    c.line(margen, y, ancho - margen, y)
    y -= 4 * mm
    
    # Productos
    c.setFont("Helvetica", 6)
    print(detalle)
    for producto in detalle:
        # Nombre del producto (puede ocupar 2 líneas)
        if len(producto.nombre) > 25:
            c.drawString(margen, y, producto.nombre[:25])
            y -= 3 * mm
            c.drawString(margen, y, producto.nombre[25:])
        else:
            c.drawString(margen, y, producto.nombre)
        
        # Cantidad, precio, importe en la misma línea
        c.drawString(ancho - 25*mm, y, str(producto.cantidad) )
        c.drawRightString(ancho - 12*mm, y, str(f"{producto.precio:.1f}"))
        c.drawRightString(ancho - margen, y, str(f"{producto.total:.2f}"))
        y -= 4 * mm
    
    # Totales
    y -= 5 * mm
    c.line(margen, y, ancho - margen, y)
    y -= 5 * mm
    
    c.setFont("Helvetica-Bold", 7)
    c.drawString(ancho - 30*mm, y, "Total Inafecto")
    c.drawRightString(ancho - margen, y, "0")
    y -= 4 * mm
    
    c.drawString(ancho - 30*mm, y, "Subtotal")
    c.drawRightString(ancho - margen, y, f"{operacion.mto_oper_gravadas:.2f}")
    y -= 4 * mm
    
    c.drawString(ancho - 30*mm, y, "Igv 18%")
    c.drawRightString(ancho - margen, y, f"{operacion.mto_igv:.2f}")
    y -= 4 * mm
    
    c.drawString(ancho - 30*mm, y, "TOTAL S/.")
    c.drawRightString(ancho - margen, y, f"{operacion.mto_imp_venta:.2f}")
    y -= 6 * mm
    
    # Mensaje final
    c.setFont("Helvetica", 5)
    c.drawCentredString(ancho/2, y, "Gracias por tu Compra - Recomendanos con un amigo")
    y -= 3 * mm

    
    c.drawCentredString(ancho/2, y, f"VENDEDOR: Vendedor:{TICKET_DATA['vendedor']}")
    y -= 5 * mm
    
    c.setFont("Helvetica", 5)
    c.drawCentredString(ancho/2, y, "Esta es una representación impresa del comprobante electrónico")
    y -= 3 * mm
    

    
    # Código QR
    qr_buffer = generar_qr()
    c.drawImage(qr_buffer, (ancho - 20*mm)/2, y - 20*mm, width=20*mm, height=20*mm)

    c.setFont("Helvetica-Bold", 5)
    y -= 23 * mm
    c.drawCentredString(ancho/2, y, "NO SE ACEPTAN DEVOLUCIONES")
    y -= 3 * mm
    c.drawCentredString(ancho/2, y, "GRACIAS POR TU COMPRA")
    
    
    c.save()
    buffer.seek(0)
    return buffer


def generar_qr():
    """Genera código QR y retorna un ImageReader"""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr_data = f"RUC: {TICKET_DATA['ruc']}\nFactura: {TICKET_DATA['factura']}\nTotal: S/. {TICKET_DATA['total']}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir a PIL Image si no lo es
    if not isinstance(img, Image.Image):
        img = img.convert('RGB')
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Retornar ImageReader que ReportLab puede usar
    return ImageReader(buffer)
