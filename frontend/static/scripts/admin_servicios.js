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