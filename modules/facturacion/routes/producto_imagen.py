# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from database import db
from modules.facturacion.models.producto_imagen_model import ProductoImagen
from werkzeug.utils import secure_filename
import os
import uuid

#producto_grupo_bp = Blueprint('producto_imagen', __name__)

from .. import bp 




@bp.route('/producto_imagen/create', methods=['POST'])
def producto_imagen_create():    
    print('producto_imagen_create')
    if request.method == 'POST':
        try:
            #if 'file' not in request.files:
            #     flash('No se seleccionó ningún archivo')
            #     return redirect(request.url)
            file = request.files['file']
            # if file.filename == '':
            #     flash('Archivo vacío')
            #     return redirect(request.url)
            #if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(file.filename)
            ext = ext.lower()
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join('uploads', unique_filename))
            ProductoImagen.create(request.form.get('uniqueid', '').strip(), unique_filename)
            flash('Archivo subido correctamente')
            #return redirect(url_for('upload_file'))
            # else:
            #      flash('Tipo de archivo no permitido')
            return redirect(url_for('facturacion.producto_update', uniqueid = request.form.get('uniqueid', '').strip()))
        except Exception as error:
            flash('Error: '+error, 'error')


    
@bp.route('/producto_imagen/delete/<string:uniqueid>/<string:producto_uniqueid>', methods=['POST'])
def producto_imagen_delete(uniqueid, producto_uniqueid):
    if request.method == 'POST':
        try:
            result = ProductoImagen.delete(uniqueid)
            flash('Producto eliminado', 'success')
            return redirect(url_for('facturacion.producto_update', uniqueid = producto_uniqueid))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('facturacion.producto_index'))

@bp.route('/producto_imagen/uploads/<string:filename>', methods=['GET'])
def producto_imagen_uploaded(filename):
    print('uploaded_file')
    
    return send_from_directory('uploads',filename)