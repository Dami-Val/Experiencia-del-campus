"""
EduLink — Backend Developer 1
Servidor Flask principal. Puerto: 5000.

Estado de dependencias externas:
  - database.py : VACÍO — se usan mocks internos (ver sección MOCKS).
  - validator.py : VACÍO — validación implementada localmente (ver sección VALIDACIÓN).

Cuando el DB Developer entregue database.py, reemplaza las funciones marcadas
con "# TODO: reemplazar mock" por los imports reales.
"""

import logging
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

# ---------------------------------------------------------------------------
# Configuración de la aplicación
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

# CORS restringido a localhost (seguridad acordada en bob_context.md)
CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MOCKS TEMPORALES
# Sustituir por imports de database.py cuando ese archivo esté implementado.
#
#   from database import init_db, get_all_solicitudes, insert_solicitud
#
# ---------------------------------------------------------------------------

_mock_store: list[dict] = []          # almacén en memoria (sin persistencia)
_mock_next_id: int = 1


def _mock_init_db() -> None:
    """TODO: reemplazar mock — llamar a database.init_db() en su lugar."""
    logger.info("MOCK: base de datos en memoria inicializada.")


def _mock_get_all_solicitudes() -> list[dict]:
    """TODO: reemplazar mock — llamar a database.get_all_solicitudes()."""
    return list(_mock_store)


def _mock_insert_solicitud(nombre: str, carrera: str, materia: str, descripcion: str) -> dict:
    """TODO: reemplazar mock — llamar a database.insert_solicitud(...)."""
    global _mock_next_id
    nueva = {
        "id": _mock_next_id,
        "nombre": nombre,
        "carrera": carrera,
        "materia": materia,
        "descripcion": descripcion,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }
    _mock_store.append(nueva)
    _mock_next_id += 1
    logger.info("MOCK: solicitud insertada con id=%s", nueva["id"])
    return nueva


# Alias activos — cambiar a los de database.py cuando estén disponibles
init_db             = _mock_init_db
get_all_solicitudes = _mock_get_all_solicitudes
insert_solicitud    = _mock_insert_solicitud

# ---------------------------------------------------------------------------
# VALIDACIÓN
# Cuando validator.py esté implementado, reemplazar _validate_solicitud
# por: from validator import validate_solicitud
# ---------------------------------------------------------------------------

CARRERAS_VALIDAS = {"IE", "IM", "IS", "IME"}

def _validate_solicitud(data: dict) -> str | None:
    """
    Valida los campos del contrato (bob_context.md).
    Devuelve un mensaje de error (str) si hay problema, o None si todo está bien.
    TODO: reemplazar por validator.validate_solicitud(data) cuando esté listo.
    """
    campos = {
        "nombre":      50,
        "carrera":     None,
        "materia":     100,
        "descripcion": 500,
    }
    for campo, max_len in campos.items():
        valor = data.get(campo, "").strip() if isinstance(data.get(campo), str) else ""
        if not valor:
            return f"El campo '{campo}' es obligatorio."
        if max_len and len(valor) > max_len:
            return f"El campo '{campo}' no puede superar {max_len} caracteres."
    if data.get("carrera") not in CARRERAS_VALIDAS:
        return "El campo 'carrera' debe ser uno de: IE, IM, IS, IME."
    return None

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
def obtener_solicitudes():
    """Devuelve todas las solicitudes almacenadas."""
    try:
        solicitudes = get_all_solicitudes()
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

    error = _validate_solicitud(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        nueva = insert_solicitud(
            nombre=data["nombre"].strip(),
            carrera=data["carrera"].strip(),
            materia=data["materia"].strip(),
            descripcion=data["descripcion"].strip(),
        )
        return jsonify(nueva), 201
    except Exception:
        logger.exception("Error al insertar solicitud")
        return jsonify({"error": "No se pudo registrar la solicitud."}), 500


# ---------------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    init_db()
    logger.info("Servidor EduLink iniciando en http://localhost:5000")
    app.run(host='localhost', port=5000, debug=False)
