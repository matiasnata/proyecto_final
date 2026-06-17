from flask import Blueprint, redirect, url_for, request, render_template
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
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
        response = requests.post(f'{API_BASE_URL}/reservas', json=data, timeout=5)

        if response.status_code == 201:
            return redirect(url_for('inicio.inicio'))
        elif response.status_code == 409:
            return redirect(url_for('inicio.inicio'))
        else:
            return redirect(url_for('inicio.inicio'))

    except Timeout:
        return redirect(url_for('inicio.inicio'))
    except ConnectionError:
        return redirect(url_for('inicio.inicio'))
    except RequestException as e:
        return redirect(url_for('inicio.inicio'))
    
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
        response = requests.get(f"{API_BASE_URL}/reservas/admin", params=parametros_para_backend, timeout=5)
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
        
    except Timeout:
        print("Error: Timeout al obtener reservas")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener reservas")
    except RequestException as e:
        print(f"Error inesperado al obtener reservas: {e}")

    return render_template("admin_reservas.html", usuario_autenticado="Admin", total_reservas=total_reservas, link_prev=link_prev, link_next=link_next, link_first=link_first, link_last=link_last)

@reservas_bp.route("/admin/reservas/confirmar/<int:id_reserva>", methods=["POST"])
def admin_confirmar_reserva(id_reserva):
    try:
        requests.put(f"{API_BASE_URL}/reservas/{id_reserva}", json={"estado_reserva": "asistio"}, timeout=5)
    except Timeout:
        print("Error: Timeout al confirmar reserva")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para confirmar reserva")
    except RequestException as e:
        print(f"Error inesperado al confirmar reserva: {e}")
    return redirect(url_for("reservas.admin_reservas"))

@reservas_bp.route("/admin/reservas/cancelar/<int:id_reserva>", methods=["POST"])
def admin_cancelar_reserva(id_reserva):
    try:
        requests.delete(f"{API_BASE_URL}/reservas/{id_reserva}", timeout=5)
    except Timeout:
        print("Error: Timeout al cancelar reserva")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para cancelar reserva")
    except RequestException as e:
        print(f"Error inesperado al cancelar reserva: {e}")
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
        requests.put(f"{API_BASE_URL}/reservas/{id_reserva}", json=datos_actualizados, timeout=5)
    except Timeout:
        print("Error: Timeout al editar reserva")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para editar reserva")
    except RequestException as e:
        print(f"Error inesperado al editar reserva: {e}")
    return redirect(url_for("reservas.admin_reservas"))