# -*- coding: utf-8 -*-
"""
EduLink — Backend
Servidor Flask principal. Puerto: 5000.

SEGURIDAD implementada en este archivo:
  - CORS restringido a localhost (no wildcard).
  - Cabeceras de seguridad HTTP en cada respuesta:
      Content-Security-Policy, X-Content-Type-Options, X-Frame-Options,
      Referrer-Policy, Permissions-Policy.
  - debug=False — nunca expone traceback al cliente.
  - Excepciones capturadas: solo se devuelve mensaje genérico al cliente;
    el detalle queda en el log del servidor.
  - host='127.0.0.1' — solo accesible desde la misma máquina.
  - Los campos se sanean en validator.sanitize_field() antes de persistir.
"""

import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

# ---------------------------------------------------------------------------
# Configuración de la aplicación
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

# CORS restringido a localhost únicamente — nunca usar origins='*' en producción
CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Imports de módulos del proyecto
# ---------------------------------------------------------------------------

from database import init_db, insertar_solicitud, obtener_solicitudes
from validator import validate_solicitud, sanitize_field

# ---------------------------------------------------------------------------
# Cabeceras de seguridad HTTP — aplicadas a TODAS las respuestas
# ---------------------------------------------------------------------------

@app.after_request
def add_security_headers(response):
    """
    Añade cabeceras de seguridad HTTP en cada respuesta.

    CSP: solo permite recursos del mismo origen; bloquea scripts inline
         y recursos externos (protección XSS + data injection).
    X-Content-Type-Options: evita MIME-type sniffing.
    X-Frame-Options: impide que la página sea embebida en un iframe (clickjacking).
    Referrer-Policy: no filtra la URL del servidor en cabeceras Referer.
    Permissions-Policy: deshabilita APIs de hardware no requeridas.
    """
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# ---------------------------------------------------------------------------
# Rutas — Frontend
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Sirve index.html desde la carpeta frontend."""
    return send_from_directory(FRONTEND_DIR, 'index.html')

# ---------------------------------------------------------------------------
# Rutas — API
# ---------------------------------------------------------------------------

@app.route('/api/solicitudes', methods=['GET'])
def get_solicitudes():
    """Devuelve todas las solicitudes almacenadas."""
    try:
        solicitudes = obtener_solicitudes()
        return jsonify({"solicitudes": solicitudes}), 200
    except Exception:
        logger.exception("Error al obtener solicitudes")
        # No se expone el detalle del error al cliente
        return jsonify({"error": "No se pudieron obtener las solicitudes."}), 500


@app.route('/api/solicitudes', methods=['POST'])
def crear_solicitud():
    """Crea una nueva solicitud tras validar y sanear los campos."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON válido."}), 400

    error = validate_solicitud(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        # sanitize_field() elimina etiquetas HTML antes de persistir (anti-XSS almacenado)
        nuevo_id = insertar_solicitud(
            nombre=sanitize_field(data["nombre"]),
            carrera=data["carrera"].strip(),          # carrera validada por whitelist
            materia=sanitize_field(data["materia"]),
            descripcion=sanitize_field(data["descripcion"]),
        )
        return jsonify({"mensaje": "Solicitud creada exitosamente.", "id": nuevo_id}), 201
    except Exception:
        logger.exception("Error al insertar solicitud")
        return jsonify({"error": "No se pudo registrar la solicitud."}), 500


# ---------------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    init_db()
    logger.info("Servidor EduLink iniciando en http://127.0.0.1:5000")
    # host='127.0.0.1' — solo accesible localmente, no expuesto en red
    # debug=False — nunca enviar tracebacks al navegador
    app.run(host='127.0.0.1', port=5000, debug=False)
