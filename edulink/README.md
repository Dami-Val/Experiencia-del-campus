# EduLink — Espacio de apoyo estudiantil

> Prototipo funcional v0.1 · Sprint de 30 minutos

EduLink es una plataforma web que centraliza las solicitudes de apoyo académico entre estudiantes de Ingeniería. Elimina la dispersión de recursos en grupos de mensajería y hace visible quién necesita ayuda y en qué materia.

---

## Usuarios objetivo

~1 000 estudiantes de las carreras:

- Ingeniería Eléctrica (IE)
- Ingeniería Mecatrónica (IM)
- Ingeniería de Software (IS)
- Ingeniería Mecánica Eléctrica (IME)

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | HTML5 + CSS3 + JavaScript vanilla |
| Backend | Flask (Python) |
| Base de datos | SQLite (archivo local) |
| Control de versiones | Git + GitHub (`main`) |

**Puerto:** `localhost:5000`

---

## Estructura del proyecto

```
edulink/
├── backend/
│   ├── app.py          ← Servidor Flask (Backend Developer 1)
│   ├── database.py     ← Conexión SQLite y funciones CRUD (DB Developer)
│   └── validator.py    ← Validación de campos de entrada (Backend Developer 2)
├── frontend/
│   ├── index.html      ← Estructura HTML (Frontend Developer 1)
│   ├── styles.css      ← Estilos responsivos (Frontend Developer 1)
│   └── app.js          ← Lógica JavaScript y Fetch API (Frontend Developer 2)
├── contrato.md         ← Contrato de datos acordado
├── security_notes.md   ← Notas y checklist de seguridad
└── README.md
```

---

## Requisitos previos

- Python 3.8 o superior
- pip

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd edulink

# 2. Instalar dependencias del backend
pip install flask

# 3. Iniciar el servidor
python backend/app.py
```

Abrir el navegador en `http://localhost:5000`.

> El frontend se sirve directamente desde Flask; no se requiere servidor adicional.

---

## API

### `GET /api/solicitudes`
Devuelve todas las solicitudes almacenadas.

```json
{
  "solicitudes": [
    {
      "id": 1,
      "nombre": "Ana",
      "carrera": "IS",
      "materia": "Cálculo Diferencial",
      "descripcion": "Necesito ayuda con límites y derivadas.",
      "fecha_creacion": "2025-01-01T10:00:00"
    }
  ]
}
```

### `POST /api/solicitudes`
Crea una nueva solicitud. Todos los campos son obligatorios.

**Request body:**
```json
{
  "nombre": "Ana",
  "carrera": "IS",
  "materia": "Cálculo Diferencial",
  "descripcion": "Necesito ayuda con límites y derivadas."
}
```

**Error (HTTP 400):**
```json
{ "error": "El campo 'materia' es obligatorio." }
```

---

## Roles del equipo

| Rol | Archivo(s) |
|---|---|
| Project Manager | `README.md`, repositorio Git |
| Analista de Sistemas | `contrato.md` |
| DB Developer | `backend/database.py` |
| Backend Developer 1 | `backend/app.py` |
| Backend Developer 2 | `backend/validator.py` |
| Frontend Developer 1 | `frontend/index.html`, `frontend/styles.css` |
| Frontend Developer 2 | `frontend/app.js` |
| Responsable de Seguridad | `security_notes.md`, revisión de código |

---

## Checklist de aceptación

- [ ] La página carga en el navegador sin errores en consola.
- [ ] El servidor backend arranca sin errores en la terminal.
- [ ] El formulario muestra error si se envía con campos vacíos.
- [ ] Se puede enviar una solicitud completa y recibir confirmación.
- [ ] La solicitud aparece en la lista sin recargar la página.
- [ ] La interfaz es usable en pantalla de celular (responsive).
- [ ] `GET /api/solicitudes` devuelve JSON válido.
- [ ] No hay credenciales ni claves secretas en el repositorio.
- [ ] El equipo puede demostrar el flujo completo en menos de 2 minutos.

---

## Advertencia de seguridad

> Este prototipo **NO** es apto para uso con estudiantes reales sin una revisión de seguridad completa.  
> **No ingresar datos personales reales durante las pruebas.**

---

## Funciones fuera del alcance de v0.1

Login, chat en tiempo real, notificaciones, subida de archivos, sistema de roles, moderación de contenido, búsqueda por texto libre, despliegue en servidor público.

---

*EduLink v0.1 · Generado con IBM Bob*
