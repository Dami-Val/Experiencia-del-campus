"""
database.py — EduLink v0.1
Conexión SQLite y funciones CRUD para la tabla `solicitudes`.
DB Developer · Contrato de datos: contrato.md
"""

import sqlite3
import os

# Ruta al archivo de base de datos, junto a este módulo
DB_PATH = os.path.join(os.path.dirname(__file__), "edulink.db")


def get_connection():
    """Devuelve una conexión SQLite con row_factory para acceso por nombre de columna."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea la tabla `solicitudes` si no existe. Llamar al iniciar el servidor."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes (
                id             INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre         TEXT     NOT NULL CHECK(length(nombre) <= 50),
                carrera        TEXT     NOT NULL CHECK(carrera IN ('IE', 'IM', 'IS', 'IME')),
                materia        TEXT     NOT NULL CHECK(length(materia) <= 100),
                descripcion    TEXT     NOT NULL CHECK(length(descripcion) <= 500),
                fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


def insertar_solicitud(nombre: str, carrera: str, materia: str, descripcion: str) -> int:
    """
    Inserta una nueva solicitud en la base de datos.

    Parámetros
    ----------
    nombre      : Nombre del estudiante (máx. 50 chars).
    carrera     : Clave de carrera — 'IE', 'IM', 'IS' o 'IME'.
    materia     : Nombre de la materia (máx. 100 chars).
    descripcion : Descripción del problema (máx. 500 chars).

    Retorna
    -------
    El `id` (INTEGER) de la fila recién creada.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO solicitudes (nombre, carrera, materia, descripcion)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, carrera, materia, descripcion),
        )
        conn.commit()
        assert cursor.lastrowid is not None
        return cursor.lastrowid
    finally:
        conn.close()


def obtener_solicitudes() -> list[dict]:
    """
    Devuelve todas las solicitudes ordenadas por `fecha_creacion` DESC.

    Retorna
    -------
    Lista de diccionarios con las claves:
        id, nombre, carrera, materia, descripcion, fecha_creacion
    `fecha_creacion` se serializa como string ISO-8601 (YYYY-MM-DDTHH:MM:SS).
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, nombre, carrera, materia, descripcion,
                   strftime('%Y-%m-%dT%H:%M:%S', fecha_creacion) AS fecha_creacion
            FROM   solicitudes
            ORDER  BY fecha_creacion DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
