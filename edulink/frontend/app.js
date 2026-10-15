// app.js — EduLink v0.1
// Frontend Developer 2 · Lógica JS e integración con API
//
// SEGURIDAD:
//   - Nunca se usa innerHTML con datos del servidor → sin XSS DOM.
//   - Todos los textos dinámicos se insertan con textContent.
//   - El formulario valida campos vacíos antes de enviar al servidor.
//   - Los errores del servidor se muestran al usuario sin exponer detalles técnicos.

"use strict";

const API_BASE = "http://127.0.0.1:5000";

// ---------------------------------------------------------------------------
// Referencias al DOM
// ---------------------------------------------------------------------------
const form         = document.getElementById("form-solicitud");
const btnEnviar    = document.getElementById("btn-enviar");
const formFeedback = document.getElementById("form-feedback");
const listEstado   = document.getElementById("list-estado");
const listaGrid    = document.getElementById("lista-solicitudes");
const textarea     = document.getElementById("descripcion");
const counter      = document.getElementById("descripcion-counter");

// ---------------------------------------------------------------------------
// Counter de caracteres del textarea
// ---------------------------------------------------------------------------
if (textarea && counter) {
  textarea.addEventListener("input", () => {
    counter.textContent = `${textarea.value.length} / 500`;
  });
}

// ---------------------------------------------------------------------------
// Utilidades de UI
// ---------------------------------------------------------------------------

function clearFieldErrors() {
  document.querySelectorAll(".field-error").forEach(el => {
    el.textContent = "";
  });
  document.querySelectorAll(".field-input").forEach(el => {
    el.classList.remove("is-invalid");
  });
}

function showFieldError(fieldId, message) {
  const input = document.getElementById(fieldId);
  const errorEl = document.getElementById(`${fieldId}-error`);
  if (input)   input.classList.add("is-invalid");
  if (errorEl) errorEl.textContent = message;
}

function showFeedback(message, type) {
  // type: "success" | "error"
  formFeedback.textContent = message;
  formFeedback.className = `form-feedback show ${type}`;
}

function hideFeedback() {
  formFeedback.textContent = "";
  formFeedback.className = "form-feedback";
}

function setLoading(loading) {
  btnEnviar.disabled = loading;
  btnEnviar.classList.toggle("loading", loading);
}

// ---------------------------------------------------------------------------
// Validación en el cliente (primera línea de defensa — UX)
// La validación real y autoritativa ocurre en el servidor (validator.py).
// ---------------------------------------------------------------------------

function validateForm(data) {
  let valid = true;

  if (!data.nombre.trim()) {
    showFieldError("nombre", "El nombre es obligatorio.");
    valid = false;
  }
  if (!data.carrera) {
    showFieldError("carrera", "Selecciona una carrera.");
    valid = false;
  }
  if (!data.materia.trim()) {
    showFieldError("materia", "La materia es obligatoria.");
    valid = false;
  }
  if (!data.descripcion.trim()) {
    showFieldError("descripcion", "La descripción es obligatoria.");
    valid = false;
  }

  return valid;
}

// ---------------------------------------------------------------------------
// Enviar solicitud — POST /api/solicitudes
// ---------------------------------------------------------------------------

async function enviarSolicitud(event) {
  event.preventDefault();
  clearFieldErrors();
  hideFeedback();

  const data = {
    nombre:      form.nombre.value,
    carrera:     form.carrera.value,
    materia:     form.materia.value,
    descripcion: form.descripcion.value,
  };

  if (!validateForm(data)) return;

  setLoading(true);

  try {
    const response = await fetch(`${API_BASE}/api/solicitudes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      // Muestra el mensaje del servidor (validación) — no detalles técnicos
      showFeedback(result.error || "Error al enviar la solicitud.", "error");
      return;
    }

    showFeedback("¡Solicitud publicada correctamente!", "success");
    form.reset();
    if (counter) counter.textContent = "0 / 500";
    await cargarSolicitudes();

  } catch (_err) {
    // No exponer el error técnico al usuario
    showFeedback("No se pudo conectar con el servidor. Intenta de nuevo.", "error");
  } finally {
    setLoading(false);
  }
}

// ---------------------------------------------------------------------------
// Cargar solicitudes — GET /api/solicitudes
// ---------------------------------------------------------------------------

async function cargarSolicitudes() {
  listEstado.textContent = "Cargando solicitudes…";
  listaGrid.innerHTML = "";

  try {
    const response = await fetch(`${API_BASE}/api/solicitudes`);
    if (!response.ok) throw new Error("respuesta no OK");

    const result = await response.json();
    const solicitudes = result.solicitudes || [];

    listEstado.textContent = "";

    if (solicitudes.length === 0) {
      listEstado.textContent = "Aún no hay solicitudes. ¡Sé el primero en publicar!";
      return;
    }

    solicitudes.forEach(sol => listaGrid.appendChild(crearTarjeta(sol)));

  } catch (_err) {
    listEstado.textContent = "No se pudieron cargar las solicitudes.";
  }
}

// ---------------------------------------------------------------------------
// Crear tarjeta — solo textContent, nunca innerHTML con datos del servidor
// ---------------------------------------------------------------------------

function crearTarjeta(sol) {
  const article = document.createElement("article");
  article.className = "card-solicitud";

  const header = document.createElement("div");
  header.className = "card-header";

  const badgeCarrera = document.createElement("span");
  badgeCarrera.className = "card-carrera";
  badgeCarrera.textContent = sol.carrera;          // textContent — seguro contra XSS

  const fecha = document.createElement("span");
  fecha.className = "card-fecha";
  fecha.textContent = sol.fecha_creacion
    ? sol.fecha_creacion.replace("T", " ").slice(0, 16)
    : "";

  header.appendChild(badgeCarrera);
  header.appendChild(fecha);

  const materia = document.createElement("p");
  materia.className = "card-materia";
  materia.textContent = sol.materia;               // textContent — seguro

  const descripcion = document.createElement("p");
  descripcion.className = "card-descripcion";
  descripcion.textContent = sol.descripcion;       // textContent — seguro

  const footer = document.createElement("div");
  footer.className = "card-footer";

  const nombre = document.createElement("span");
  nombre.className = "card-nombre";
  nombre.textContent = sol.nombre;                 // textContent — seguro

  footer.appendChild(nombre);

  article.appendChild(header);
  article.appendChild(materia);
  article.appendChild(descripcion);
  article.appendChild(footer);

  return article;
}

// ---------------------------------------------------------------------------
// Inicialización
// ---------------------------------------------------------------------------

form.addEventListener("submit", enviarSolicitud);
cargarSolicitudes();
