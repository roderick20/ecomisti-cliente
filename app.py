# app.py
from flask import Flask, render_template, session, request, redirect, url_for
from util.config import config

from modules.auth import  bp as main_bp
from modules.ordenes import  bp as orden_bp

import os

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config[config_name])
        
    # Registrar blueprints
    app.register_blueprint(main_bp, url_prefix='/')

    app.register_blueprint(orden_bp, url_prefix='/ordenes')


    @app.before_request
    def require_login():
        # Lista de rutas públicas (no requieren login)
        public_endpoints = {
            'auth.login', 
            'static',
            'uploads',  
        }
        
        if request.endpoint and request.endpoint not in public_endpoints:
            if 'user_id' not in session:  
                return redirect(url_for('auth.login'))
            
    @app.context_processor
    def inject_session():
        return dict(
            session_username = session.get('username'),
            session_nombre = session.get('nombre'),
            session_user_id = session.get('user_id')
        )
    
    return app

app = create_app()

if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5001)
