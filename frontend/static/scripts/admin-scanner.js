const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const resultado = document.getElementById("resultado");
const ctx = canvas.getContext("2d");

// Iniciamos la camara
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(stream => {
        video.srcObject = stream;
        video.play();
        requestAnimationFrame(scanear);
    })
    .catch(err => {
        resultado.innerHTML = `<p class="error">No se pudo acceder a la cámara: ${err.message}</p>`;
    });

function scanear() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const qr = jsQR(imageData.data, imageData.width, imageData.height);

        if (qr) {
            confirmarReserva(qr.data);
            return; // paramos el loop
        }
    }
    requestAnimationFrame(scanear);
}

function confirmarReserva(token) {
    resultado.innerHTML = `<p class="procesando">Procesando QR...</p>`;

    fetch("/admin/scanner/verificar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token_qr: token })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            resultado.innerHTML = `<p class="exito">✓ ${data.message}</p>`;
        } else {
            resultado.innerHTML = `<p class="error">✗ ${data.errors[0].message}</p>`;
        }
    })
    .catch(err => {
        resultado.innerHTML = `<p class="error">Error de conexión: ${err.message}</p>`;
    });
}