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