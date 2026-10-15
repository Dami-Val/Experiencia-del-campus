<div align="center">

# 📚 EduLink

**Espacio de apoyo estudiantil entre compañeros de Ingeniería**

Publica tu solicitud de ayuda, descubre quién puede apoyarte y conecta con la comunidad académica de tu carrera.

[![Estado](https://img.shields.io/badge/estado-prototipo_v0.1-yellow?style=for-the-badge)](https://github.com/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

</div>

---

## 📖 Descripción

**EduLink** es una plataforma web que centraliza las solicitudes de apoyo académico entre estudiantes de Ingeniería. Elimina la dispersión de recursos en grupos de mensajería desorganizados y hace visible quién necesita ayuda y en qué materia.

Los estudiantes pueden publicar una solicitud indicando su carrera, la materia y una descripción de su duda. El resto de la comunidad puede consultar todas las solicitudes y ofrecer apoyo directamente.

---

## ✨ Funcionalidades

| Funcionalidad | Estado |
|---|---|
| Publicación de solicitudes de apoyo | ✅ Completado |
| Listado de solicitudes en tiempo real | ✅ Completado |
| Filtro por carrera | ✅ Completado |
| Validación de formulario (campos vacíos) | ✅ Completado |
| Interfaz responsiva (móvil y escritorio) | ✅ Completado |
| API REST JSON | ✅ Completado |
| Base de datos local SQLite | ✅ Completado |

---

## 👥 Usuarios objetivo

~1 000 estudiantes de las carreras:

| Clave | Carrera |
|---|---|
| IE | Ingeniería Eléctrica |
| IM | Ingeniería Mecatrónica |
| IS | Ingeniería de Software |
| IME | Ingeniería Mecánica Eléctrica |

---

## 🛠️ Tecnologías utilizadas

<p align="left">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="50" height="50" title="HTML5"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="50" height="50" title="CSS3"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="50" height="50" title="JavaScript"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50" height="50" title="Python"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" width="50" height="50" title="SQLite"/>
</p>

| Tecnología | Uso |
|---|---|
| **Python + Flask** | Servidor backend y API REST |
| **SQLite** | Base de datos local (sin servidor externo) |
| **HTML5** | Estructura de la interfaz web |
| **CSS3** | Diseño responsivo y estilos visuales |
| **JavaScript** | Fetch API e interactividad del cliente |

---

## 🚀 Instalación y ejecución

### Requisitos previos

- Python 3.8 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd edulink

# 2. Instalar dependencias del backend
pip install flask

# 3. Iniciar el servidor
python backend/app.py
```

Abrir el navegador en **`http://localhost:5000`**.

> El frontend se sirve directamente desde Flask; no se requiere servidor adicional.

---

## 📁 Estructura del proyecto

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

## 🔌 API

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

## 🧑‍💼 Roles del equipo

| Rol | Archivo(s) | Dependencias |
|---|---|---|
| Project Manager | `README.md`, repositorio Git | — (inicia primero) |
| Analista de Sistemas | `contrato.md` | PM |
| DB Developer | `backend/database.py` | Analista |
| Backend Developer 1 | `backend/app.py` | Analista, DB Developer |
| Backend Developer 2 | `backend/validator.py` | Analista, Backend 1 |
| Frontend Developer 1 | `frontend/index.html`, `frontend/styles.css` | Analista |
| Frontend Developer 2 | `frontend/app.js` | Frontend 1, Backend 1 |
| Responsable de Seguridad | `security_notes.md`, revisión de código | Frontend 1, Backend 1 y 2 |

---

## ✅ Checklist de aceptación

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

## ⚠️ Advertencia de seguridad

> Este prototipo **NO** es apto para uso con estudiantes reales sin una revisión de seguridad completa.  
> **No ingresar datos personales reales durante las pruebas.**

---

## 🚧 Funciones fuera del alcance de v0.1

Login y registro de usuarios, chat en tiempo real, notificaciones push o por correo, subida de archivos, sistema de roles, moderación automática de contenido, búsqueda por texto libre, despliegue en servidor público.

---

## ✒️ Autores

| Nombre | Rol |
|---|---|
| Project Manager | Repositorio y coordinación |
| Analista de Sistemas | Contrato de datos |
| DB Developer | Base de datos SQLite |
| Backend Developer 1 | Servidor Flask y endpoints |
| Backend Developer 2 | Validación de campos |
| Frontend Developer 1 | HTML y CSS responsivo |
| Frontend Developer 2 | JavaScript y Fetch API |
| Responsable de Seguridad | Revisión y notas de seguridad |

---

## 📄 Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE). Puedes usarlo, modificarlo y distribuirlo libremente con atribución.

---

<div align="center">

Hecho con ❤️ por el equipo EduLink · Sprint de 30 minutos

</div>
