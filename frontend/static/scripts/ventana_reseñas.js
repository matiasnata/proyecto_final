document.addEventListener("DOMContentLoaded", () => {
    // 1. Leemos los atributos data- del body
    const body = document.querySelector("body");
    const exito = body.getAttribute("data-exito");
    const error = body.getAttribute("data-error");

    // 2. Seleccionamos los elementos del DOM
    const ventanaExito = document.getElementById("ventana-exito");
    const ventanaError = document.getElementById("ventana-error");
    const contenedorFormulario = document.getElementById("contenedor-formulario");
    const btnCerrarExito = document.getElementById("btn-cerrar-exito");
    const btnCerrarError = document.getElementById("btn-cerrar-error");

    // 3. Lógica para mostrar la ventana de ÉXITO
    if (exito && exito.trim() !== "") { //.trim es como el .strip de python, corta los espacios en blanco
        ventanaExito.classList.replace("ventana-oculta", "ventana-visible"); 
        contenedorFormulario.style.display = "none"; // Ocultamos el formulario
    } 
    // 4. Lógica para mostrar la ventana de ERROR
    else if (error && error.trim() !== "") {
        ventanaError.classList.replace("ventana-oculta", "ventana-visible");
        contenedorFormulario.style.display = "none"; 
    }

    if (btnCerrarError) {
        btnCerrarError.addEventListener("click", () => {
            // Al ser error, solo cerramos la ventana para que intente de nuevo
            ventanaError.classList.replace("ventana-visible", "ventana-oculta");
            contenedorFormulario.style.display = "block"
        });
    }
});