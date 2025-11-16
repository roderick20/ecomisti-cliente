from flask import Blueprint

bp = Blueprint('facturacion', __name__, template_folder='templates')

from .routes import (
    producto_grupo, 
    producto, 
    producto_imagen, 
    producto_precio, 
    producto_unidad, 
    personeria, 
    tabla_general, 
    operacion, 
    tipo_cambio, 
    serie_correlativo, 
    operacion_reportes,
    operacion_reportes, 
    operacion_pdf, 
    personeria_search,
    operacion_configuracion_routes,
    sunat_consulta_routes,
    sunat_factura_routes,
    sunat_nota_credito_routes,
    nota_credito_routes)