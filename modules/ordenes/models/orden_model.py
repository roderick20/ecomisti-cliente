from flask import session
from util.database import db
from datetime import datetime

class OrdenModel:

    @staticmethod
    def get_table(request):
        try:
            # Obtener y limpiar parámetros DataTables
            draw = int(request.get('draw', 1))
            start = int(request.get('start', 0))
            length = int(request.get('length', 10))
            search_value = request.get('search', '').strip()

      

            # Construcción segura de la cláusula WHERE y parámetros
            where_clause = ""
            params = {'start': start, 'length': length}

            if search_value:
                where_clause = """
                    WHERE os.GuiaRemision LIKE %(search)s 
                       OR os.GuiaTransportista LIKE %(search)s
                """
                params['search'] = f"%{search_value}%"

            # Query para contar total (con o sin búsqueda)
            count_query = f"""
                SELECT COUNT(*) AS TotalCount
                FROM [Orden] os
                LEFT JOIN [Personeria] tr ON os.TransportistaId = tr.PersoneriaID
                {where_clause}
            """

           
            # Ejecutar count
            count_result = db.query(count_query, params)
            
            total_records = count_result[0].TotalCount if count_result else 0

            # Query principal con paginación
            data_query = f"""
                SELECT 
                    os.[Id],
                    os.[UniqueId],
                    os.[Ticket],
                    os.[Anyo],
                    os.[Mes],
                    os.[Estado],
                    os.[Facturado],
                    FORMAT(os.[FechaRecepcion], 'dd-MM-yyyy') AS FechaRecepcion,
                    FORMAT(os.[HoraIngreso], 'HH:mm') AS HoraIngreso,
                    FORMAT(os.[HoraSalida], 'HH:mm') AS HoraSalida,
                    os.[Created],
                    os.[Author],
                    os.[Modified],
                    os.[Editor],
                    os.[TransportistaId],
                    os.[Placa_Tracto],
                    os.[Placa_Carreta],
                    os.[TransportistaServicioId],
                    os.[Placa_TractoServicio],
                    os.[Placa_CarretaServicio],
                    tr.[Personeria] AS TransportistaName
                FROM [Orden] os
                LEFT JOIN [Personeria] tr ON os.TransportistaId = tr.PersoneriaID
                {where_clause}
                ORDER BY os.Id DESC
                OFFSET %(start)s ROWS 
                FETCH NEXT %(length)s ROWS ONLY
            """

            data_result = db.query(data_query, params)

            data_dict = [row._asdict() for row in data_result] if data_result else []

            return {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": data_dict
            }

        except Exception as error:
            print("Error en TareaModel.create:", error)
            return {"success": False, "error": str(error)}