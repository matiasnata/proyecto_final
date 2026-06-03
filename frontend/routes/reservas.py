from flask import Blueprint, request, render_template
import requests

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():
    # Recibimos los datos del formulario HTML
    data = {
        'nombre_cliente':    request.form.get('nombre_cliente'),
        'cliente_email':     request.form.get('cliente_email'),
        'cantidad_personas': request.form.get('cantidad_personas'),
        'fecha':             request.form.get('fecha'),
        'hora':              request.form.get('hora')
    }

    # Usamos la librería requests para llamar a la API del backend
    try:
        response = requests.post('http://127.0.0.1:5001/reservas', json=data)

        if response.status_code == 201:
            return render_template('index.html', confirmacion='¡Reserva creada con éxito! Pronto recibirás un código QR por mail.')
        elif response.status_code == 409:
            return render_template('index.html', error='El email ya existe, ingresá otro.')
        else:
            return render_template('index.html', error='Hubo un error, intentá de nuevo.')

    except requests.exceptions.ConnectionError:
        return render_template('index.html', error='No se pudo conectar con el servidor, intentá más tarde.')