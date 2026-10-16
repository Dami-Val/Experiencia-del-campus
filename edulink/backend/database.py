"""
database.py — EduLink v0.2
SQLite CRUD: solicitudes + respuestas + resuelta.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "edulink.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea/actualiza tablas. Seguro de llamar en cada arranque."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes (
                id             INTEGER  PRIMARY KEY AUTOINCREMENT,
                nombre         TEXT     NOT NULL CHECK(length(nombre) <= 50),
                carrera        TEXT     NOT NULL CHECK(carrera IN ('IE', 'IM', 'IS', 'IME')),
                materia        TEXT     NOT NULL CHECK(length(materia) <= 100),
                descripcion    TEXT     NOT NULL CHECK(length(descripcion) <= 500),
                resuelta       INTEGER  NOT NULL DEFAULT 0,
                fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Migración no destructiva: añade columna si la BD ya existe sin ella
        try:
            conn.execute("ALTER TABLE solicitudes ADD COLUMN resuelta INTEGER NOT NULL DEFAULT 0")
        except Exception:
            pass  # ya existe

        conn.execute("""
            CREATE TABLE IF NOT EXISTS respuestas (
                id              INTEGER  PRIMARY KEY AUTOINCREMENT,
                solicitud_id    INTEGER  NOT NULL REFERENCES solicitudes(id),
                nombre          TEXT     NOT NULL CHECK(length(nombre) <= 50),
                texto           TEXT     NOT NULL CHECK(length(texto) <= 500),
                fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


# ── Solicitudes ────────────────────────────────────────────

def insertar_solicitud(nombre: str, carrera: str, materia: str, descripcion: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO solicitudes (nombre, carrera, materia, descripcion) VALUES (?,?,?,?)",
            (nombre, carrera, materia, descripcion),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def obtener_solicitudes() -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT id, nombre, carrera, materia, descripcion, resuelta,
                   strftime('%Y-%m-%dT%H:%M:%S', fecha_creacion) AS fecha_creacion
            FROM   solicitudes
            ORDER  BY fecha_creacion DESC
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def marcar_resuelta(solicitud_id: int) -> bool:
    """Marca como resuelta. Devuelve True si existía la fila."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE solicitudes SET resuelta=1 WHERE id=?", (solicitud_id,)
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


# ── Respuestas ─────────────────────────────────────────────

def insertar_respuesta(solicitud_id: int, nombre: str, texto: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO respuestas (solicitud_id, nombre, texto) VALUES (?,?,?)",
            (solicitud_id, nombre, texto),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def obtener_respuestas(solicitud_id: int) -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT id, solicitud_id, nombre, texto,
                   strftime('%Y-%m-%dT%H:%M:%S', fecha_creacion) AS fecha_creacion
            FROM   respuestas
            WHERE  solicitud_id=?
            ORDER  BY fecha_creacion ASC
        """, (solicitud_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
