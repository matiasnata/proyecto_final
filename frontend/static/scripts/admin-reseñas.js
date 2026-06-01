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
            
            // Le quitamos la clase oculta y le ponemos la visible (¡Aparece el HTML!)
            ventana.classList.replace('ventana-oculta', 'ventana-visible'); 
        });
    });

    // 3. ¿Qué pasa si toca Cancelar en nuestro modal?
    btnCancelar.addEventListener('click', () => {
        ventana.classList.replace('ventana-visible', 'ventana-oculta'); // Escondemos el cartel
        formularioActual = null; // Limpiamos la memoria por las dudas
    });

    // 4. ¿Qué pasa si toca Confirmar en nuestro modal?
    btnConfirmar.addEventListener('click', () => {
        if (formularioActual) {
            // Agarramos el formulario que teníamos en memoria y lo mandamos a la fuerza
            formularioActual.submit(); 
        }
    });
});