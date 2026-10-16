"""
<<<<<<< Updated upstream
EduLink — Backend Developer 1
Servidor Flask principal. Puerto: 5000.

Estado de dependencias externas:
  - database.py : VACÍO — se usan mocks internos (ver sección MOCKS).
  - validator.py : VACÍO — validación implementada localmente (ver sección VALIDACIÓN).

Cuando el DB Developer entregue database.py, reemplaza las funciones marcadas
con "# TODO: reemplazar mock" por los imports reales.
=======
EduLink — Backend v0.2
Nuevos endpoints: respuestas + marcar resuelta.
>>>>>>> Stashed changes
"""

import logging
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

<<<<<<< Updated upstream
app = Flask(__name__, static_folder=FRONTEND_DIR)

# CORS restringido a localhost (seguridad acordada en bob_context.md)
=======
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
>>>>>>> Stashed changes
CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

<<<<<<< Updated upstream
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
=======
from database import init_db, insertar_solicitud, obtener_solicitudes, \
                     marcar_resuelta, insertar_respuesta, obtener_respuestas
from validator import validate_solicitud
>>>>>>> Stashed changes

# ── Frontend ───────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# ── Solicitudes ────────────────────────────────────────────

@app.route('/api/solicitudes', methods=['GET'])
<<<<<<< Updated upstream
def obtener_solicitudes():
    """Devuelve todas las solicitudes almacenadas."""
    try:
        solicitudes = get_all_solicitudes()
        return jsonify({"solicitudes": solicitudes}), 200
=======
def get_solicitudes():
    try:
        return jsonify({"solicitudes": obtener_solicitudes()}), 200
>>>>>>> Stashed changes
    except Exception:
        logger.exception("Error al obtener solicitudes")
        return jsonify({"error": "No se pudieron obtener las solicitudes."}), 500


@app.route('/api/solicitudes', methods=['POST'])
def crear_solicitud():
    data = request.get_json(silent=True)
    if data is None:
<<<<<<< Updated upstream
        return jsonify({"error": "El cuerpo de la petición debe ser JSON válido."}), 400

    error = _validate_solicitud(data)
=======
        return jsonify({"error": "El cuerpo debe ser JSON válido."}), 400
    error = validate_solicitud(data)
>>>>>>> Stashed changes
    if error:
        return jsonify({"error": error}), 400
    try:
<<<<<<< Updated upstream
        nueva = insert_solicitud(
            nombre=data["nombre"].strip(),
            carrera=data["carrera"].strip(),
            materia=data["materia"].strip(),
            descripcion=data["descripcion"].strip(),
=======
        nuevo_id = insertar_solicitud(
            data["nombre"].strip(), data["carrera"].strip(),
            data["materia"].strip(), data["descripcion"].strip(),
>>>>>>> Stashed changes
        )
        return jsonify(nueva), 201
    except Exception:
        logger.exception("Error al insertar solicitud")
        return jsonify({"error": "No se pudo registrar la solicitud."}), 500


@app.route('/api/solicitudes/<int:sid>/resolver', methods=['POST'])
def resolver_solicitud(sid):
    """Marca la solicitud como resuelta."""
    if marcar_resuelta(sid):
        return jsonify({"mensaje": "Solicitud marcada como resuelta."}), 200
    return jsonify({"error": "Solicitud no encontrada."}), 404

# ── Respuestas ─────────────────────────────────────────────

@app.route('/api/solicitudes/<int:sid>/respuestas', methods=['GET'])
def get_respuestas(sid):
    try:
        return jsonify({"respuestas": obtener_respuestas(sid)}), 200
    except Exception:
        logger.exception("Error al obtener respuestas")
        return jsonify({"error": "No se pudieron obtener las respuestas."}), 500


@app.route('/api/solicitudes/<int:sid>/respuestas', methods=['POST'])
def crear_respuesta(sid):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo debe ser JSON válido."}), 400
    nombre = (data.get("nombre") or "").strip()
    texto  = (data.get("texto")  or "").strip()
    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400
    if not texto:
        return jsonify({"error": "El campo 'texto' es obligatorio."}), 400
    if len(nombre) > 50:
        return jsonify({"error": "'nombre' máx. 50 caracteres."}), 400
    if len(texto) > 500:
        return jsonify({"error": "'texto' máx. 500 caracteres."}), 400
    try:
        rid = insertar_respuesta(sid, nombre, texto)
        return jsonify({"mensaje": "Respuesta publicada.", "id": rid}), 201
    except Exception:
        logger.exception("Error al insertar respuesta")
        return jsonify({"error": "No se pudo registrar la respuesta."}), 500

# ── Arranque ───────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
<<<<<<< Updated upstream
    logger.info("Servidor EduLink iniciando en http://localhost:5000")
    app.run(host='localhost', port=5000, debug=False)
=======
    logger.info("Servidor EduLink v0.2 en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
>>>>>>> Stashed changes
