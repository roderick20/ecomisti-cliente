import requests
import base64
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_HALF_UP
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app



class SunatModel:

    @staticmethod
    def save_file(filename, content, encoding='utf-8'):
        """Guarda un archivo en el sistema"""
        sunat_dir = os.path.join(current_app.root_path, 'static', 'sunat')
        # Crear directorio si no existe
        os.makedirs(sunat_dir, exist_ok=True)
        file_path = os.path.join(sunat_dir, filename)
        try:
            if encoding == 'base64':
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(content))
            else:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(content)
            return True
        except Exception as e:
            print(f"Error al guardar archivo: {str(e)}")
            return False

    @staticmethod
    def send_invoice_venta(invoice_data):
        LYCET_API_URL = 'http://lycet2.agilecorp.net.pe/api/v1/invoice/send?token=123456'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(LYCET_API_URL, json=invoice_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {str(e)}")
            raise

    @staticmethod
    def send_invoice_nota(invoice_data):
        LYCET_API_URL = 'http://lycet2.agilecorp.net.pe/api/v1/note/send?token=123456'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(LYCET_API_URL, json=invoice_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {str(e)}")
            raise

    @staticmethod
    def getValor(list, nombre):
        resultado = [row for row in list if row.codigo == nombre]
        return resultado[0].valor

    @staticmethod
    def numero_a_soles(monto):
        """
        Convierte un número (int o float) a su representación en letras en soles (PEN).
        Ej: 118.0 → "SON CIENTO DIECIOCHO CON 00/100 SOLES"
        """
        if isinstance(monto, float):
            entero = int(monto)
            centavos = round((monto - entero) * 100)
        elif isinstance(monto, int):
            entero = monto
            centavos = 0
        else:
            raise ValueError("El monto debe ser int o float")

        if entero < 0:
            raise ValueError("Monto negativo no soportado")

        # --- Números en letras (hasta 999'999'999) ---
        unidades = [
            "", "UN", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE",
            "DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISÉIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"
        ]
        
        decenas = [
            "", "", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"
        ]
        
        centenas = [
            "", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS",
            "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"
        ]

        def convertir_tres_digitos(n):
            if n == 0:
                return ""
            if n < 20:
                return unidades[n]
            elif n < 100:
                d = n // 10
                u = n % 10
                if u == 0:
                    return decenas[d]
                elif d == 2:
                    return f"VEINTI{unidades[u]}"
                else:
                    return f"{decenas[d]} Y {unidades[u]}"
            else:  # n < 1000
                c = n // 100
                resto = n % 100
                if n == 100:
                    return "CIEN"
                elif resto == 0:
                    return centenas[c]
                else:
                    return f"{centenas[c]} {convertir_tres_digitos(resto)}"

        if entero == 0:
            parte_entera = "CERO"
        else:
            # Dividir en grupos de miles
            millones = entero // 1_000_000
            miles = (entero % 1_000_000) // 1_000
            unidades_parte = entero % 1_000

            partes = []

            if millones:
                if millones == 1:
                    partes.append("UN MILLÓN")
                else:
                    partes.append(f"{convertir_tres_digitos(millones)} MILLONES")

            if miles:
                if miles == 1:
                    partes.append("MIL")
                else:
                    partes.append(f"{convertir_tres_digitos(miles)} MIL")

            if unidades_parte:
                partes.append(convertir_tres_digitos(unidades_parte))
            elif not millones and not miles:
                partes.append("CERO")

            parte_entera = " ".join(partes)

        # Formato final
        centavos_str = f"{centavos:02d}"
        return f"SON {parte_entera} CON {centavos_str}/100 SOLES"
