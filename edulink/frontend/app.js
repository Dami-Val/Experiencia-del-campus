<<<<<<< Updated upstream
=======
/**
 * EduLink v0.2 — app.js
 * Filtro + búsqueda + respuestas + marcar resuelta + stats.
 */

const API_URL = '/api/solicitudes';
const CARRERAS_VALIDAS = ['IE', 'IM', 'IS', 'IME'];

// ── Demo fallback ──────────────────────────────────────────
const DATOS_DEMO = [
  { id:1, nombre:'Ana García',    carrera:'IS', materia:'Cálculo Diferencial',  descripcion:'Necesito ayuda con límites y derivadas.',             resuelta:0, fecha_creacion:'2025-01-15T10:30:00' },
  { id:2, nombre:'Luis Martínez', carrera:'IE', materia:'Circuitos Eléctricos', descripcion:'Me cuesta el análisis de mallas con ejemplos reales.', resuelta:0, fecha_creacion:'2025-01-15T09:15:00' },
  { id:3, nombre:'Sofía Ramírez', carrera:'IM', materia:'Programación en C++',  descripcion:'Dudas con punteros y arreglos dinámicos.',              resuelta:1, fecha_creacion:'2025-01-14T17:45:00' },
];

// ── Refs DOM ───────────────────────────────────────────────
const form           = document.getElementById('form-solicitud');
const btnEnviar      = document.getElementById('btn-enviar');
const formFeedback   = document.getElementById('form-feedback');
const listEstado     = document.getElementById('list-estado');
const listaEl        = document.getElementById('lista-solicitudes');
const descCounter    = document.getElementById('descripcion-counter');
const descTextarea   = document.getElementById('descripcion');

// ── Estado local ───────────────────────────────────────────
let todasLasSolicitudes = [];
let filtroActivo = '';
let textoBusqueda = '';

// ── Utilidades UI ──────────────────────────────────────────
const mostrarFeedback = (msg, tipo) => { formFeedback.textContent = msg; formFeedback.className = `form-feedback show ${tipo}`; };
const ocultarFeedback = () => { formFeedback.textContent = ''; formFeedback.className = 'form-feedback'; };
const setBtnCargando  = (on) => { btnEnviar.disabled = on; btnEnviar.classList.toggle('loading', on); };

function marcarError(id, msg) {
  const el = document.getElementById(id);
  const er = document.getElementById(`${id}-error`);
  if (el) el.classList.add('is-invalid');
  if (er) er.textContent = msg;
}
function limpiarErrores() {
  ['nombre','carrera','materia','descripcion'].forEach(id => {
    document.getElementById(id)?.classList.remove('is-invalid');
    const er = document.getElementById(`${id}-error`);
    if (er) er.textContent = '';
  });
}

// ── Validación cliente ─────────────────────────────────────
function validarFormulario(d) {
  let ok = true;
  if (!d.nombre)            { marcarError('nombre',      'El nombre es obligatorio.');       ok=false; }
  else if (d.nombre.length>50){ marcarError('nombre',    'Máximo 50 caracteres.');           ok=false; }
  if (!d.carrera)           { marcarError('carrera',     'Selecciona una carrera.');          ok=false; }
  else if (!CARRERAS_VALIDAS.includes(d.carrera)){ marcarError('carrera','Carrera no válida.'); ok=false; }
  if (!d.materia)           { marcarError('materia',     'La materia es obligatoria.');      ok=false; }
  else if (d.materia.length>100){ marcarError('materia', 'Máximo 100 caracteres.');          ok=false; }
  if (!d.descripcion)       { marcarError('descripcion', 'La descripción es obligatoria.');  ok=false; }
  else if (d.descripcion.length>500){ marcarError('descripcion','Máximo 500 caracteres.');   ok=false; }
  return ok;
}

// ── Formatear fecha ────────────────────────────────────────
function formatearFecha(iso) {
  if (!iso) return '';
  const f = new Date(iso);
  return isNaN(f) ? iso : f.toLocaleDateString('es-MX', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
}

// ── Construir tarjeta ──────────────────────────────────────
function crearTarjeta(s) {
  const article = document.createElement('article');
  article.className = 'card-solicitud' + (s.resuelta ? ' resuelta' : '');
  article.dataset.id      = s.id;
  article.dataset.carrera = s.carrera;

  // Header
  const hdr = document.createElement('header');
  hdr.className = 'card-header';
  const spanCarrera = document.createElement('span');
  spanCarrera.className = 'card-carrera';
  spanCarrera.textContent = s.carrera;
  const time = document.createElement('time');
  time.className = 'card-fecha';
  time.textContent = formatearFecha(s.fecha_creacion);
  if (s.fecha_creacion) time.setAttribute('datetime', s.fecha_creacion);
  hdr.appendChild(spanCarrera);
  if (s.resuelta) {
    const badge = document.createElement('span');
    badge.className = 'badge-resuelta';
    badge.innerHTML = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg> Resuelta';
    hdr.appendChild(badge);
  }
  hdr.appendChild(time);

  // Materia + descripcion
  const h3 = document.createElement('h3');
  h3.className = 'card-materia';
  h3.textContent = s.materia;

  const p = document.createElement('p');
  p.className = 'card-descripcion';
  p.textContent = s.descripcion;

  // Footer nombre
  const footer = document.createElement('footer');
  footer.className = 'card-footer';
  const spanNombre = document.createElement('span');
  spanNombre.className = 'card-nombre';
  spanNombre.textContent = s.nombre;
  footer.appendChild(spanNombre);

  // Sección respuestas
  const respSec = crearSeccionRespuestas(s);

  article.appendChild(hdr);
  article.appendChild(h3);
  article.appendChild(p);
  article.appendChild(footer);
  article.appendChild(respSec);
  return article;
}

// ── Sección respuestas dentro de tarjeta ──────────────────
function crearSeccionRespuestas(s) {
  const sec = document.createElement('div');
  sec.className = 'respuestas-section';

  // Botón toggle
  const btnToggle = document.createElement('button');
  btnToggle.className = 'btn-toggle-respuestas';
  btnToggle.type = 'button';
  btnToggle.innerHTML = `<svg class="chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg> Ver respuestas`;

  // Lista de respuestas
  const lista = document.createElement('div');
  lista.className = 'respuestas-lista';

  // Formulario inline
  const formResp = document.createElement('div');
  formResp.className = 'form-respuesta';
  formResp.innerHTML = `
    <input  type="text"     placeholder="Tu nombre"       maxlength="50"  class="resp-nombre" />
    <textarea               placeholder="Tu respuesta…"   maxlength="500" class="resp-texto" rows="3"></textarea>
    <div class="respuesta-actions">
      <button type="button" class="btn-enviar-respuesta">Responder</button>
      ${!s.resuelta ? `<button type="button" class="btn-resolver"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg> Marcar resuelta</button>` : ''}
    </div>
  `;

  // Toggle abre/cierra
  let cargado = false;
  btnToggle.addEventListener('click', async () => {
    const abierto = lista.classList.toggle('visible');
    formResp.classList.toggle('visible', abierto);
    btnToggle.classList.toggle('abierto', abierto);

    if (abierto && !cargado) {
      cargado = true;
      await cargarRespuestas(s.id, lista);
    }
  });

  // Enviar respuesta
  formResp.querySelector('.btn-enviar-respuesta').addEventListener('click', async () => {
    const btn   = formResp.querySelector('.btn-enviar-respuesta');
    const nombre = formResp.querySelector('.resp-nombre').value.trim();
    const texto  = formResp.querySelector('.resp-texto').value.trim();
    if (!nombre || !texto) { alert('Completa tu nombre y la respuesta.'); return; }
    btn.disabled = true;
    try {
      const res = await fetch(`${API_URL}/${s.id}/respuestas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, texto }),
      });
      if (res.ok) {
        formResp.querySelector('.resp-nombre').value = '';
        formResp.querySelector('.resp-texto').value  = '';
        cargado = false;
        await cargarRespuestas(s.id, lista);
        // actualiza el contador en el botón toggle
        actualizarTextoToggle(btnToggle, lista);
      } else {
        const d = await res.json().catch(() => ({}));
        alert(d.error || 'No se pudo publicar la respuesta.');
      }
    } catch { alert('Sin conexión con el servidor.'); }
    finally { btn.disabled = false; }
  });

  // Marcar resuelta
  const btnResolver = formResp.querySelector('.btn-resolver');
  if (btnResolver) {
    btnResolver.addEventListener('click', async () => {
      btnResolver.disabled = true;
      try {
        const res = await fetch(`${API_URL}/${s.id}/resolver`, { method: 'POST' });
        if (res.ok) {
          // Actualiza la tarjeta visualmente sin recargar todo
          const card = document.querySelector(`.card-solicitud[data-id="${s.id}"]`);
          if (card) {
            card.classList.add('resuelta');
            const badge = document.createElement('span');
            badge.className = 'badge-resuelta';
            badge.innerHTML = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg> Resuelta';
            card.querySelector('.card-header').insertBefore(badge, card.querySelector('.card-fecha'));
          }
          btnResolver.remove();
        } else {
          btnResolver.disabled = false;
          alert('No se pudo marcar como resuelta.');
        }
      } catch { btnResolver.disabled = false; alert('Sin conexión.'); }
    });
  }

  sec.appendChild(btnToggle);
  sec.appendChild(lista);
  sec.appendChild(formResp);
  return sec;
}

async function cargarRespuestas(solicitudId, listaEl) {
  listaEl.innerHTML = '<p style="font-size:.8rem;color:var(--color-muted)">Cargando…</p>';
  try {
    const res  = await fetch(`${API_URL}/${solicitudId}/respuestas`);
    const data = await res.json();
    const resp = data.respuestas || [];
    listaEl.innerHTML = '';
    if (resp.length === 0) {
      listaEl.innerHTML = '<p style="font-size:.8rem;color:var(--color-muted)">Sin respuestas aún. ¡Sé el primero!</p>';
      return;
    }
    resp.forEach(r => {
      const item = document.createElement('div');
      item.className = 'respuesta-item';
      const autor = document.createElement('div');
      autor.className = 'respuesta-autor';
      autor.textContent = r.nombre;
      const texto = document.createElement('div');
      texto.className = 'respuesta-texto';
      texto.textContent = r.texto;
      item.appendChild(autor);
      item.appendChild(texto);
      listaEl.appendChild(item);
    });
  } catch {
    listaEl.innerHTML = '<p style="font-size:.8rem;color:var(--color-error)">Error al cargar respuestas.</p>';
  }
}

function actualizarTextoToggle(btn, lista) {
  const n = lista.querySelectorAll('.respuesta-item').length;
  btn.innerHTML = `<svg class="chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg> ${n} respuesta${n!==1?'s':''}`;
  btn.classList.add('abierto');
}

// ── Stats en hero ──────────────────────────────────────────
function actualizarStats(lista) {
  const total     = lista.length;
  const resueltas = lista.filter(s => s.resuelta).length;
  const abiertas  = total - resueltas;
  const el = id => document.getElementById(id);
  if (el('stat-total'))     el('stat-total').textContent     = total;
  if (el('stat-abiertas'))  el('stat-abiertas').textContent  = abiertas;
  if (el('stat-resueltas')) el('stat-resueltas').textContent = resueltas;
}

// ── Búsqueda ───────────────────────────────────────────────
document.getElementById('buscador')?.addEventListener('input', e => {
  textoBusqueda = e.target.value.toLowerCase().trim();
  renderizarSolicitudes();
});

// ── Filtro por carrera ─────────────────────────────────────
document.querySelector('.filtro-bar')?.addEventListener('click', e => {
  const btn = e.target.closest('.filtro-btn');
  if (!btn) return;
  document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  filtroActivo = btn.dataset.carrera;
  renderizarSolicitudes();
});

function renderizarSolicitudes() {
  listaEl.innerHTML = '';
  let filtradas = filtroActivo
    ? todasLasSolicitudes.filter(s => s.carrera === filtroActivo)
    : todasLasSolicitudes;

  if (textoBusqueda) {
    filtradas = filtradas.filter(s =>
      s.materia.toLowerCase().includes(textoBusqueda) ||
      s.descripcion.toLowerCase().includes(textoBusqueda)
    );
  }

  if (filtradas.length === 0) {
    listEstado.textContent = textoBusqueda
      ? `Sin resultados para "${textoBusqueda}".`
      : filtroActivo
        ? `No hay solicitudes de ${filtroActivo} todavía.`
        : 'No hay solicitudes todavía. ¡Sé el primero en publicar!';
    return;
  }
  listEstado.textContent = '';
  filtradas.forEach(s => listaEl.appendChild(crearTarjeta(s)));
}

// ── Cargar solicitudes ─────────────────────────────────────
async function cargarSolicitudes() {
  listEstado.textContent = 'Cargando solicitudes…';
  listaEl.innerHTML = '';
  try {
    const res  = await fetch(API_URL);
    if (!res.ok) { const d = await res.json().catch(()=>({})); listEstado.textContent = d.error||'Error al cargar.'; return; }
    const data = await res.json();
    todasLasSolicitudes = data.solicitudes || [];
    actualizarStats(todasLasSolicitudes);
    renderizarSolicitudes();
  } catch {
    console.error('[EduLink] Sin servidor. Modo demo.');
    todasLasSolicitudes = DATOS_DEMO;
    actualizarStats(todasLasSolicitudes);
    listEstado.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px" aria-hidden="true"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> Modo demo — datos de ejemplo';
    listEstado.style.cssText = 'color:var(--color-error);font-weight:600';
    renderizarSolicitudes();
  }
}

// ── Submit formulario ──────────────────────────────────────
form.addEventListener('submit', async e => {
  e.preventDefault();
  limpiarErrores();
  ocultarFeedback();

  const datos = {
    nombre:      document.getElementById('nombre').value.trim(),
    carrera:     document.getElementById('carrera').value.trim(),
    materia:     document.getElementById('materia').value.trim(),
    descripcion: document.getElementById('descripcion').value.trim(),
  };
  if (!validarFormulario(datos)) return;

  setBtnCargando(true);
  try {
    const res  = await fetch(API_URL, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(datos) });
    if (res.ok) {
      mostrarFeedback('¡Solicitud publicada! Ya aparece en la lista.', 'success');
      form.reset();
      descCounter.textContent = '0 / 500';
      await cargarSolicitudes();
      document.getElementById('lista').scrollIntoView({ behavior:'smooth' });
    } else {
      const d = await res.json().catch(()=>({}));
      mostrarFeedback(d.error || 'No se pudo enviar la solicitud.', 'error');
    }
  } catch { mostrarFeedback('Sin conexión con el servidor.', 'error'); }
  finally  { setBtnCargando(false); }
});

// ── Contador descripcion ───────────────────────────────────
descTextarea.addEventListener('input', () => {
  const n = descTextarea.value.length;
  descCounter.textContent = `${n} / 500`;
  descCounter.style.color = n >= 480 ? 'var(--color-error)' : '';
});

// ── Init ───────────────────────────────────────────────────
cargarSolicitudes();
>>>>>>> Stashed changes
