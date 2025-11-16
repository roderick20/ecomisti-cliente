from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from modules.auth.models.usuario_model import UsuarioModel

from .. import bp 

@bp.route('/usuario')
def usuario_index():
    result = UsuarioModel.get_all()    
    print(result['data'])
    if result['success']:
        return render_template('/auth/usuario/index.html', list = result['data'])
    else:
        return render_template('error.html', error = result['error'])


@bp.route('/usuario/create', methods=['GET', 'POST'])
def usuario_create():    
    if request.method == 'POST':
        try:
            result = UsuarioModel.create(request.form)
            flash('usuario agregado', 'success')
            return redirect(url_for('auth.usuario_index'))
        except Exception as error:
            return render_template('error.html', error = result['error'])
    return render_template('/auth/usuario/create.html')

        
    

@bp.route('/usuario/update/<string:uniqueid>', methods=['GET', 'POST'])
def usuario_update(uniqueid):    
    if request.method == 'POST':
        try:
            result = usuario.update(request.form)
            return redirect(url_for('auth.usuario_index'))
        except Exception as error:
            print(error)
            #return render_template('error.html', error = error)
    usuario_grupo = usuarioGrupo.get_all_select()
    usuario_unidad = usuarioUnidad.get_all_select()
    print(usuario_unidad)
    usuario = usuario.get_by_uniqueid(uniqueid)
    imagenes = usuarioImagen.get_all_by_usuario_id(usuario['data']['id'])
    if usuario['success']:
        return render_template('/auth/usuario/update.html', 
                               usuario_grupo = usuario_grupo['data'],
                               usuario_unidad = usuario_unidad['data'], 
                               usuario = usuario['data'], 
                               imagenes = imagenes['data'])
    else:
        return render_template('error.html', error = result['error'])    

@bp.route('/usuario/delete/<string:uniqueid>', methods=['POST'])
def usuario_delete(uniqueid):
    if request.method == 'POST':
        try:
            result = usuario.delete(uniqueid)
            flash('usuario eliminado', 'success')
            return redirect(url_for('auth.usuario_index'))
        except Exception as error:
            flash('Error: ' + error, 'error')
            return redirect(url_for('auth.usuario_index'))