# EduLink — Contexto del Proyecto

> Archivo de contexto para sincronizar a todos los integrantes del equipo con su agente Bob.
> Comparte este archivo al inicio de cada sesión de trabajo con tu agente.

---

## Datos generales

| Campo | Valor |
|---|---|
| Nombre del proyecto | EduLink — Espacio de apoyo estudiantil |
| Versión actual | 0.1 (prototipo) |
| Tipo | Página web funcional (prototipo de 30 minutos) |
| Usuarios objetivo | ~1,000 estudiantes de Ingeniería |
| Carreras | Ingeniería Eléctrica (IE), Ingeniería Mecatrónica (IM), Ingeniería de Software (IS), Ingeniería Mecánica Eléctrica (IME) |
| Repositorio | GitHub — rama principal: `main` |
| Entorno de ejecución | localhost (sin despliegue en producción en v0.1) |

---

## Problema que resuelve

Los estudiantes no tienen un canal único y organizado para pedir ayuda académica entre compañeros. Los recursos útiles se pierden en grupos de mensajería desorganizados y no existe visibilidad de quién puede ayudar con qué materia.

---

## Objetivo general

Desarrollar un prototipo funcional de una plataforma web que permita a los estudiantes de Ingeniería publicar y consultar solicitudes de apoyo académico, centralizando en un solo lugar las necesidades y recursos de la comunidad estudiantil.

---

## Objetivos específicos

1. Construir una interfaz web responsiva con página de inicio, formulario de solicitud y vista de publicaciones, demostrable en navegador en menos de 30 minutos.
2. Implementar un endpoint backend que reciba y almacene solicitudes de ayuda en una base de datos local.
3. Permitir filtrar o visualizar publicaciones por carrera.
4. Validar los campos del formulario para evitar envíos incompletos o maliciosos.
5. Lograr que los ocho integrantes integren sus componentes en una sola aplicación demostrable al finalizar los 30 minutos.

---

## Stack tecnológico

| Capa | Tecnología | Notas |
|---|---|---|
| Frontend | HTML5 + CSS3 + JavaScript vanilla | Sin frameworks, sin npm en el cliente |
| Backend | **Opción A:** Flask (Python) · **Opción B:** Express (Node.js) | El equipo elige una opción al inicio |
| Base de datos | SQLite (archivo local) | Sin servidor externo; stdlib de Python o better-sqlite3 |
| Control de versiones | Git + GitHub | Rama única: `main` |

**Puerto acordado:** `localhost:5000` (Flask) o `localhost:3000` (Express)

---

## Estructura de archivos

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
├── contrato.md         ← Contrato de datos acordado (Analista de Sistemas)
├── security_notes.md   ← Notas y checklist de seguridad (Responsable de Seguridad)
└── README.md           ← Instrucciones para correr el proyecto (Project Manager)
```

---

## Modelo de datos

### Tabla: `solicitudes`

| Campo | Tipo | Requerido | Descripción | Restricción |
|---|---|---|---|---|
| `id` | INTEGER PK AUTOINCREMENT | Auto | Identificador único | — |
| `nombre` | TEXT | Sí | Primer nombre del estudiante | Máx. 50 caracteres |
| `carrera` | TEXT | Sí | Carrera del estudiante | Valores: IE, IM, IS, IME |
| `materia` | TEXT | Sí | Materia en la que necesita ayuda | Máx. 100 caracteres |
| `descripcion` | TEXT | Sí | Descripción breve del problema | Máx. 500 caracteres |
| `fecha_creacion` | DATETIME | Auto | Timestamp del servidor | DEFAULT CURRENT_TIMESTAMP |

---

## Contrato de datos (API)

### POST `/api/solicitudes` — Request body
```json
{
  "nombre": "Ana",
  "carrera": "IS",
  "materia": "Cálculo Diferencial",
  "descripcion": "Necesito ayuda con límites y derivadas."
}
```

### GET `/api/solicitudes` — Response
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

### POST — Error response (HTTP 400)
```json
{
  "error": "El campo 'materia' es obligatorio."
}
```

---

## Endpoints mínimos

| Método | Ruta | Descripción | Implementado por |
|---|---|---|---|
| GET | `/api/solicitudes` | Devuelve todas las solicitudes en JSON | Backend Developer 1 |
| POST | `/api/solicitudes` | Crea una nueva solicitud; valida campos requeridos | Backend Developer 1 + Backend Developer 2 |

---

## Roles del equipo y entregables

| # | Rol | Archivo(s) que produce | Dependencias |
|---|---|---|---|
| 1 | Project Manager | `README.md`, repositorio Git | — (inicia primero) |
| 2 | Analista de Sistemas | `contrato.md` | PM (repositorio) |
| 3 | DB Developer | `backend/database.py` | Analista (contrato) |
| 4 | Backend Developer 1 | `backend/app.py` | Analista (contrato), DB Developer |
| 5 | Backend Developer 2 | `backend/validator.py` integrado en `app.py` | Analista (contrato), Backend 1 |
| 6 | Frontend Developer 1 | `frontend/index.html`, `frontend/styles.css` | Analista (campos del formulario) |
| 7 | Frontend Developer 2 | `frontend/app.js` | Frontend 1 (HTML), Backend 1 (endpoints) |
| 8 | Responsable de Seguridad | `security_notes.md`, revisión de código | Frontend 1, Backend 1 y 2 |

---

## Cronograma del sprint (30 minutos)

| Bloque | Minutos | Actividades | Modo |
|---|---|---|---|
| Arranque y setup | 0 – 3 | PM crea repo; todos hacen clone; se verifica el entorno | Secuencial |
| Contratos | 3 – 5 | Analista publica el contrato de datos en el chat; todos confirman | Secuencial |
| Desarrollo | 5 – 20 | Todos trabajan en su archivo en paralelo | **Paralelo** |
| Integración | 20 – 23 | Todos hacen push; PM integra en main; Backend conecta BD real | Coordinado |
| Pruebas | 23 – 26 | Analista y Seguridad ejecutan la checklist de aceptación | Paralelo |
| Correcciones | 26 – 28 | Solo errores críticos que impidan la demo | Priorizado |
| Demo final | 28 – 30 | PM conduce la demo del flujo completo | Secuencial |

---

## Checklist de aceptación (criterios obligatorios)

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

## Medidas de seguridad implementadas en v0.1

- Validación de campos requeridos en el servidor (HTTP 400 si faltan datos).
- Atributo `maxlength` en los campos del formulario HTML.
- CORS restringido a `localhost`.
- Sin credenciales en el código fuente.
- El servidor no devuelve trazas de error al cliente.
- Solo se muestran los campos necesarios en las tarjetas de solicitudes.

> **ADVERTENCIA:** Este prototipo NO es apto para uso con estudiantes reales sin una revisión de seguridad completa. No ingresar datos personales reales durante las pruebas.

---

## Funciones pospuestas (fuera del alcance de v0.1)

- Login y registro de usuarios
- Chat en tiempo real
- Notificaciones push o por correo
- Subida de archivos
- Sistema de roles (admin / estudiante)
- Moderación automática de contenido
- Búsqueda por texto libre
- Despliegue en servidor público

---

## Plan de contingencia

| Situación | Acción |
|---|---|
| Backend no listo al min 20 | Frontend 2 activa array local en `app.js`; indicar "Modo demo" en pantalla |
| Conflicto de merge en Git | PM lo resuelve; cada uno trabaja en su archivo propio |
| Error de CORS | Backend 2 tiene esta tarea como prioridad desde el min 5 |
| Integrante sin entorno listo | Trabaja en el frontend (no requiere dependencias adicionales) |
| No alcanza el tiempo | PM reduce alcance al min 15: priorizar formulario + lista con datos de ejemplo |

---

## Protocolo de comunicación durante el sprint

- **Canal único:** chat del equipo (WhatsApp, Discord o similar).
- **Bloqueo:** escribir `[BLOQUEADO] descripción del problema` en el chat.
- **Entregable listo:** escribir `[LISTO] nombre del archivo` en el chat.
- **PM revisa el progreso:** minutos 10, 15 y 20.
- **Bloqueo sin solución en 2 minutos:** el PM asigna apoyo.

---

## Resultado mínimo esperable al terminar los 30 minutos

1. La página EduLink se carga con título, descripción y formulario visible.
2. Se puede llenar el formulario (nombre, carrera, materia, descripción) y presionar **Enviar**.
3. La solicitud aparece inmediatamente en la lista de solicitudes en la misma página.
4. El formulario rechaza el envío si algún campo está vacío.
5. La interfaz se ve correctamente en vista móvil.

---

*EduLink v0.1 — Archivo de contexto del proyecto · Generado con IBM Bob*
