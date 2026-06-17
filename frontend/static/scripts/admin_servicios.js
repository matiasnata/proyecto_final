const botonAgregar = document.getElementsByClassName("Agregar")[0]
const formAgregar = document.getElementsByClassName("Agregar-servicio")[0]
                    .getElementsByTagName("form")[0]


botonAgregar.addEventListener("click", function(event) {
    if (formAgregar.classList.contains("visible")) {
        formAgregar.classList.remove("visible")  // lo oculta
    } else {
        formAgregar.classList.add("visible")     // lo muestra
    }
})

document.addEventListener('DOMContentLoaded', () => {
    // 1. Agarramos todos los elementos necesarios
    const formulariosEliminar = document.querySelectorAll('.form-eliminar');
    const ventana = document.getElementById('ventana-confirmacion');
    const btnConfirmar = document.getElementById('btn-confirmar');
    const btnCancelar = document.getElementById('btn-cancelar');

    // Esta variable va a "recordar" qué botón de eliminar tocamos exactamente
    let formularioActual = null;

    // 2. Le ponemos el freno de mano a todos los formularios de la tabla
    formulariosEliminar.forEach(formulario => {
        formulario.addEventListener('submit', (event) => {
            event.preventDefault(); // Bloqueamos el viaje al backend, bloquea la accion submit entonces nunca llega a comunicaarse con el backend

            formularioActual = formulario; // Guardamos este formulario específico en la memoria

            // Le quitamos la clase oculta y le ponemos la visible
            ventana.classList.replace('ventana-oculta', 'ventana-visible');
        });
    });

    // 3. Que pasa si toca Cancelar en nuestro modal
    btnCancelar.addEventListener('click', () => {
        ventana.classList.replace('ventana-visible', 'ventana-oculta'); // Escondemos el cartel
        formularioActual = null; // Limpiamos la memoria por las dudas
    });

    // 4. Qué pasa si toca Confirmar en nuestro modal
    btnConfirmar.addEventListener('click', () => {
        if (formularioActual) {
            // Agarramos el formulario que teníamos en memoria y lo mandamos a la fuerza
            formularioActual.submit();
        }
    });
    const botonModificar = document.querySelectorAll('.btn-verde-modificar');
    const ventanaModificar = document.getElementById('ventana-modificacion');
    const botonCancelarmodificar = document.getElementById('btn-cancelar-modificar');

    const inputId = document.getElementById('id_modificado');
    const inputNombre = document.getElementById('nombre_modificado');
    const inputDescripcion = document.getElementById('descripcion_modificado');
    const selectActivo = document.getElementById('activo_modificado');

    // Creamos una funcion flecha donde para cada boton modificar que se vaya a tocar, los datos dentro del boton
    // se pasen al formulario, de esa manera se puede agregar informacion sin perder la anterior.
    botonModificar.forEach(boton => {
        boton.addEventListener('click', () => {

            const idServicio = boton.getAttribute('data-id');
            const nombreServicio = boton.getAttribute('data-nombre');
            const descripcionServicio = boton.getAttribute('data-descripcion');
            const activoServicio = boton.getAttribute('data-activo');

            //agrego los valores

            inputId.value = idServicio;
            inputNombre.value = nombreServicio;
            inputDescripcion.value = descripcionServicio;
            selectActivo.value = activoServicio;


            ventanaModificar.classList.replace('ventana-oculta', 'ventana-visible');
        });
    });

    botonCancelarmodificar.addEventListener('click', () => {

        ventanaModificar.classList.replace('ventana-visible', 'ventana-oculta');
    });
});
