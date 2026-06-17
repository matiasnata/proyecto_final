// "Espera a que el HTML termine de cargar antes de hacer nada"
document.addEventListener("DOMContentLoaded", function() {
    
    const canvas = document.getElementById('graficoTendencia'); // "Busca la pizarra por su ID"
    const ctx = canvas.getContext('2d'); // "Agarra el pincel para dibujar en 2D"

// "Lee lo que dice data-meses y conviértelo en una lista (JSON.parse)"
    const etiquetasMeses = JSON.parse(canvas.getAttribute('data-meses'));
    
    // "Lee lo que dice data-promedios y conviértelo en números"
    const datosPromedios = JSON.parse(canvas.getAttribute('data-promedios'));

    new Chart(ctx, {
        type: 'line', // 1. TIPO DE GRÁFICO: Queremos uno de líneas.
        
        data: {
            labels: etiquetasMeses, // 2. EJE X (Abajo): Pon los nombres de los meses.
            datasets: [{
                label: 'Promedio de Reseñas',
                data: datosPromedios,   // 3. EJE Y (Los puntos): Usa los promedios numéricos.
                
                // 4. DECORACIÓN (Pura estética):
                borderColor: '#2E5C3A', // Color de la línea 
                borderWidth: 2,         // Grosor de la línea
                tension: 0.4,           // Hace que la línea sea curva (0 es recta, 1 es muy curva)
                pointRadius: 3          // Tamaño de los puntitos en cada mes
            }]
        },
        
        options: {
            responsive: true, // "Ajusta tu tamaño si la pantalla se achica"
            maintainAspectRatio: false, // "No te preocupes por mantener la proporción, queremos que se adapte al contenedor"
            plugins: { 
                legend: { display: false } // "Oculta el cuadrito que dice 'Promedio de Reseñas' arriba"
            },
            scales: {
                y: { 
                    beginAtZero: true, // "El gráfico empieza en 0"
                    max: 5             // "El techo del gráfico es 5 (porque las reseñas son de 1 a 5)"
                }
            }
        }
    });
});