from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.auth.models.auth_model import Auth

#auth_bp = Blueprint('auth', __name__)

from .. import bp 

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = Auth.login(username, password)
            if user:                
                return redirect(url_for('auth.index'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
        except Exception as error:
            print(error)
            return redirect(url_for('auth.error', error = error))
    
    return render_template('/auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('auth.login'))

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         nombre = request.form['nombre']
        
#         if register_user(username, email, password, nombre):
#             flash('Usuario registrado exitosamente. Puedes iniciar sesión.', 'success')
#             return redirect(url_for('auth.login'))
#         else:
#             flash('El usuario o email ya existe', 'error')
    
#     return render_template('register.html')