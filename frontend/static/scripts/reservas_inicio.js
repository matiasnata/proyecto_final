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
    });

    if (i < 4) {
        fila1.appendChild(div);
    } else {
        fila2.appendChild(div);
    }
}