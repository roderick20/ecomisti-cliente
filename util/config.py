# config.py
import os


from dotenv import load_dotenv

load_dotenv()

class Config:


    MSSQL_HOST = os.environ.get('SQL_SERVER') or 'localhost'
    MSSQL_USER = os.environ.get('SQL_UID') or 'root'
    MSSQL_PASSWORD = os.environ.get('SQL_PWD') or 'Aladino?09'
    MSSQL_DB = os.environ.get('SQL_DATABASE') or 'sistema_facturacion'
    MSSQL_PORT = 1433  # opcional

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_muy_segura'
    
    # Configuración de MySQL
    
    # Configuración de uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

import os

    
# Crear carpeta de uploads si no existe
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)