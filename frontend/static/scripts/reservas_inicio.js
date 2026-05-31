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

    div.addEventListener('click', function() {
        document.querySelectorAll('.dia_calendario').forEach(d => d.classList.remove('seleccionado'));
        this.classList.add('seleccionado');
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
        actualizarResumen();
    }
});

document.querySelector('.restar').addEventListener('click', function() {
    let p = document.querySelector('.cantidad_personas');
    let cantidad = parseInt(p.textContent);
    if (cantidad > 1) {
        p.textContent = cantidad - 1;
        actualizarResumen();
    }
});

document.querySelector('.boton_confirmar').addEventListener('click', function() {
    const datos = document.querySelectorAll('.resumen_dato');
    const fechaSeleccionada = document.querySelector('.dia_calendario.seleccionado');
    const horaSeleccionada = document.querySelector('.horario.seleccionado');
    const personas = document.querySelector('.cantidad_personas').textContent;

    if (fechaSeleccionada) datos[0].textContent = 'Fecha: ' + fechaSeleccionada.textContent.trim();
    if (horaSeleccionada) datos[1].textContent = 'Hora: ' + horaSeleccionada.textContent;
    datos[2].textContent = 'Personas: ' + personas;

    document.querySelector('.calendario').style.display = 'none';
    document.querySelector('.horarios').style.display = 'none';
    document.querySelector('.personas').style.display = 'none';
    document.querySelector('.resumen').style.display = 'none';
    document.querySelector('.confirmacion').style.display = 'block';
});

function actualizarResumen() {
    const fechaSeleccionada = document.querySelector('.dia_calendario.seleccionado');
    const horaSeleccionada = document.querySelector('.horario.seleccionado');
    const personas = document.querySelector('.cantidad_personas').textContent;
    const datos = document.querySelectorAll('.resumen_dato');

    if (fechaSeleccionada) {
        datos[0].textContent = 'Fecha: ' + fechaSeleccionada.textContent.trim();
    }
    if (horaSeleccionada) {
        datos[1].textContent = 'Hora: ' + horaSeleccionada.textContent;
    }
    datos[2].textContent = 'Personas: ' + personas;
}