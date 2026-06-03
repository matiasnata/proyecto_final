const fila1 = document.getElementById('fila1');
const fila2 = document.getElementById('fila2');
const hoy = new Date();

for (let i = 0; i < 8; i++) {
    const fecha = new Date(hoy);
    fecha.setDate(hoy.getDate() + i);

    const dias = ['DOM', 'LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB'];
    const meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];

    const div = document.createElement('div');
    div.classList.add('dia_calendario');
    div.innerHTML = `
        <span>${dias[fecha.getDay()]}</span><br>
        <strong>${fecha.getDate()}</strong><br>
        <span>${meses[fecha.getMonth()]}</span>
    `;

    const anio = fecha.getFullYear();
    const mes  = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia  = String(fecha.getDate()).padStart(2, '0');
    div.dataset.fechaIso = `${anio}-${mes}-${dia}`;

    div.addEventListener('click', function() {
        document.querySelectorAll('.dia_calendario').forEach(d => d.classList.remove('seleccionado'));
        this.classList.add('seleccionado');
        document.getElementById('input_fecha').value = this.dataset.fechaIso;
        actualizarResumen();
    });

    if (i < 4) {
        fila1.appendChild(div);
    } else {
        fila2.appendChild(div);
    }
}

const fila_hora1 = document.getElementById('fila_hora1');
const fila_hora2 = document.getElementById('fila_hora2');
const horas = ['13:00', '13:30', '14:00', '20:00', '20:30', '21:00', '21:30', '22:00'];

horas.forEach(function(hora, i) {
    const div = document.createElement('div');
    div.classList.add('horario');
    div.textContent = hora;
    div.addEventListener('click', function() {
        document.querySelectorAll('.horario').forEach(h => h.classList.remove('seleccionado'));
        this.classList.add('seleccionado');
        document.getElementById('input_hora').value = hora;
        actualizarResumen();
    });
    if (i < 4) {
        fila_hora1.appendChild(div);
    } else {
        fila_hora2.appendChild(div);
    }
});

document.querySelector('.sumar').addEventListener('click', function() {
    let p = document.querySelector('.cantidad_personas');
    let cantidad = parseInt(p.textContent);
    if (cantidad < 12) {
        p.textContent = cantidad + 1;
        document.getElementById('input_personas').value = cantidad + 1;
        actualizarResumen();
    }
});

document.querySelector('.restar').addEventListener('click', function() {
    let p = document.querySelector('.cantidad_personas');
    let cantidad = parseInt(p.textContent);
    if (cantidad > 1) {
        p.textContent = cantidad - 1;
        document.getElementById('input_personas').value = cantidad - 1;
        actualizarResumen();
    }
});

document.getElementById('form_reserva').addEventListener('submit', function(e) {
    const nombre = document.querySelector('.input_reserva[name="nombre_cliente"]').value.trim();
    const email  = document.querySelector('.input_reserva[name="cliente_email"]').value.trim();
    const fecha  = document.getElementById('input_fecha').value;
    const hora   = document.getElementById('input_hora').value;

    if (!nombre) {
        e.preventDefault();
        alert('Por favor ingresá tu nombre completo.');
        return;
    }
    if (!email || !email.includes('@')) {
        e.preventDefault();
        alert('Por favor ingresá un correo electrónico válido.');
        return;
    }
    if (!fecha) {
        e.preventDefault();
        alert('Por favor seleccioná una fecha.');
        return;
    }
    if (!hora) {
        e.preventDefault();
        alert('Por favor seleccioná un horario.');
        return;
    }
});

function actualizarResumen() {
    const fechaSeleccionada = document.querySelector('.dia_calendario.seleccionado');
    const horaSeleccionada  = document.querySelector('.horario.seleccionado');
    const personas          = document.querySelector('.cantidad_personas').textContent;
    const datos             = document.querySelectorAll('.resumen_dato');

    if (fechaSeleccionada) {
        datos[0].textContent = 'Fecha: ' + fechaSeleccionada.textContent.trim();
    }
    if (horaSeleccionada) {
        datos[1].textContent = 'Hora: ' + horaSeleccionada.textContent;
    }
    datos[2].textContent = 'Personas: ' + personas;
}