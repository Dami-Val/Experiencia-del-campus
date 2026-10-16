# -*- coding: utf-8 -*-
"""
validator.py — EduLink v0.1
Validación y saneado de campos de entrada para la tabla `solicitudes`.
Backend Developer 2 · Contrato de datos: contrato.md

SEGURIDAD:
  - strip_tags() elimina cualquier etiqueta HTML antes de persistir,
    previniendo XSS almacenado (stored XSS).
  - La whitelist de carreras impide valores fuera del dominio.
  - Los límites de longitud se aplican DESPUÉS del saneado.
"""

import re

CARRERAS_VALIDAS = {"IE", "IM", "IS", "IME"}

_REGLAS = [
    ("nombre",      50),
    ("carrera",     None),
    ("materia",     100),
    ("descripcion", 500),
]

# Regex que elimina cualquier etiqueta HTML/XML del texto
_RE_TAGS = re.compile(r"<[^>]*>")


def strip_tags(text: str) -> str:
    """Elimina etiquetas HTML del texto para prevenir XSS almacenado."""
    return _RE_TAGS.sub("", text)


def sanitize_field(value: str) -> str:
    """Elimina etiquetas HTML y normaliza espacios en los extremos."""
    return strip_tags(value).strip()


def validate_solicitud(data: dict) -> str | None:
    """
    Valida los campos requeridos del contrato de datos (contrato.md).

    Parámetros
    ----------
    data : dict
        Cuerpo JSON de la petición POST /api/solicitudes.

    Retorna
    -------
    str  — mensaje de error (primer fallo encontrado).
    None — todos los campos son válidos.
    """
    if not isinstance(data, dict):
        return "El cuerpo de la petición debe ser un objeto JSON."

    for campo, max_len in _REGLAS:
        valor = data.get(campo)

        # Campo ausente o null
        if valor is None:
            return f"El campo '{campo}' es obligatorio."

        # Debe ser texto
        if not isinstance(valor, str):
            return f"El campo '{campo}' debe ser texto."

        # Sanear y verificar que no quede vacío
        valor_limpio = sanitize_field(valor)
        if not valor_limpio:
            return f"El campo '{campo}' es obligatorio."

        # Límite de longitud (sobre el valor ya saneado)
        if max_len is not None and len(valor_limpio) > max_len:
            return f"El campo '{campo}' no puede superar {max_len} caracteres."

    # Validación específica de carrera (no se sanea: debe ser exacto)
    if data.get("carrera", "").strip() not in CARRERAS_VALIDAS:
        return "El campo 'carrera' debe ser uno de: IE, IM, IS, IME."

    return None
