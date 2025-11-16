# database.py
import pymssql
from util.config import Config
from collections import namedtuple

class Database:
    def __init__(self):
        self.config = {
            'server': Config.MSSQL_HOST,
            'user': Config.MSSQL_USER,
            'password': Config.MSSQL_PASSWORD,
            'database': Config.MSSQL_DB,
            'charset': 'utf8',  # pymssql usa 'utf8' (no utf8mb4)
            'port': getattr(Config, 'MSSQL_PORT', 1433),
            'as_dict': True  # permite usar dict-like rows
        }

    def get_connection(self):
        try:
            conn = pymssql.connect(
                server=self.config['server'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                port=self.config['port'],
                charset=self.config['charset']
            )
            return conn
        except Exception as e:
            print(f"Error conectando a SQL Server: {e}")
            return None

    def execute(self, query, params=None):
        """Ejecuta una consulta de escritura (INSERT, UPDATE, DELETE) y devuelve el ID del último registro insertado si aplica."""
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()

            # En SQL Server, puedes obtener el último ID con SCOPE_IDENTITY()
            # Pero solo si hiciste un INSERT con IDENTITY
            # Si no necesitas el ID, puedes omitir esto o devolver None
            # Alternativa: no devolver lastrowid (pymssql no lo soporta directamente)
            return None  # O ajusta según tu lógica
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    def query(self, query, params=None):
        """Ejecuta una consulta de lectura y devuelve una lista de namedtuples."""
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()

            if not rows:
                return []

            # Obtener nombres de columnas
            columns = [col[0] for col in cursor.description]
            # Normalizar nombres
            columns = [col.replace(' ', '_').replace('-', '_').replace('.', '_') for col in columns]

            Row = namedtuple('Row', columns, rename=True)  # rename=True evita nombres inválidos
            return [Row(*row) for row in rows]

        except Exception as e:
            print(f"Error ejecutando query: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    def execute_query(self, query, params=None, fetch=False):
        """Método genérico: si fetch=True, devuelve resultados; si no, ejecuta y confirma."""
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())

            if fetch:
                return cursor.fetchall()
            else:
                connection.commit()
                return True  # o None, según tu convención
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

# Instancia global
db = Database()