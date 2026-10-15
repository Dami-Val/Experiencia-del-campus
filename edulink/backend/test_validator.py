"""
test_validator.py — pruebas unitarias para validator.py
Ejecutar con: python test_validator.py
No requiere Flask ni base de datos.
"""

from validator import validate_solicitud

PASS = "[PASS]"
FAIL = "[FAIL]"

resultados = []

def check(descripcion: str, data: dict, esperado_error: str | None):
    resultado = validate_solicitud(data)
    ok = resultado == esperado_error
    estado = PASS if ok else FAIL
    print(f"{estado}  {descripcion}")
    if not ok:
        print(f"       esperado : {repr(esperado_error)}")
        print(f"       obtenido : {repr(resultado)}")
    resultados.append(ok)


# ---------------------------------------------------------------------------
# Casos validos
# ---------------------------------------------------------------------------
check(
    "Solicitud completa y valida -> None",
    {"nombre": "Ana", "carrera": "IS", "materia": "Calculo", "descripcion": "Necesito ayuda."},
    None,
)
check(
    "Carrera IME valida -> None",
    {"nombre": "Luis", "carrera": "IME", "materia": "Fisica", "descripcion": "Ayuda con vectores."},
    None,
)

# ---------------------------------------------------------------------------
# Campos obligatorios ausentes
# ---------------------------------------------------------------------------
check(
    "Falta 'nombre' -> error obligatorio",
    {"carrera": "IE", "materia": "algebra", "descripcion": "Matrices"},
    "El campo 'nombre' es obligatorio.",
)
check(
    "Falta 'carrera' -> error obligatorio",
    {"nombre": "Ana", "materia": "algebra", "descripcion": "Matrices"},
    "El campo 'carrera' es obligatorio.",
)
check(
    "Falta 'materia' -> error obligatorio",
    {"nombre": "Ana", "carrera": "IM", "descripcion": "Matrices"},
    "El campo 'materia' es obligatorio.",
)
check(
    "Falta 'descripcion' -> error obligatorio",
    {"nombre": "Ana", "carrera": "IM", "materia": "algebra"},
    "El campo 'descripcion' es obligatorio.",
)

# ---------------------------------------------------------------------------
# Cadenas vacias
# ---------------------------------------------------------------------------
check(
    "nombre vacio '' -> error obligatorio",
    {"nombre": "", "carrera": "IS", "materia": "Calculo", "descripcion": "Texto"},
    "El campo 'nombre' es obligatorio.",
)
check(
    "nombre solo espacios -> error obligatorio",
    {"nombre": "   ", "carrera": "IS", "materia": "Calculo", "descripcion": "Texto"},
    "El campo 'nombre' es obligatorio.",
)

# ---------------------------------------------------------------------------
# Carrera invalida
# ---------------------------------------------------------------------------
check(
    "carrera 'XY' invalida -> error carrera",
    {"nombre": "Ana", "carrera": "XY", "materia": "Calculo", "descripcion": "Texto"},
    "El campo 'carrera' debe ser uno de: IE, IM, IS, IME.",
)
check(
    "carrera en minusculas 'is' -> error carrera",
    {"nombre": "Ana", "carrera": "is", "materia": "Calculo", "descripcion": "Texto"},
    "El campo 'carrera' debe ser uno de: IE, IM, IS, IME.",
)

# ---------------------------------------------------------------------------
# Longitudes excedidas
# ---------------------------------------------------------------------------
check(
    "nombre con 51 caracteres -> error longitud",
    {"nombre": "A" * 51, "carrera": "IE", "materia": "Calculo", "descripcion": "Texto"},
    "El campo 'nombre' no puede superar 50 caracteres.",
)
check(
    "materia con 101 caracteres -> error longitud",
    {"nombre": "Ana", "carrera": "IE", "materia": "M" * 101, "descripcion": "Texto"},
    "El campo 'materia' no puede superar 100 caracteres.",
)
check(
    "descripcion con 501 caracteres -> error longitud",
    {"nombre": "Ana", "carrera": "IE", "materia": "Calculo", "descripcion": "D" * 501},
    "El campo 'descripcion' no puede superar 500 caracteres.",
)

# ---------------------------------------------------------------------------
# Tipos incorrectos
# ---------------------------------------------------------------------------
check(
    "nombre como numero -> error tipo",
    {"nombre": 123, "carrera": "IE", "materia": "Calculo", "descripcion": "Texto"},
    "El campo 'nombre' debe ser texto.",
)
check(
    "data no es dict -> error tipo",
    "esto no es un dict",
    "El cuerpo de la petici\u00f3n debe ser un objeto JSON.",
)

# ---------------------------------------------------------------------------
# Resumen
# ---------------------------------------------------------------------------
total  = len(resultados)
passed = sum(resultados)
failed = total - passed
print(f"\n{'='*45}")
print(f"  Resultado: {passed}/{total} pruebas pasaron  {'[OK]' if failed == 0 else f'[{failed} FALLARON]'}")
print(f"{'='*45}")
