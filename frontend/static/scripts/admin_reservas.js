function abrirModal(boton) {
    const id = boton.getAttribute('data-id');
    const nombre = boton.getAttribute('data-nombre');
    const personas = boton.getAttribute('data-personas');
    const fecha = boton.getAttribute('data-fecha');
    const hora = boton.getAttribute('data-hora');
    const estado = boton.getAttribute('data-estado');

    document.getElementById('formEditar').action = "/admin/reservas/editar/" + id;
    document.getElementById('modal_id_texto').innerText = "#" + id;

    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_personas').value = personas;
    
    // Formateo seguro para la fecha (primeros 10 caracteres)
    let fechaLimpia = fecha;
    if (fecha && fecha.length >= 10) {
        fechaLimpia = fecha.substring(0, 10);
    }
    document.getElementById('edit_fecha').value = fechaLimpia;
    
    // Limpieza de segundos en la hora (primeros 5 caracteres)
    let horaLimpia = hora;
    if (hora && hora.length >= 5) {
        horaLimpia = hora.substring(0, 5);
    }
    document.getElementById('edit_hora').value = horaLimpia;
    
    document.getElementById('edit_estado').value = estado;

    document.getElementById('modalEditar').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalEditar').style.display = 'none';
}