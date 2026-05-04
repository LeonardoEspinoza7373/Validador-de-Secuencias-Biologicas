/**
 * Validador de Secuencias Biológicas - Frontend
 * Maneja la interacción con la API y la visualización de resultados
 */

// Variables globales
let archivoSeleccionado = null;
let resultadosActuales = [];
let filtroActual = 'todos';

// ================================================
// ELEMENTOS DEL DOM
// ================================================

const dropzone = document.getElementById('dropzone');
const archivoInput = document.getElementById('archivo-input');
const nombreArchivoDiv = document.getElementById('nombre-archivo');
const btnValidar = document.getElementById('btn-validar');
const indicadorCarga = document.getElementById('indicador-carga');
const seccionResultados = document.getElementById('seccion-resultados');
const seccionError = document.getElementById('seccion-error');
const mensajeError = document.getElementById('mensaje-error');
const modal = document.getElementById('modal');
const btnCerrarModal = document.getElementById('btn-cerrar-modal');
const contenedorResultados = document.getElementById('contenedor-resultados');

// Elementos de entrada manual
const nombresecuenciaInput = document.getElementById('nombre-secuencia');
const secuenciaEntradaTextarea = document.getElementById('secuencia-entrada');
const btnValidarManual = document.getElementById('btn-validar-manual');
const longitudSecuencia = document.getElementById('longitud-secuencia');
const caracteresInvalidos = document.getElementById('caracteres-invalidos');

// ================================================
// TABS
// ================================================

document.querySelectorAll('.tab-boton').forEach(boton => {
    boton.addEventListener('click', (e) => {
        const tabDestino = e.target.getAttribute('data-tab');
        cambiarTab(tabDestino);
    });
});

function cambiarTab(tabDestino) {
    // Actualizar botones
    document.querySelectorAll('.tab-boton').forEach(b => b.classList.remove('activo'));
    document.querySelector(`[data-tab="${tabDestino}"]`).classList.add('activo');

    // Actualizar contenido
    document.querySelectorAll('.tab-contenido').forEach(tab => {
        tab.classList.remove('activo');
        tab.style.display = 'none';
    });
    document.getElementById(`tab-${tabDestino}`).classList.add('activo');
    document.getElementById(`tab-${tabDestino}`).style.display = 'block';

    // Limpiar errores
    ocultarError();
}

// ================================================
// EVENT LISTENERS - ENTRADA MANUAL
// ================================================

secuenciaEntradaTextarea.addEventListener('input', actualizarLongitudSecuencia);
btnValidarManual.addEventListener('click', validarSecuenciaManual);

function actualizarLongitudSecuencia() {
    const secuencia = secuenciaEntradaTextarea.value.toUpperCase();
    const longitud = secuencia.replace(/[^ATGC]/g, '').length;
    const total = secuencia.replace(/\s/g, '').length;

    longitudSecuencia.textContent = `Longitud: ${longitud} nucleótidos válidos`;

    // Detectar caracteres inválidos
    const caracteresValidos = /[ATGC\s]/g;
    const secuenciaLimpia = secuencia.replace(caracteresValidos, '');

    if (secuenciaLimpia.length > 0) {
        const caracteresUnicos = [...new Set(secuenciaLimpia)].join(', ');
        caracteresInvalidos.textContent = `❌ Caracteres inválidos: ${caracteresUnicos}`;
        caracteresInvalidos.style.display = 'inline';
    } else {
        caracteresInvalidos.style.display = 'none';
    }
}

async function validarSecuenciaManual() {
    const nombre = nombresecuenciaInput.value.trim();
    const secuencia = secuenciaEntradaTextarea.value.trim().toUpperCase();

    if (!nombre) {
        mostrarError('Por favor ingresa un nombre para la secuencia');
        return;
    }

    if (!secuencia) {
        mostrarError('Por favor ingresa una secuencia');
        return;
    }

    // Validar que solo contenga caracteres válidos
    const secuenciaLimpia = secuencia.replace(/\s/g, '');
    if (!/^[ATGC]+$/.test(secuenciaLimpia)) {
        mostrarError('La secuencia solo puede contener A, T, G, C (sin espacios)');
        return;
    }

    mostrarIndicadorCarga(true);
    ocultarError();
    ocultarResultados();

    try {
        const respuesta = await fetch('/api/validar-secuencia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                secuencia: secuenciaLimpia
            })
        });

        if (!respuesta.ok) {
            const datos = await respuesta.json();
            throw new Error(datos.error || 'Error al validar la secuencia');
        }

        const datos = await respuesta.json();
        mostrarIndicadorCarga(false);
        resultadosActuales = [datos.resultado];

        // Mostrar resultados como un único registro
        mostrarResultadosManual(datos.resultado);
        aplicarFiltro('todos');

    } catch (error) {
        mostrarIndicadorCarga(false);
        mostrarError(error.message);
    }
}

function mostrarResultadosManual(resultado) {
    // Actualizar estadísticas
    document.getElementById('total-registros').textContent = '1';
    document.getElementById('total-validas').textContent = resultado.es_valida ? '1' : '0';
    document.getElementById('total-invalidas').textContent = resultado.es_valida ? '0' : '1';

    // Mostrar sección de resultados
    seccionResultados.style.display = 'block';
    seccionResultados.scrollIntoView({ behavior: 'smooth' });

    // Renderizar tarjeta única
    renderizarTarjetas([resultado]);
}

// ================================================
// EVENT LISTENERS - DRAG AND DROP
// ================================================

dropzone.addEventListener('click', () => archivoInput.click());

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('activa');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('activa');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('activa');
    
    const archivos = e.dataTransfer.files;
    if (archivos.length > 0) {
        seleccionarArchivo(archivos[0]);
    }
});

archivoInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        seleccionarArchivo(e.target.files[0]);
    }
});

// ================================================
// MANEJO DE SELECCIÓN DE ARCHIVO
// ================================================

function seleccionarArchivo(archivo) {
    archivoSeleccionado = archivo;
    mostrarNombreArchivo(archivo.name);
    btnValidar.disabled = false;
}

function mostrarNombreArchivo(nombre) {
    nombreArchivoDiv.textContent = `✓ Archivo seleccionado: ${nombre}`;
    nombreArchivoDiv.classList.add('mostrado');
}

// ================================================
// VALIDACIÓN
// ================================================

btnValidar.addEventListener('click', validarArchivo);

async function validarArchivo() {
    if (!archivoSeleccionado) {
        mostrarError('Por favor selecciona un archivo');
        return;
    }

    const formData = new FormData();
    formData.append('archivo', archivoSeleccionado);

    // Mostrar indicador de carga
    mostrarIndicadorCarga(true);
    ocultarError();
    ocultarResultados();

    try {
        const respuesta = await fetch('/api/validar', {
            method: 'POST',
            body: formData
        });

        if (!respuesta.ok) {
            const datos = await respuesta.json();
            throw new Error(datos.error || 'Error al validar el archivo');
        }

        const datos = await respuesta.json();
        mostrarIndicadorCarga(false);
        resultadosActuales = datos.resultados;
        mostrarResultados(datos);
        aplicarFiltro('todos');

    } catch (error) {
        mostrarIndicadorCarga(false);
        mostrarError(error.message);
    }
}

// ================================================
// VISUALIZACIÓN DE RESULTADOS
// ================================================

function mostrarResultados(datos) {
    // Actualizar estadísticas
    document.getElementById('total-registros').textContent = datos.total_registros;
    document.getElementById('total-validas').textContent = datos.total_validas;
    document.getElementById('total-invalidas').textContent = 
        datos.total_registros - datos.total_validas;

    // Mostrar sección de resultados
    seccionResultados.style.display = 'block';
    seccionResultados.scrollIntoView({ behavior: 'smooth' });

    // Renderizar tarjetas de resultados
    renderizarTarjetas(datos.resultados);
}

function renderizarTarjetas(resultados) {
    contenedorResultados.innerHTML = '';

    resultados.forEach((resultado, indice) => {
        const tarjeta = document.createElement('div');
        tarjeta.className = `tarjeta-resultado ${resultado.es_valida ? 'valida' : 'invalida'}`;
        tarjeta.setAttribute('data-indice', indice);
        tarjeta.setAttribute('data-estado', resultado.es_valida ? 'valida' : 'invalida');

        const estado = resultado.es_valida ? 'Válida' : 'Inválida';
        const claseEstado = resultado.es_valida ? 'estado-valido' : 'estado-invalido';

        tarjeta.innerHTML = `
            <div class="tarjeta-encabezado">
                <span class="nombre-registro">${resultado.nombre_registro}</span>
                <span class="estado-validacion ${claseEstado}">${estado}</span>
            </div>
            <p class="motivo-validacion">${resultado.motivo}</p>
            <p class="valor-detalle" style="margin-bottom: 15px; word-break: break-word;">
                <strong>Secuencia:</strong> ${resultado.secuencia.substring(0, 50)}${resultado.secuencia.length > 50 ? '...' : ''}
            </p>
            <div class="botones-tarjeta">
                <button class="boton-detalles" onclick="mostrarDetalles(${indice})">
                    Ver detalles
                </button>
                <button class="boton-copiar" onclick="copiarSecuencia(${indice}, this)">
                    Copiar secuencia
                </button>
            </div>
        `;

        contenedorResultados.appendChild(tarjeta);
    });
}

// ================================================
// MODAL DE DETALLES
// ================================================

function mostrarDetalles(indice) {
    const resultado = resultadosActuales[indice];
    const modalCuerpo = document.getElementById('modal-cuerpo');

    const posicionesPatrones = `
        <div class="detalle-fila">
            <span class="etiqueta-detalle">ATG</span>
            <div class="posiciones-lista">
                ${resultado.coincidencias.posiciones_atg.length > 0 
                    ? resultado.coincidencias.posiciones_atg.map(p => 
                        `<span class="posicion-badge">${p}</span>`
                    ).join('')
                    : '<span class="posicion-badge">No encontrado</span>'
                }
            </div>
        </div>
        <div class="detalle-fila">
            <span class="etiqueta-detalle">TAA</span>
            <div class="posiciones-lista">
                ${resultado.coincidencias.posiciones_taa.length > 0 
                    ? resultado.coincidencias.posiciones_taa.map(p => 
                        `<span class="posicion-badge">${p}</span>`
                    ).join('')
                    : '<span class="posicion-badge">No encontrado</span>'
                }
            </div>
        </div>
        <div class="detalle-fila">
            <span class="etiqueta-detalle">TAG</span>
            <div class="posiciones-lista">
                ${resultado.coincidencias.posiciones_tag.length > 0 
                    ? resultado.coincidencias.posiciones_tag.map(p => 
                        `<span class="posicion-badge">${p}</span>`
                    ).join('')
                    : '<span class="posicion-badge">No encontrado</span>'
                }
            </div>
        </div>
        <div class="detalle-fila">
            <span class="etiqueta-detalle">TGA</span>
            <div class="posiciones-lista">
                ${resultado.coincidencias.posiciones_tga.length > 0 
                    ? resultado.coincidencias.posiciones_tga.map(p => 
                        `<span class="posicion-badge">${p}</span>`
                    ).join('')
                    : '<span class="posicion-badge">No encontrado</span>'
                }
            </div>
        </div>
    `;

    const estadosAFD = resultado.recorrido_afd.estados_visitados.map(e => 
        `<span class="estado-afd">${e}</span>`
    ).join('');

    modalCuerpo.innerHTML = `
        <h3>${resultado.nombre_registro}</h3>
        
        <div class="detalle-fila">
            <span class="etiqueta-detalle">Estado</span>
            <span class="valor-detalle">
                ${resultado.es_valida ? '✓ Válida' : '✗ Inválida'}
            </span>
        </div>

        <div class="detalle-fila">
            <span class="etiqueta-detalle">Motivo</span>
            <span class="valor-detalle">${resultado.motivo}</span>
        </div>

        <div class="detalle-fila">
            <span class="etiqueta-detalle">Secuencia Completa</span>
            <span class="valor-detalle">${resultado.secuencia}</span>
        </div>

        <div class="detalle-fila">
            <span class="etiqueta-detalle">Longitud</span>
            <span class="valor-detalle">${resultado.secuencia.length} nucleótidos</span>
        </div>

        <h3 style="margin-top: 20px; margin-bottom: 15px;">Patrones Encontrados (KMP)</h3>
        ${posicionesPatrones}

        <h3 style="margin-top: 20px; margin-bottom: 15px;">Simulación AFD</h3>
        <div class="detalle-fila">
            <span class="etiqueta-detalle">Aceptada</span>
            <span class="valor-detalle">
                ${resultado.recorrido_afd.aceptada ? '✓ Sí' : '✗ No'}
            </span>
        </div>

        <div class="detalle-fila">
            <span class="etiqueta-detalle">Estado Final</span>
            <span class="valor-detalle">${resultado.recorrido_afd.estado_final}</span>
        </div>

        <div class="detalle-fila">
            <span class="etiqueta-detalle">Estados Visitados</span>
            <div class="estados-afd">${estadosAFD}</div>
        </div>
    `;

    modal.style.display = 'flex';
}

btnCerrarModal.addEventListener('click', () => {
    modal.style.display = 'none';
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// ================================================
// FILTROS
// ================================================

document.querySelectorAll('.boton-filtro').forEach(boton => {
    boton.addEventListener('click', (e) => {
        document.querySelectorAll('.boton-filtro').forEach(b => b.classList.remove('activo'));
        e.target.classList.add('activo');
        aplicarFiltro(e.target.getAttribute('data-filtro'));
    });
});

function aplicarFiltro(filtro) {
    filtroActual = filtro;
    const tarjetas = document.querySelectorAll('.tarjeta-resultado');

    tarjetas.forEach(tarjeta => {
        const estado = tarjeta.getAttribute('data-estado');
        let mostrar = false;

        if (filtro === 'todos') {
            mostrar = true;
        } else if (filtro === 'validas' && estado === 'valida') {
            mostrar = true;
        } else if (filtro === 'invalidos' && estado === 'invalida') {
            mostrar = true;
        }

        tarjeta.style.display = mostrar ? 'block' : 'none';
    });
}

// ================================================
// COPIAR SECUENCIA
// ================================================

function copiarSecuencia(indice, boton) {
    const resultado = resultadosActuales[indice];
    
    navigator.clipboard.writeText(resultado.secuencia).then(() => {
        const textoOriginal = boton.textContent;
        boton.textContent = '✓ Copiada';
        boton.classList.add('copiado');

        setTimeout(() => {
            boton.textContent = textoOriginal;
            boton.classList.remove('copiado');
        }, 2000);
    }).catch(err => {
        console.error('Error al copiar:', err);
    });
}

// ================================================
// FUNCIONES DE UTILIDAD
// ================================================

function mostrarIndicadorCarga(mostrar) {
    indicadorCarga.style.display = mostrar ? 'block' : 'none';
}

function mostrarError(mensaje) {
    mensajeError.textContent = mensaje;
    seccionError.style.display = 'block';
    seccionError.scrollIntoView({ behavior: 'smooth' });
}

function ocultarError() {
    seccionError.style.display = 'none';
}

function ocultarResultados() {
    seccionResultados.style.display = 'none';
}
