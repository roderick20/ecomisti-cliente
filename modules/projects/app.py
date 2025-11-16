from flask import Flask, session, request, redirect, url_for
from config import Config
from filters import register_filters
from auth import auth_bp
from modules.auth.routes.main_routes import main_bp
from project_routes import project_bp
from sprint_routes import sprint_bp
from task_routes import task_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar filtros
    register_filters(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(task_bp)

    @app.before_request
    def require_login():
        # Lista de rutas públicas (no requieren login)
        public_endpoints = {
            'auth.login',      # Asegúrate de que coincida con el nombre de tu endpoint de login
            # 'auth.register',   # Si tienes registro público
            'static',          # Archivos estáticos siempre deben estar accesibles
        }

        # Si el endpoint actual no está en la lista pública y no hay sesión activa
        if request.endpoint and request.endpoint not in public_endpoints:
            if 'user_id' not in session:  # o la clave que uses para verificar login
                return redirect(url_for('auth.login'))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)