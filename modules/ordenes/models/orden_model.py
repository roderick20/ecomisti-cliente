from flask import session
from util.database import db
from datetime import datetime

class OrdenModel:

    #estado => 1 borrador, 2 enviado, 3 activo, 4 cerrado

    @staticmethod
    def getProductoGrupo():
        query = 'SELECT [GrupoID],[Descripcion] FROM [dbo].[ProductoGrupo]'
        data_result =  db.query(query)
        data_dict = [row._asdict() for row in data_result] if data_result else []
        return data_dict
    
    @staticmethod
    def get_orden_by_uniqueid(uniqueid):
        query = 'SELECT * FROM [dbo].[Orden] WHERE uniqueid = %s'
        result =  db.query(query,(uniqueid,))
        return result[0]
    
    @staticmethod
    def get_ordenservice_by_uniqueid(uniqueid):
        query = '''SELECT ordser.* FROM [dbo].[OrdenServicio] ordser
                LEFT JOIN [dbo].[Orden] ord ON ord.Id = ordser.OrdenId
                WHERE ord.uniqueid = %s'''
        data_result =  db.query(query,(uniqueid,))
        data_dict = [row._asdict() for row in data_result] if data_result else []
        return data_dict

    @staticmethod
    def getProductos():
        query = 'SELECT [ProductoID],[Descripcion],[GrupoID] FROM [dbo].[Producto]'
        data_result =  db.query(query)
        data_dict = [row._asdict() for row in data_result] if data_result else []
        return data_dict
    
    @staticmethod
    def searchPersoneria(search):
        searchTerm = f'%{search}%'
        query = 'SELECT [PersoneriaID], [Personeria] FROM [dbo].[Personeria] WHERE [Personeria] LIKE %s'
       
        data_result =  db.query(query,(searchTerm, ))
        data_dict = [row._asdict() for row in data_result] if data_result else []
        return data_dict
    
    @staticmethod
    def get_placa_personeria_id(PersoneriaID):
        query = 'SELECT [Placa] ,[Carreta] FROM [dbo].[PersoneriaVehiculo] WHERE [PersoneriaID] =  %s'       
        data_result =  db.query(query,(PersoneriaID, ))
        data_dict = [row._asdict() for row in data_result] if data_result else []
        return data_dict
    
    @staticmethod
    def get_direccion_personeria_id(PersoneriaID):
        query = '''SELECT pd.[DireccionID], u.[ubicacion], pd.[Direccion]     
                    FROM [dbo].[PersoneriaDireccion] pd
                    LEFT JOIN [dbo].[UBICACIONES] u ON pd.[UbicacionID] = u.[idubicacion]
                    WHERE pd.PersoneriaID = %s'''      
        data_result =  db.query(query,(PersoneriaID, ))
        data_dict = [row._asdict() for row in data_result] if data_result else []
        return data_dict
    
    @staticmethod
    def create(form_data):
        try :
            user_id = session.get('user_id')
            values = {
            'FechaProgramacion' :  form_data.get('FechaProgramacion', '').strip(),
            'TransportistaId' :  user_id,
            'Placa_Tracto' :  form_data.get('Placa_Tracto', '').strip(),
            'Placa_Carreta' : form_data.get('Placa_Carreta', '').strip(),
            'TransportistaServicioId' :  1, #form_data.get('TransportistaServicioId', '').strip()
            'ConductorLicencia' :  form_data.get('ConductorLicencia', '').strip(),
            'ConductorNombre' :  form_data.get('ConductorNombre', '').strip(),
            'Estado' : 1,
            'Author' : user_id
            }

            query = '''
                INSERT INTO [dbo].[Orden] 
                (FechaProgramacion, 
                TransportistaId, Placa_Tracto, Placa_Carreta, 
                TransportistaServicioId,  
                ConductorLicencia, ConductorNombre, Estado, Author)
                VALUES 
                (%(FechaProgramacion)s, 
                %(TransportistaId)s, %(Placa_Tracto)s, %(Placa_Carreta)s, 
                %(TransportistaServicioId)s,
                %(ConductorLicencia)s, %(ConductorNombre)s, %(Estado)s, %(Author)s);
            '''
            data = db.execute(query, ( values ))
            print(data)
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        
    @staticmethod
    def addservice(form_data):
        try :
            print(form_data)

            UniqueId = form_data.get('UniqueId', '').strip()
            query = 'SELECT * FROM [dbo].[Orden] WHERE uniqueid = %s'
            result =  db.query(query,(UniqueId,))

            print(result[0].Id)

            user_id = session.get('user_id')
            values = {
            'GuiaRemision' :  form_data.get('GuiaRemision', '').strip(),
            'GuiaTransportista' :  form_data.get('GuiaTransportista', '').strip(),
            'Peso' : form_data.get('Peso', '').strip(),
            'Volumen' :  form_data.get('Volumen', '').strip(),
            'Codigo' :  form_data.get('Codigo', '').strip(),
            'Descripcion' :  form_data.get('Descripcion', '').strip(),
            'Author' : user_id,
            'OrdenId': result[0].Id
            }


            query = '''
                INSERT INTO [dbo].[OrdenServicio] 
                (GuiaRemision, 
                GuiaTransportista, Peso, Volumen, 
                Codigo,  
                Descripcion, OrdenId, Author)
                VALUES 
                (%(GuiaRemision)s, 
                %(GuiaTransportista)s, %(Peso)s, %(Volumen)s, 
                %(Codigo)s,
                %(Descripcion)s, %(OrdenId)s, %(Author)s);
            '''
            data = db.execute(query, ( values ))
            print(data)
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
        

    @staticmethod
    def get_table(request):
        try:
            # Obtener y limpiar parámetros DataTables
            draw = int(request.get('draw', 1))
            start = int(request.get('start', 0))
            length = int(request.get('length', 10))
            search_value = request.get('search', '').strip()

            # Construcción segura de la cláusula WHERE y parámetros
            where_clause = "WHERE os.TransportistaId = %(TransportistaId)s "
            TransportistaId = session.get('user_id')
            params = {'start': start, 'length': length, 'TransportistaId':TransportistaId}

            

            if search_value:
                where_clause = """
                    AND ( os.GuiaRemision LIKE %(search)s 
                       OR os.GuiaTransportista LIKE %(search)s )
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
                    FORMAT(os.[FechaProgramacion], 'HH:mm') AS FechaProgramacion,
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