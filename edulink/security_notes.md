# security_notes.md — EduLink v0.1
> **Responsable de Seguridad · Sprint 30 minutos**
> Este documento es el entregable oficial del rol de seguridad.
> Última actualización: sprint de integración.

---

## 1. Checklist de seguridad — medidas implementadas en el prototipo

Marcar como ✅ tras verificar en el min 23–26.

| # | Medida | Archivo(s) | Estado |
|---|--------|-----------|--------|
| 1 | Validación de campos requeridos en el servidor (HTTP 400 si falta alguno) | `validator.py` | ✅ Implementado |
| 2 | Longitud máxima de campos en el servidor (50/100/500 chars) | `validator.py` | ✅ Implementado |
| 3 | Whitelist de valores para `carrera` (`IE`,`IM`,`IS`,`IME`) | `validator.py` | ✅ Implementado |
| 4 | Saneado de etiquetas HTML en campos de texto (anti-XSS almacenado) | `validator.py` → `strip_tags()` | ✅ Implementado |
| 5 | Atributo `maxlength` en todos los campos del formulario HTML | `index.html` | ✅ Implementado |
| 6 | `<select>` para carrera (impide valores fuera de lista en el cliente) | `index.html` | ✅ Implementado |
| 7 | Tipos de input correctos (`type="text"`, `<textarea>`, `<select>`) | `index.html` | ✅ Implementado |
| 8 | Validación en el cliente antes de enviar (UX — no reemplaza la del servidor) | `app.js` | ✅ Implementado |
| 9 | Tarjetas renderizadas con `textContent` — nunca `innerHTML` con datos del servidor | `app.js` | ✅ Implementado |
| 10 | Excepciones del servidor capturadas — solo mensaje genérico al cliente, detalle en log | `app.py` | ✅ Implementado |
| 11 | `debug=False` en Flask — sin traceback al cliente | `app.py` | ✅ Implementado |
| 12 | `host='127.0.0.1'` — servidor no expuesto en red local | `app.py` | ✅ Implementado |
| 13 | CORS restringido a `localhost:5000` y `127.0.0.1:5000` | `app.py` | ✅ Implementado |
| 14 | Cabecera `Content-Security-Policy` en todas las respuestas | `app.py` | ✅ Implementado |
| 15 | Cabecera `X-Content-Type-Options: nosniff` | `app.py` | ✅ Implementado |
| 16 | Cabecera `X-Frame-Options: DENY` (anti-clickjacking) | `app.py` | ✅ Implementado |
| 17 | Cabecera `Referrer-Policy: no-referrer` | `app.py` | ✅ Implementado |
| 18 | Cabecera `Permissions-Policy` (deshabilita geolocation/mic/cam) | `app.py` | ✅ Implementado |
| 19 | Consultas SQLite parametrizadas con `?` — sin concatenación de strings en SQL | `database.py` | ✅ Implementado |
| 20 | Constraints de BD (`CHECK`, `NOT NULL`) como segunda línea de defensa | `database.py` | ✅ Implementado |
| 21 | No hay contraseñas ni claves secretas en el código fuente | Todo el proyecto | ✅ Verificado |
| 22 | No se devuelven IDs internos ni datos técnicos al frontend (solo campos del contrato) | `app.py`, `app.js` | ✅ Implementado |

---

## 2. Detalles técnicos por vulnerabilidad

### 2.1 XSS Almacenado (Stored Cross-Site Scripting)
**Riesgo:** Un atacante envía un `<script>alert(1)</script>` como valor de `descripcion`. Si se almacena y luego se renderiza con `innerHTML`, se ejecuta en el navegador de cada visitante.

**Mitigaciones aplicadas (defensa en profundidad):**
1. `validator.py` → `strip_tags()` elimina etiquetas HTML con regex antes de persistir en la BD.
2. `app.js` → `crearTarjeta()` usa exclusivamente `textContent` para insertar datos en el DOM.
3. `app.py` → CSP `script-src 'self'` bloquea scripts inline aunque llegaran al cliente.

---

### 2.2 Inyección SQL
**Riesgo:** Si se construye SQL con concatenación de strings, un valor como `'; DROP TABLE solicitudes; --` puede destruir datos.

**Mitigación aplicada:**
- `database.py` usa consultas parametrizadas con `?` en todos los `INSERT` y `SELECT`. SQLite escapa los valores automáticamente.

```python
# CORRECTO — parametrizado
conn.execute("INSERT INTO ... VALUES (?, ?, ?, ?)", (nombre, carrera, materia, descripcion))

# INCORRECTO — nunca hacer esto
conn.execute(f"INSERT INTO ... VALUES ('{nombre}', ...)")
```

---

### 2.3 Exposición de información de error
**Riesgo:** Si Flask corre con `debug=True`, los tracebacks completos se envían al navegador, exponiendo rutas del sistema, versiones de librerías y lógica interna.

**Mitigaciones aplicadas:**
- `app.py` → `debug=False` siempre.
- Todos los bloques `except` loguean el detalle internamente (`logger.exception`) y devuelven solo un mensaje genérico al cliente.

---

### 2.4 Clickjacking
**Riesgo:** Un atacante puede embeber la página en un `<iframe>` invisible y superponer botones falsos.

**Mitigación aplicada:**
- Cabecera `X-Frame-Options: DENY` — el navegador rechaza cargar la página dentro de cualquier frame.
- CSP `frame-ancestors 'none'` — refuerzo moderno equivalente.

---

### 2.5 Exposición en red local
**Riesgo:** `host='0.0.0.0'` expone el servidor a toda la red local (compañeros de sala, red Wi-Fi del campus).

**Mitigación aplicada:**
- `app.py` → `host='127.0.0.1'` — el servidor solo responde en la interfaz loopback de la misma máquina.

---

## 3. Riesgos pendientes para versiones futuras

> ⚠️ El prototipo **NO es apto para uso con datos reales** hasta resolver estos puntos.

| Riesgo | Impacto | Tarea para v0.2+ |
|--------|---------|-----------------|
| Sin autenticación — cualquiera puede publicar con cualquier nombre | Alto | Implementar login con hash de contraseña (bcrypt) y sesiones seguras |
| Sin rate limiting — se puede hacer spam de solicitudes | Medio | Agregar `Flask-Limiter` o similar |
| Sin moderación de contenido | Medio | Revisión manual o integración con API de moderación |
| HTTPS no configurado | Alto | Obligatorio antes de cualquier despliegue; usar certificado TLS válido |
| Sin política de privacidad | Legal | Redactar antes de recibir datos de estudiantes reales |
| Sanitización con regex es básica | Medio | En producción usar `bleach` (Python) para saneado robusto de HTML |
| Sin paginación en `GET /api/solicitudes` | Bajo | Agregar `LIMIT`/`OFFSET` para evitar respuestas masivas |
| BD SQLite sin backup | Medio | Migrar a PostgreSQL con backups automáticos en producción |

---

## 4. Comunicación al equipo (min 20–25)

Mensajes para enviar en el canal de chat:

```
[SEGURIDAD] Checklist completada — todas las medidas del prototipo están implementadas.

Puntos revisados:
✅ Formulario con maxlength y select para carrera (index.html)
✅ Validación + saneado de HTML en servidor (validator.py)
✅ Consultas SQL parametrizadas (database.py)
✅ debug=False, host=127.0.0.1, sin tracebacks al cliente (app.py)
✅ Cabeceras CSP, X-Frame-Options, X-Content-Type-Options (app.py)
✅ Tarjetas renderizadas con textContent — sin innerHTML (app.js)
✅ Sin credenciales en el código

⚠️ Riesgos pendientes para v0.2: autenticación, HTTPS, rate limiting.
⚠️ NO ingresar datos personales reales durante la demo.
```

---

*EduLink v0.1 · Notas de Seguridad · Responsable de Seguridad · Generado con IBM Bob*
