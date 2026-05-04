"""
API Web para el Validador de Secuencias Biológicas.
Sirve una interfaz web para validar archivos FASTA con visualización de resultados.
"""

import os
import sys
import json

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from lector_fasta import leer_registros_fasta
from orf import validar_registro
from modelos import RegistroFasta

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    """Sirve la página principal."""
    return render_template('index.html')


@app.route('/api/validar', methods=['POST'])
def validar():
    """
    Endpoint para validar secuencias FASTA.
    Recibe un archivo FASTA y retorna los resultados de validación en JSON.
    """
    try:
        # Verificar que se envió un archivo
        if 'archivo' not in request.files:
            return jsonify({'error': 'No se envió archivo'}), 400

        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'Archivo sin nombre'}), 400

        # Guardar temporalmente el archivo
        temp_path = f'/tmp/{archivo.filename}'
        archivo.save(temp_path)

        # Leer y validar registros
        registros = leer_registros_fasta(temp_path)
        resultados = [validar_registro(registro) for registro in registros]

        # Convertir resultados a formato JSON serializable
        datos_resultados = []
        for resultado in resultados:
            datos_resultados.append({
                'nombre_registro': resultado.nombre_registro,
                'secuencia': resultado.secuencia,
                'es_valida': resultado.es_valida,
                'motivo': resultado.motivo,
                'coincidencias': {
                    'posiciones_atg': resultado.coincidencias.posiciones_atg,
                    'posiciones_taa': resultado.coincidencias.posiciones_taa,
                    'posiciones_tag': resultado.coincidencias.posiciones_tag,
                    'posiciones_tga': resultado.coincidencias.posiciones_tga,
                },
                'recorrido_afd': {
                    'aceptada': resultado.recorrido_afd.aceptada,
                    'estado_final': resultado.recorrido_afd.estado_final,
                    'estados_visitados': resultado.recorrido_afd.estados_visitados,
                }
            })

        # Eliminar archivo temporal
        os.remove(temp_path)

        return jsonify({
            'exito': True,
            'total_registros': len(resultados),
            'total_validas': sum(1 for r in resultados if r.es_valida),
            'resultados': datos_resultados
        })

    except FileNotFoundError as e:
        return jsonify({'error': f'Error al leer archivo: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al procesar: {str(e)}'}), 500


@app.route('/api/validar-secuencia', methods=['POST'])
def validar_secuencia():
    """
    Endpoint para validar una secuencia individual.
    Recibe JSON con nombre y secuencia, retorna resultados de validación.
    """
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({'error': 'No se envió datos JSON'}), 400

        nombre = datos.get('nombre', 'Secuencia_sin_nombre').strip()
        secuencia = datos.get('secuencia', '').strip().upper()

        if not nombre:
            return jsonify({'error': 'El nombre de la secuencia es requerido'}), 400

        if not secuencia:
            return jsonify({'error': 'La secuencia es requerida'}), 400

        # Crear registro FASTA y validar
        registro = RegistroFasta(nombre=nombre, secuencia=secuencia)
        resultado = validar_registro(registro)

        # Convertir resultado a formato JSON serializable
        datos_resultado = {
            'nombre_registro': resultado.nombre_registro,
            'secuencia': resultado.secuencia,
            'es_valida': resultado.es_valida,
            'motivo': resultado.motivo,
            'coincidencias': {
                'posiciones_atg': resultado.coincidencias.posiciones_atg,
                'posiciones_taa': resultado.coincidencias.posiciones_taa,
                'posiciones_tag': resultado.coincidencias.posiciones_tag,
                'posiciones_tga': resultado.coincidencias.posiciones_tga,
            },
            'recorrido_afd': {
                'aceptada': resultado.recorrido_afd.aceptada,
                'estado_final': resultado.recorrido_afd.estado_final,
                'estados_visitados': resultado.recorrido_afd.estados_visitados,
            }
        }

        return jsonify({
            'exito': True,
            'resultado': datos_resultado
        })

    except Exception as e:
        return jsonify({'error': f'Error al procesar: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
