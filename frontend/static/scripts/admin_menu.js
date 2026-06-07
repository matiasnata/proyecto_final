document.addEventListener('DOMContentLoaded', function() {

    // --- AGREGAR PLATO ---
    const botonAgregar = document.getElementsByClassName("Agregar")[0]
    const formAgregar = document.getElementsByClassName("agregar-plato")[0]
                        .getElementsByTagName("form")[0]

    botonAgregar.addEventListener("click", function() {
        if (formAgregar.classList.contains("visible")) {
            formAgregar.classList.remove("visible")
        } else {
            formAgregar.classList.add("visible")
        }
    })

})

function abrirModalModificar(id, nombre, descripcion, precio, imagen, restricciones, disponible) {
    // rellena los campos con los datos del plato elegido
    document.getElementById('mod_nombre').value = nombre;
    document.getElementById('mod_descripcion').value = descripcion;
    document.getElementById('mod_precio').value = precio;
    document.getElementById('mod_imagen').value = imagen !== 'None' ? imagen : '';
    document.getElementById('mod_restricciones').value = restricciones !== 'None' ? restricciones : '';
    document.getElementById('mod_disponible').value = disponible;

    // apunta el formulario a la ruta correcta 
    const form = document.getElementById('form-modificar');
    form.action = `/admin/menu/modificar/${id}`;

    // muestra la ventana
    const modal = document.getElementById('modal-modificar');
    modal.style.display = 'flex';
}

function cerrarModalModificar() {
    // oculta la ventana
    document.getElementById('modal-modificar').style.display = 'none';
}

function abrirModalEliminar(id) {
    // apunto el formulario interno a la ruta correspondiente a ese plato
    const form = document.getElementById('form-confirmar-eliminar');
    form.action = `/admin/menu/eliminar/${id}`;

    // muestro el cartel en pantalla
    const modal = document.getElementById('modal-eliminar');
    modal.style.display = 'flex';
}

function cerrarModalEliminar() {
    // oculto el cartel si se arrepiente
    document.getElementById('modal-eliminar').style.display = 'none';
}

function filtrarPlatos() {
    // tomo lo que escribe el usuario y lo pasamos a minúsculas
    const textoBuscado = document.getElementById('buscador-platos').value.toLowerCase();
    
    // apunto a todas las filas del cuerpo de la tabla
    const filas = document.querySelectorAll('table tbody tr');

    filas.forEach(fila => {
        // extraigo solo las celdas de ID y Nombre 
        const id = fila.children[0] ? fila.children[0].textContent.toLowerCase().trim() : '';
        const nombre = fila.children[1] ? fila.children[1].textContent.toLowerCase().trim() : '';

        // evaluo si coincide con el ID exacto o si el nombre contiene el texto
        if (id === textoBuscado || nombre.includes(textoBuscado)) {
            fila.style.display = ''; // muestra la fila
        } else {
            fila.style.display = 'none'; // oculta la fila si no coincide
        }
    });
}