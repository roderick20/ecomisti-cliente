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
        query = '''SELECT ordser.*, per.* FROM [dbo].[OrdenServicio] ordser
LEFT JOIN [dbo].[Orden] ord ON ord.Id = ordser.OrdenId
LEFT JOIN [dbo].[Personeria] per ON ordser.ClienteId = per.PersoneriaID
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
            'TransportistaServicioId' :  form_data.get('TransportistaServicioId', '').strip(),
            'ConductorLicencia' :  form_data.get('ConductorLicencia', '').strip(),
            'ConductorNombre' :  form_data.get('ConductorNombre', '').strip(),
            'Estado' : 1,
            'Author' : user_id
            }

            print(values)

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
            'OrdenId': result[0].Id,
            'ClienteId':  form_data.get('ClienteId', '').strip(),
            }


            query = '''
                INSERT INTO [dbo].[OrdenServicio] 
                (GuiaRemision, 
                GuiaTransportista, Peso, Volumen, 
                Codigo,  
                Descripcion, OrdenId, Author, ClienteId)
                VALUES 
                (%(GuiaRemision)s, 
                %(GuiaTransportista)s, %(Peso)s, %(Volumen)s, 
                %(Codigo)s,
                %(Descripcion)s, %(OrdenId)s, %(Author)s, %(ClienteId)s);
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
                    FORMAT(os.[FechaRecepcion], 'yyyy-MM-dd') AS FechaRecepcion,
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
                    FORMAT(os.[FechaProgramacion], 'yyyy-MM-dd') AS FechaProgramacion,
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
        
    @staticmethod
    def get_by_numero_doc(numero_doc):
        try:
            query = """
                SELECT  *
                FROM [dbo].[Personeria] 
                WHERE NroIdentidad =  %s
            """
            data = db.query(query,(numero_doc,))

            query = """
                SELECT [DireccionID], [Direccion]
                FROM [dbo].[PersoneriaDireccion] 
                WHERE PersoneriaID =  %s
            """
            direccion = db.query(query,(data[0].PersoneriaID,))

            return { "success": True, "data": data, "direccion":direccion }
        except Exception as error:
            return { "success": False, "error": str(error) }   
        

    # @staticmethod
    # def create_ruc(razon_social, numero_doc, direccion, ubigeo):
    #     print('create_ruc')
    #     try:
    #         creado_por = session['user_id']            
    #         query = """
    #             INSERT INTO personeria
    #                 (Personeria, NombreComercial, TipoIdentidadID, NroIdentidad, GrupoPersoneria, Domiciliado,TipoContribuyente,FamiliaID,NegocioID,CtaDetraccion,
    #                 Codigo,Estado,UsuarioID,ConvenioID,MedioRegistroID,MedioInformacionID,Referencia,Telefonos,email)
    #             VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    #                     %s, %s, %s, %s, %s, %s, %s, %s, %s)  
    #         """
    #         data = db.execute(query, ( 
    #             razon_social, razon_social, '203.00002', numero_doc, '101000', 1, 0,'143.00000','179.00000','',
    #             '',1,1,'902.00001','900.00001','901.00002','','',''))
    #         print(data)
    #         return { "success": True, "data": data }
    #     except Exception as error:
    #         print(error)
    #         return { "success": False, "error": str(error) }

    @staticmethod
    def create_ruc(razon_social, numero_doc, direccion, ubigeo):
        print('create_ruc')
        try:
            creado_por = session['user_id']

            query = """
                INSERT INTO personeria (
                    Personeria, NombreComercial, TipoIdentidadID, NroIdentidad, 
                    GrupoPersoneria, Domiciliado, TipoContribuyente, FamiliaID, 
                    NegocioID, CtaDetraccion, Codigo, Estado, UsuarioID, ConvenioID, 
                    MedioRegistroID, MedioInformacionID, Referencia, Telefonos, email
                )
                
                VALUES (
                    %(Personeria)s, %(NombreComercial)s, %(TipoIdentidadID)s, %(NroIdentidad)s,
                    %(GrupoPersoneria)s, %(Domiciliado)s, %(TipoContribuyente)s, %(FamiliaID)s,
                    %(NegocioID)s, %(CtaDetraccion)s, %(Codigo)s, %(Estado)s, %(UsuarioID)s, %(ConvenioID)s,
                    %(MedioRegistroID)s, %(MedioInformacionID)s, %(Referencia)s, %(Telefonos)s, %(email)s
                );
            """

            params = {
                'Personeria': razon_social,
                'NombreComercial': razon_social,
                'TipoIdentidadID': '203.00002',
                'NroIdentidad': numero_doc,
                'GrupoPersoneria': '101000',
                'Domiciliado': 1,
                'TipoContribuyente': 0,
                'FamiliaID': '143.00000',
                'NegocioID': '179.00000',
                'CtaDetraccion': '',
                'Codigo': '',
                'Estado': 1,
                'UsuarioID': 1,
                'ConvenioID': '902.00001',
                'MedioRegistroID': '900.00001',
                'MedioInformacionID': '901.00002',
                'Referencia': direccion or '',
                'Telefonos': '',
                'email': ''
            }

            db.execute(query, params)
            #-------------------------------------------------
            query = """
                SELECT  *
                FROM [dbo].[Personeria] 
                WHERE NroIdentidad =  %s
            """
            data = db.query(query,(numero_doc,))
            #------------------------------------------------
            query = """
                INSERT INTO [dbo].[PersoneriaDireccion] (
                    [PersoneriaID],[DireccionID],[PaisID],[UbicacionID],[ViaID]
                    ,[NombreVia],[NumeroVia],[InteriorVia],[ZonaID],[NombreZona]
                    ,[Direccion],[Telefonos],[Email],[ZonaRutaID],[Secuencia]
                    ,[Coordenada],[Estado],[UsuarioID]
                )
                
                VALUES (
                    %(PersoneriaID)s,%(DireccionID)s,%(PaisID)s,%(UbicacionID)s,%(ViaID)s
                    ,%(NombreVia)s,%(NumeroVia)s,%(InteriorVia)s,%(ZonaID)s,%(NombreZona)s
                    ,%(Direccion)s,%(Telefonos)s,%(Email)s,%(ZonaRutaID)s,%(Secuencia)s
                    ,%(Coordenada)s,%(Estado)s,%(UsuarioID)s
                );
            """
            PersoneriaID = data[0].PersoneriaID
            params = {
                'PersoneriaID': PersoneriaID,
                'DireccionID': ubigeo,
                'PaisID': '204.00000',
                'UbicacionID': '010101',
                'ViaID': '135.00000',

                'NombreVia': '',
                'NumeroVia': '',
                'InteriorVia': '',
                'ZonaID': '136.00000',
                'NombreZona': '',

                'Direccion': direccion,
                'Telefonos': '',
                'Email': '',
                'ZonaRutaID': '180.00000',
                'Secuencia': 1,

                'Coordenada': '',
                'Estado': 1,
                'UsuarioID': 1
            }

            db.execute(query, params)

            #-------------------------------------------------
            query = """
                SELECT [DireccionID], [Direccion]
                FROM [dbo].[PersoneriaDireccion] 
                WHERE PersoneriaID =  %s
            """
            data = db.query(query,(PersoneriaID,))
            #------------------------------------------------
            if data:
                return {"success": True, "data": data, "PersoneriaID": PersoneriaID}
            else:
                return {"success": False, "error": "No se devolvió el ID del nuevo registro"}

        except Exception as error:
            print("Error en create_ruc:", error)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_dni(razon_social, numero_doc):
        try:
            #razon_social = form_data.get('razon_social', '').strip()
            nombre_comercial =  ''# form_data.get('nombre_comercial', '').strip()
            tipo_doc = 1 #form_data.get('tipo_doc', '').strip()
            
            #numero_doc =  form_data.get('numero_doc', '').strip()
            personeria_tipo = 1 #form_data.get('personeria_tipo', '').strip()
            contacto =   ''#form_data.get('contacto', '').strip()
            telefono =  ''#form_data.get('telefono', '').strip()
            email =  ''# form_data.get('email', '').strip()
            cuenta_detraccion =  ''#form_data.get('cuenta_detraccion', '').strip()
            cuenta_cci =  ''#form_data.get('cuenta_cci', '').strip()

            direccion = ''
            ubigeo =  ''

            creado_por = session['user_id']            
            query = """
                INSERT INTO personeria
                    (razon_social, nombre_comercial, tipo_doc, numero_doc,
                    personeria_tipo, contacto, telefono, email,
                    cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por)
                VALUES( %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s)  
            """
            data = db.execute(query, ( razon_social, nombre_comercial, tipo_doc, numero_doc, 
                                       personeria_tipo, contacto, telefono, email,
                                       cuenta_detraccion, cuenta_cci, direccion, ubigeo, creado_por))
            return { "success": True, "data": data }
        except Exception as error:
            print(error)
            return { "success": False, "error": str(error) }
