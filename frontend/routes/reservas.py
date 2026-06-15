from flask import Blueprint, redirect, url_for, request, render_template
import requests
from config import API_BASE_URL

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
        response = requests.post(f'{API_BASE_URL}/reservas', json=data)

        if response.status_code == 201:
            return render_template('index.html', confirmacion='¡Reserva creada con éxito! Pronto recibirás un código QR por mail.')
        elif response.status_code == 409:
            return render_template('index.html', error='El email ya existe, ingresá otro.')
        else:
            return render_template('index.html', error='Hubo un error, intentá de nuevo.')

    except requests.exceptions.ConnectionError:
        return render_template('index.html', error='No se pudo conectar con el servidor, intentá más tarde.')

@reservas_bp.route("/admin/reservas")
def admin_reservas():
    limit = request.args.get('_limit', 5)   
    offset = request.args.get('_offset', 0)
    url_backend = f"{API_BASE_URL}/reservas/admin"
    
    parametros_para_backend = {
        '_limit': limit,
        '_offset': offset
    }
    
    total_reservas = []
    link_prev = {}
    link_next = {}
    link_first = {}
    link_last = {}
    
    try:
        response = requests.get(f"{API_BASE_URL}/reservas/admin", params=parametros_para_backend)
        if response.status_code == 200:
            total_reservas = response.json().get("data", [])
            links = response.json().get("links", [])
        
        url_frontend_base = url_for('reservas.admin_reservas')
        
        def corregir_link(link_backend):
            if link_backend and 'href' in link_backend:
                # Reemplazamos el dominio del backend por el del frontend
                link_backend['href'] = link_backend['href'].replace(f'{API_BASE_URL}/reservas/admin', url_frontend_base)
            return link_backend
        
        
        link_prev = corregir_link(links.get('prev', {}))
        link_next = corregir_link(links.get('next', {}))
        link_first = corregir_link(links.get('first', {}))
        link_last = corregir_link(links.get('last', {}))
        
    except Exception as e:
        print("Error al buscar reservas:", e)
    return render_template("admin_reservas.html", usuario_autenticado="Admin", total_reservas=total_reservas, link_prev=link_prev, link_next=link_next, link_first=link_first, link_last=link_last)

@reservas_bp.route("/admin/reservas/confirmar/<int:id_reserva>", methods=["POST"])
def admin_confirmar_reserva(id_reserva):
    try:
        requests.put(f"{API_BASE_URL}/reservas/{id_reserva}", json={"estado_reserva": "asistio"})
    except Exception as e:
        print("Error confirmando asistencia:", e)
    return redirect(url_for("reservas.admin_reservas"))

@reservas_bp.route("/admin/reservas/cancelar/<int:id_reserva>", methods=["POST"])
def admin_cancelar_reserva(id_reserva):
    try:
        requests.delete(f"{API_BASE_URL}/reservas/{id_reserva}")
    except Exception as e:
        print("Error cancelando:", e)
    return redirect(url_for("reservas.admin_reservas"))

@reservas_bp.route("/admin/reservas/editar/<int:id_reserva>", methods=["POST"])
def admin_guardar_edicion_reserva(id_reserva):
    datos_actualizados = {
        "nombre_cliente": request.form.get("nombre_cliente"),
        "cantidad_personas": request.form.get("cantidad_personas"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "estado_reserva": request.form.get("estado_reserva")
    }
    try:
        requests.put(f"{API_BASE_URL}/reservas/{id_reserva}", json=datos_actualizados)
    except Exception as e:
        print("Error actualizando:", e)
    return redirect(url_for("reservas.admin_reservas"))