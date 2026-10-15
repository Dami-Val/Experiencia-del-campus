"""
validator.py — EduLink v0.1
Validación de campos de entrada para la tabla `solicitudes`.
Backend Developer 2 · Contrato de datos: contrato.md
"""

CARRERAS_VALIDAS = {"IE", "IM", "IS", "IME"}

_REGLAS = [
    ("nombre",      50),
    ("carrera",     None),
    ("materia",     100),
    ("descripcion", 500),
]


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

        # No se aceptan cadenas vacías
        if not valor.strip():
            return f"El campo '{campo}' es obligatorio."

        # Límite de longitud
        if max_len is not None and len(valor.strip()) > max_len:
            return f"El campo '{campo}' no puede superar {max_len} caracteres."

    # Validación específica de carrera
    if data.get("carrera", "").strip() not in CARRERAS_VALIDAS:
        return "El campo 'carrera' debe ser uno de: IE, IM, IS, IME."

    return None
