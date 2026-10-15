# Contrato de Datos — EduLink v0.1

> **Analista de Sistemas · Sprint 30 min**
> Este documento es la fuente de verdad para el equipo.
> **Todos los desarrolladores deben confirmar en el chat que leyeron este contrato antes del minuto 5.**

---

## 1. Campos del formulario (Frontend)

| Campo HTML `name` | Etiqueta visible | Tipo de input | Requerido | Restricción | Valores permitidos |
|---|---|---|---|---|---|
| `nombre` | Nombre | `text` | ✅ | `maxlength="50"` | Texto libre |
| `carrera` | Carrera | `select` | ✅ | Solo opciones de la lista | `IE`, `IM`, `IS`, `IME` |
| `materia` | Materia | `text` | ✅ | `maxlength="100"` | Texto libre |
| `descripcion` | Descripción | `textarea` | ✅ | `maxlength="500"` | Texto libre |

> **Nota Frontend 1:** el atributo `name` de cada `<input>` / `<select>` / `<textarea>` debe coincidir exactamente con los nombres de la tabla anterior. El botón de envío lleva `id="btn-enviar"`.

---

## 2. Estructura JSON de la API

### 2.1 POST `/api/solicitudes` — cuerpo de la petición (request body)

```json
{
  "nombre":      "Ana",
  "carrera":     "IS",
  "materia":     "Cálculo Diferencial",
  "descripcion": "Necesito ayuda con límites y derivadas."
}
```

**Reglas de validación (responsabilidad de `validator.py`):**
- Los cuatro campos son obligatorios; si alguno falta → HTTP 400.
- `nombre` máximo 50 caracteres.
- `carrera` debe ser exactamente uno de: `IE`, `IM`, `IS`, `IME`.
- `materia` máximo 100 caracteres.
- `descripcion` máximo 500 caracteres.
- No se aceptan valores `null` ni cadenas vacías `""`.

**Respuesta exitosa — HTTP 201:**
```json
{
  "mensaje": "Solicitud creada exitosamente.",
  "id": 1
}
```

**Respuesta de error — HTTP 400:**
```json
{
  "error": "El campo 'materia' es obligatorio."
}
```

---

### 2.2 GET `/api/solicitudes` — respuesta completa

```json
{
  "solicitudes": [
    {
      "id":             1,
      "nombre":         "Ana",
      "carrera":        "IS",
      "materia":        "Cálculo Diferencial",
      "descripcion":    "Necesito ayuda con límites y derivadas.",
      "fecha_creacion": "2025-01-01T10:00:00"
    }
  ]
}
```

- `fecha_creacion` es generado por el servidor (no lo envía el cliente).
- El array puede estar vacío `[]` si aún no hay solicitudes; no es un error.

---

## 3. Endpoints acordados

| Método | Ruta | Descripción | Responsable |
|---|---|---|---|
| `POST` | `/api/solicitudes` | Crea una solicitud; valida campos; devuelve 201 o 400 | Backend Dev 1 + Backend Dev 2 |
| `GET` | `/api/solicitudes` | Devuelve todas las solicitudes ordenadas por `fecha_creacion DESC` | Backend Dev 1 |

**URL base:**
- Flask → `http://localhost:5000`
- Express → `http://localhost:3000`

El equipo elige una sola opción al inicio del sprint y la comunica en el chat.

---

## 4. Modelo de base de datos (referencia para DB Developer)

### Tabla: `solicitudes`

```sql
CREATE TABLE IF NOT EXISTS solicitudes (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre         TEXT    NOT NULL CHECK(length(nombre) <= 50),
    carrera        TEXT    NOT NULL CHECK(carrera IN ('IE','IM','IS','IME')),
    materia        TEXT    NOT NULL CHECK(length(materia) <= 100),
    descripcion    TEXT    NOT NULL CHECK(length(descripcion) <= 500),
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 5. Cabeceras HTTP requeridas

| Cabecera | Valor | Quién la pone |
|---|---|---|
| `Content-Type` | `application/json` | Frontend (en el `fetch`) y Backend (en la respuesta) |
| `Access-Control-Allow-Origin` | `http://localhost` (o `*` solo para prototipo) | Backend (CORS) |

---

## 6. Checklist de aceptación (Analista — min 25–30)

- [ ] `POST /api/solicitudes` con todos los campos devuelve HTTP 201 y un `id` numérico.
- [ ] `POST /api/solicitudes` con un campo faltante devuelve HTTP 400 con mensaje de error.
- [ ] `POST /api/solicitudes` con `carrera` fuera de lista devuelve HTTP 400.
- [ ] `GET /api/solicitudes` devuelve JSON con clave `"solicitudes"` (array, puede estar vacío).
- [ ] La solicitud enviada aparece en la respuesta del `GET` sin recargar la página.
- [ ] El formulario muestra un mensaje visible de error si se envía con campos vacíos.
- [ ] La página carga sin errores en consola del navegador.
- [ ] La interfaz es funcional en viewport de 375 px (móvil).

---

## 7. Lo que está fuera del alcance en v0.1

- Autenticación o login de ningún tipo.
- Filtrado por carrera en el backend (puede hacerse en el frontend si hay tiempo).
- Paginación del `GET`.
- Actualización (`PUT`) o eliminación (`DELETE`) de solicitudes.
- Subida de archivos.

---

*EduLink v0.1 · Contrato de Datos · Analista de Sistemas · Generado con IBM Bob*
