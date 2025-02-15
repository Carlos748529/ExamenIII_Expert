# app.py

import utils_patch  # noqa

from flask import Flask, request, jsonify, render_template
from diagnostico import DiagnosticoEngine, Sintoma
import requests

app = Flask(__name__)

def get_medline_info(condition):
    """Obtiene información adicional de MedlinePlus"""
    api_url = f"https://connect.medlineplus.gov/service?mainSearchCriteria.v.cs=2.16.840.1.113883.6.103&mainSearchCriteria.v.c={condition}&knowledgeResponseType=application/json"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    """
    Endpoint que recibe un JSON con los síntomas y devuelve un diagnóstico.
    
    Ejemplo de JSON de entrada:
    {
        "fiebre": true,
        "tos": true,
        "dolor_garganta": true,
        "dolor_abdominal": false,
        "nauseas": false,
        "vomito": false,
        "erupcion": false
    }
    """
    datos = request.get_json()

    # Crear y preparar el motor experto.
    engine = DiagnosticoEngine()
    engine.reset()

    # Declarar los hechos (síntomas) en el motor.
    engine.declare(Sintoma(**datos))
    engine.run()

    # Obtener diagnóstico
    if engine.resultado:
        diagnostico = engine.resultado
        # Obtener información adicional de MedlinePlus
        info_adicional = get_medline_info(diagnostico)
    else:
        diagnostico = "No se pudo determinar un diagnóstico con la información proporcionada."
        info_adicional = None

    return jsonify({
        'diagnostico': diagnostico,
        'info_adicional': info_adicional
    })

if __name__ == '__main__':
    app.run(debug=True)
