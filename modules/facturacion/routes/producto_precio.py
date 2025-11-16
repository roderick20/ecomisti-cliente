# routes/categorias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from database import db
from modules.facturacion.models.producto_precio_model import ProductoPrecio
from werkzeug.utils import secure_filename
import os
import uuid

from .. import bp

@bp.route('/producto_precio/create', methods=['POST'])
def producto_precio_create_update():    
    print('producto_imagen_create')
    if request.method == 'POST':
        try:
            producto_uniqueid = request.form.get('producto_uniqueid', '').strip()
            uniqueid = request.form.get('uniqueid', '').strip()
            if uniqueid == '':
                ProductoPrecio.create(request.form)
            else :
                
                ProductoPrecio.update(request.form)
            
            
            flash('Precio actualizado')

            return redirect(url_for('facturacion.producto_update', uniqueid = request.form.get('producto_uniqueid', '').strip()))
        except Exception as error:
            flash('Error: '+error, 'error')

