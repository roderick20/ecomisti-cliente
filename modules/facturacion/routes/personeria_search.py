from flask import Flask, jsonify
import requests
import os

from modules.facturacion.models.personeria_model import Personeria

from .. import bp 

# Reemplaza esto con tu token real o usa una variable de entorno
TOKEN_RUC_DNI = 'sk_8793.rOQ48irZfIsXJQGHh3NJ4lKbs7gNgsXb'

@bp.route('/personeria/search_dni/<numero>', methods=['GET'])
def search_dni(numero):
    print(f"Este es el numero: {numero}")


    personeria = Personeria.get_by_numero_doc(numero)

    if len(personeria['data']) == 1 :        
        return jsonify({
            "razon_social": personeria['data'][0].razon_social,
            "personeria_id": personeria['data'][0].id
        })
    
    else:

        headers = {'Authorization': f'Bearer {TOKEN_RUC_DNI}'}

        try:
            # Intentar con API v1 (RENIEC - DNI)
            apiUrlV1 = f"https://api.decolecta.com/v1/reniec/dni?numero={numero}"
            response_v1 = requests.get(apiUrlV1, headers=headers, timeout=10)
            if response_v1.status_code == 200:
                empresa = response_v1.json()
                print(empresa)

                razon_social = empresa.get("first_last_name") +" "+empresa.get("second_last_name") +" "+  empresa.get("first_name")


                personeria = Personeria.create_dni(
                razon_social, 
                empresa.get("numero_documento", numero))
            
                print(personeria['data'])
                return jsonify({
                    "razon_social": razon_social,
                    # "tipoDocumento": empresa.get("TipoIdentidadID", ""),
                    # "numeroDocumento": empresa.get("numero_documento", numero),
                    # #"GrupoPersoneria": empresa.get("GrupoPersoneria", ""),
                    # "estado": empresa.get("estado", ""),
                    # "condicion": empresa.get("condicion", ""),
                    # "direccion": empresa.get("direccion", ""),
                    # "ubigeo": empresa.get("ubigeo", ""),
                    # "viaTipo": empresa.get("viaTipo", ""),
                    # "viaNombre": empresa.get("viaNombre", ""),
                    # "zonaCodigo": empresa.get("zonaCodigo", ""),
                    "personeria_id": personeria['data']
                })
            else:
                raise Exception("No encontrado en v1")

        except Exception as e:
            print(f"Error en API v1: {e}")
            # Devolver respuesta por defecto si no se encuentra
            return jsonify({
                "razon_social": "DNI no encontrado",
                "personeria_id": 0
            })

        # Este punto no debería alcanzarse, pero por seguridad:
        return jsonify({"error": "No se pudo obtener información"}), 500


@bp.route('/personeria/search_ruc/<numero>', methods=['GET'])
def search_ruc(numero):
    print(f"Consultando RUC: {numero}")

    personeria = Personeria.get_by_numero_doc(numero)

    if len(personeria['data']) == 1 :        
        return jsonify({
            "razon_social": personeria['data'][0].razon_social,
            "personeria_id": personeria['data'][0].id
        })
    
    else:
        headers = {'Authorization': f'Bearer {TOKEN_RUC_DNI}'}

        try:
            # Intentar con API v2 (SUNAT - RUC)
            apiUrlV2 = f"https://api.decolecta.com/v1/sunat/ruc?numero={numero}"
            response_v2 = requests.get(apiUrlV2, headers=headers, timeout=10)

            if response_v2.status_code == 200:
                empresa = response_v2.json()
            else:
                print("RUC no encontrado en API v2.")
                empresa = {}

            personeria = Personeria.create_ruc(
                empresa.get("razon_social", ""), 
                empresa.get("numero_documento", numero), 
                empresa.get("direccion", ""), 
                empresa.get("ubigeo", ""))
            
            print(personeria['data'])
            return jsonify({
                "razon_social": empresa.get("razon_social", ""),
                # "tipoDocumento": empresa.get("TipoIdentidadID", ""),
                # "numeroDocumento": empresa.get("numero_documento", numero),
                # #"GrupoPersoneria": empresa.get("GrupoPersoneria", ""),
                # "estado": empresa.get("estado", ""),
                # "condicion": empresa.get("condicion", ""),
                # "direccion": empresa.get("direccion", ""),
                # "ubigeo": empresa.get("ubigeo", ""),
                # "viaTipo": empresa.get("viaTipo", ""),
                # "viaNombre": empresa.get("viaNombre", ""),
                # "zonaCodigo": empresa.get("zonaCodigo", ""),
                "personeria_id": personeria['data']
            })

        except Exception as e:
            print(f"Error en controlador /personerias/searchRuc: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500


