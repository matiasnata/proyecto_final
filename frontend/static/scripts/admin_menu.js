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