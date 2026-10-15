/**
 * EduLink v0.1 — app.js
 * Frontend Developer 2
 *
 * Responsabilidades:
 *   - cargarSolicitudes(): GET al arrancar; renderiza tarjetas en #lista-solicitudes.
 *   - enviarSolicitud(): submit del formulario; valida en cliente; POST; recarga lista.
 *   - Modo demo: si el servidor no responde (error de red), muestra datos de ejemplo.
 */

// ─────────────────────────────────────────────
// CONFIGURACIÓN
// Ruta relativa: el frontend lo sirve Flask en http://localhost:5000/
// Cambiar aquí si la URL base cambia.
// ─────────────────────────────────────────────
const API_URL = '/api/solicitudes';

// Carreras válidas según contrato.md
const CARRERAS_VALIDAS = ['IE', 'IM', 'IS', 'IME'];

// Datos de ejemplo para modo demo (el servidor no responde por red)
const DATOS_DEMO = [
  {
    nombre: 'Ana García',
    carrera: 'IS',
    materia: 'Cálculo Diferencial',
    descripcion: 'Necesito ayuda con límites y derivadas. Tengo examen la próxima semana.',
    fecha_creacion: '2025-01-15T10:30:00',
  },
  {
    nombre: 'Luis Martínez',
    carrera: 'IE',
    materia: 'Circuitos Eléctricos',
    descripcion: 'Me cuesta entender el análisis de mallas. ¿Alguien puede explicarme con un ejemplo?',
    fecha_creacion: '2025-01-15T09:15:00',
  },
  {
    nombre: 'Sofía Ramírez',
    carrera: 'IM',
    materia: 'Programación en C++',
    descripcion: 'Tengo dudas con punteros y arreglos dinámicos.',
    fecha_creacion: '2025-01-14T17:45:00',
  },
];

// ─────────────────────────────────────────────
// REFERENCIAS AL DOM
// ─────────────────────────────────────────────
const form           = document.getElementById('form-solicitud');
const btnEnviar      = document.getElementById('btn-enviar');
const formFeedback   = document.getElementById('form-feedback');
const listEstado     = document.getElementById('list-estado');
const listaSolicitudes = document.getElementById('lista-solicitudes');
const descCounter    = document.getElementById('descripcion-counter');
const descTextarea   = document.getElementById('descripcion');

// ─────────────────────────────────────────────
// UTILIDADES DE UI
// ─────────────────────────────────────────────

/**
 * Muestra u oculta el mensaje de feedback global del formulario.
 * @param {string} mensaje  - Texto a mostrar.
 * @param {'success'|'error'} tipo - Clase de estilo.
 */
function mostrarFeedback(mensaje, tipo) {
  formFeedback.textContent = mensaje;
  formFeedback.className = `form-feedback show ${tipo}`;
}

/** Oculta el feedback global del formulario. */
function ocultarFeedback() {
  formFeedback.textContent = '';
  formFeedback.className = 'form-feedback';
}

/**
 * Marca un campo como inválido y muestra el mensaje de error debajo de él.
 * @param {string} campoId  - ID del input/select/textarea.
 * @param {string} mensaje  - Texto del error.
 */
function marcarError(campoId, mensaje) {
  const campo = document.getElementById(campoId);
  const errorSpan = document.getElementById(`${campoId}-error`);
  if (campo) campo.classList.add('is-invalid');
  if (errorSpan) errorSpan.textContent = mensaje;
}

/** Limpia el estado de error de todos los campos del formulario. */
function limpiarErrores() {
  ['nombre', 'carrera', 'materia', 'descripcion'].forEach((id) => {
    const campo = document.getElementById(id);
    const errorSpan = document.getElementById(`${id}-error`);
    if (campo) campo.classList.remove('is-invalid');
    if (errorSpan) errorSpan.textContent = '';
  });
}

/** Activa o desactiva el estado de carga del botón de envío. */
function setBtnCargando(cargando) {
  btnEnviar.disabled = cargando;
  if (cargando) {
    btnEnviar.classList.add('loading');
  } else {
    btnEnviar.classList.remove('loading');
  }
}

// ─────────────────────────────────────────────
// VALIDACIÓN EN CLIENTE
// Devuelve true si todo está bien, false si hay errores.
// ─────────────────────────────────────────────

/**
 * Valida los campos del formulario antes de enviar al servidor.
 * Marca errores individuales por campo.
 * @param {{nombre:string, carrera:string, materia:string, descripcion:string}} datos
 * @returns {boolean} true si los datos son válidos.
 */
function validarFormulario(datos) {
  let valido = true;

  // nombre: requerido, máx 50
  if (!datos.nombre) {
    marcarError('nombre', 'El nombre es obligatorio.');
    valido = false;
  } else if (datos.nombre.length > 50) {
    marcarError('nombre', 'El nombre no puede superar 50 caracteres.');
    valido = false;
  }

  // carrera: requerido, valores permitidos
  if (!datos.carrera) {
    marcarError('carrera', 'Selecciona una carrera.');
    valido = false;
  } else if (!CARRERAS_VALIDAS.includes(datos.carrera)) {
    marcarError('carrera', 'Carrera no válida.');
    valido = false;
  }

  // materia: requerido, máx 100
  if (!datos.materia) {
    marcarError('materia', 'La materia es obligatoria.');
    valido = false;
  } else if (datos.materia.length > 100) {
    marcarError('materia', 'La materia no puede superar 100 caracteres.');
    valido = false;
  }

  // descripcion: requerido, máx 500
  if (!datos.descripcion) {
    marcarError('descripcion', 'La descripción es obligatoria.');
    valido = false;
  } else if (datos.descripcion.length > 500) {
    marcarError('descripcion', 'La descripción no puede superar 500 caracteres.');
    valido = false;
  }

  return valido;
}

// ─────────────────────────────────────────────
// CONSTRUCCIÓN DE TARJETAS
// Usa createElement + textContent; nunca innerHTML con datos del usuario.
// Estructura según comentario de styles.css (línea 398).
// No se muestra el campo id.
// ─────────────────────────────────────────────

/**
 * Formatea una fecha ISO-8601 a texto legible en español.
 * @param {string} isoStr - e.g. "2025-01-15T10:30:00"
 * @returns {string}
 */
function formatearFecha(isoStr) {
  if (!isoStr) return '';
  const fecha = new Date(isoStr);
  if (isNaN(fecha.getTime())) return isoStr; // si no se puede parsear, devuelve el original
  return fecha.toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Crea y devuelve un elemento <article> con la estructura de tarjeta.
 * @param {{ nombre:string, carrera:string, materia:string, descripcion:string, fecha_creacion:string }} solicitud
 * @returns {HTMLElement}
 */
function crearTarjeta(solicitud) {
  // <article class="card-solicitud">
  const article = document.createElement('article');
  article.className = 'card-solicitud';

  // <header class="card-header">
  const header = document.createElement('header');
  header.className = 'card-header';

  const spanCarrera = document.createElement('span');
  spanCarrera.className = 'card-carrera';
  spanCarrera.textContent = solicitud.carrera;

  const time = document.createElement('time');
  time.className = 'card-fecha';
  time.textContent = formatearFecha(solicitud.fecha_creacion);
  if (solicitud.fecha_creacion) time.setAttribute('datetime', solicitud.fecha_creacion);

  header.appendChild(spanCarrera);
  header.appendChild(time);

  // <h3 class="card-materia">
  const h3 = document.createElement('h3');
  h3.className = 'card-materia';
  h3.textContent = solicitud.materia;

  // <p class="card-descripcion">
  const p = document.createElement('p');
  p.className = 'card-descripcion';
  p.textContent = solicitud.descripcion;

  // <footer class="card-footer">
  const footer = document.createElement('footer');
  footer.className = 'card-footer';

  const spanNombre = document.createElement('span');
  spanNombre.className = 'card-nombre';
  spanNombre.textContent = solicitud.nombre;

  footer.appendChild(spanNombre);

  // Ensamblar
  article.appendChild(header);
  article.appendChild(h3);
  article.appendChild(p);
  article.appendChild(footer);

  return article;
}

// ─────────────────────────────────────────────
// CARGAR SOLICITUDES — GET /api/solicitudes
// ─────────────────────────────────────────────

/**
 * Obtiene las solicitudes del servidor y las renderiza en #lista-solicitudes.
 * Si el servidor no responde por red, activa el modo demo.
 */
async function cargarSolicitudes() {
  listEstado.textContent = 'Cargando solicitudes…';
  listaSolicitudes.innerHTML = '';

  try {
    const response = await fetch(API_URL);

    if (!response.ok) {
      // El servidor respondió con error HTTP (4xx/5xx) — NO activar modo demo
      const datos = await response.json().catch(() => ({}));
      listEstado.textContent = datos.error || 'Error al cargar las solicitudes.';
      return;
    }

    const datos = await response.json();
    const solicitudes = datos.solicitudes || [];

    listEstado.textContent = '';

    if (solicitudes.length === 0) {
      listEstado.textContent = 'No hay solicitudes todavía. ¡Sé el primero en publicar!';
      return;
    }

    solicitudes.forEach((s) => {
      listaSolicitudes.appendChild(crearTarjeta(s));
    });

  } catch (err) {
    // Error de red: el servidor no responde — activar modo demo
    console.error('[EduLink] El servidor no responde. Activando modo demo.', err);
    activarModoDemo();
  }
}

/**
 * Muestra datos de ejemplo cuando el servidor no está disponible.
 */
function activarModoDemo() {
  // Aviso visible en #list-estado
  listEstado.textContent = '⚠️ Modo demo — datos de ejemplo';
  listEstado.style.color = 'var(--color-error)';
  listEstado.style.fontWeight = '600';

  listaSolicitudes.innerHTML = '';
  DATOS_DEMO.forEach((s) => {
    listaSolicitudes.appendChild(crearTarjeta(s));
  });
}

// ─────────────────────────────────────────────
// ENVIAR SOLICITUD — POST /api/solicitudes
// ─────────────────────────────────────────────

/**
 * Manejador del submit del formulario.
 * Valida en cliente → POST → limpia formulario → recarga lista.
 */
async function enviarSolicitud(evento) {
  evento.preventDefault();

  limpiarErrores();
  ocultarFeedback();

  // Leer y limpiar valores
  const datos = {
    nombre:      document.getElementById('nombre').value.trim(),
    carrera:     document.getElementById('carrera').value.trim(),
    materia:     document.getElementById('materia').value.trim(),
    descripcion: document.getElementById('descripcion').value.trim(),
  };

  // Validación en cliente
  if (!validarFormulario(datos)) return;

  setBtnCargando(true);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos),
    });

    if (response.ok) {
      // Éxito (201 o 2xx)
      mostrarFeedback('¡Solicitud publicada! Ya aparece en la lista.', 'success');
      form.reset();
      descCounter.textContent = '0 / 500'; // reiniciar contador
      await cargarSolicitudes();

      // Desplazar suavemente a la lista
      document.getElementById('lista').scrollIntoView({ behavior: 'smooth' });
    } else {
      // Error del servidor (400, 500, etc.) — mostrar su mensaje; NO activar modo demo
      const respuesta = await response.json().catch(() => ({}));
      mostrarFeedback(respuesta.error || 'No se pudo enviar la solicitud.', 'error');
    }

  } catch (err) {
    // Error de red: el servidor no responde
    console.error('[EduLink] Error de red al enviar solicitud.', err);
    mostrarFeedback('No se puede conectar con el servidor. Inténtalo de nuevo.', 'error');
  } finally {
    setBtnCargando(false);
  }
}

// ─────────────────────────────────────────────
// CONTADOR DE CARACTERES (descripcion)
// ─────────────────────────────────────────────
descTextarea.addEventListener('input', () => {
  const len = descTextarea.value.length;
  descCounter.textContent = `${len} / 500`;
  // Advertencia visual cuando se acerca al límite
  descCounter.style.color = len >= 480 ? 'var(--color-error)' : '';
});

// ─────────────────────────────────────────────
// INICIALIZACIÓN
// ─────────────────────────────────────────────
form.addEventListener('submit', enviarSolicitud);
cargarSolicitudes();
