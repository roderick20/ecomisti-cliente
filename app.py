# app.py
from flask import Flask, render_template, session, request, redirect, url_for
from util.config import config

from modules.auth import  bp as main_bp


import os

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config[config_name])
    
    # Inicializar base de datos
    # init_database()
    
    # Registrar blueprints
    app.register_blueprint(main_bp, url_prefix='/')

    # app.register_blueprint(facturacion_bp, url_prefix='/facturacion')
    # app.register_blueprint(task_bp, url_prefix='/task')


    @app.before_request
    def require_login():
        # Lista de rutas públicas (no requieren login)
        public_endpoints = {
            'auth.login',      # Asegúrate de que coincida con el nombre de tu endpoint de login
            # 'auth.register',   # Si tienes registro público
            'static','uploads',          # Archivos estáticos siempre deben estar accesibles
        }

        # Si el endpoint actual no está en la lista pública y no hay sesión activa
        if request.endpoint and request.endpoint not in public_endpoints:
            if 'user_id' not in session:  # o la clave que uses para verificar login
                return redirect(url_for('auth.login'))
            
    @app.context_processor
    def inject_session():
        username = session.get('username')
        return dict(username=username)

    return app

app = create_app()

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5001)
    #app.run(debug=False) 


