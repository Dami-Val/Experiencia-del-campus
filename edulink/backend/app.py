"""
EduLink — Backend
Servidor Flask principal. Puerto: 5000.
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

app = Flask(__name__, static_folder=FRONTEND_DIR)

# CORS restringido a localhost (seguridad acordada en bob_context.md)
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
from validator import validate_solicitud

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
        return jsonify({"error": "No se pudieron obtener las solicitudes."}), 500


@app.route('/api/solicitudes', methods=['POST'])
def crear_solicitud():
    """Crea una nueva solicitud tras validar los campos obligatorios."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON válido."}), 400

    error = validate_solicitud(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        nuevo_id = insertar_solicitud(
            nombre=data["nombre"].strip(),
            carrera=data["carrera"].strip(),
            materia=data["materia"].strip(),
            descripcion=data["descripcion"].strip(),
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
    logger.info("Servidor EduLink iniciando en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
