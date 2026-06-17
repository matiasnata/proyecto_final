from flask import Flask, jsonify, request, Blueprint, render_template, redirect, abort, url_for
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from config import API_BASE_URL
servicios_extra_bp= Blueprint('servicios_extra', __name__, url_prefix='/admin/servicios')


@servicios_extra_bp.route('', methods=['GET'])
def admin_servicios():
    try:

        url_completa = f"{API_BASE_URL}/restaurante/admin/servicios-extra"
        respuesta = requests.get(url_completa, timeout=5)

        lista_servicios = respuesta.json()

    except Timeout:
        print("Timeout: La API tardó mucho en responder")
        return render_template('500.html', usuario_autenticado="Admin"), 504
    except ConnectionError:
        print("Error de conexión: El backend parece estar apagado")
        return render_template('500.html', usuario_autenticado="Admin"), 503
    except RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return render_template('500.html', usuario_autenticado="Admin"), 500

    # Si la API responde pero con un error interno
    if respuesta.status_code == 500:
        print("El backend devolvió error 500:", respuesta.json())
        return render_template('500.html', usuario_autenticado="Admin"), 500

    return render_template('admin_servicios.html', servicios=lista_servicios, usuario_autenticado="Admin")


@servicios_extra_bp.route('/agregar', methods=['POST'])
def agregar_servicio():
    nombre = request.form.get('nservicio')
    descripcion = request.form.get('dservicio')

    url_backend = f"{API_BASE_URL}/restaurante/admin/servicios-extra"

    try:
        respuesta = requests.post(url_backend, json={
            "nombre_servicio": nombre,
            "descripcion": descripcion
        }, timeout=5)

    except Timeout:
        print("Timeout al intentar agregar servicio")
    except ConnectionError:
        print("Error de conexión al intentar agregar servicio")
    except RequestException as e:
        print(f"Error con la API: {e}")

    return redirect(url_for('servicios_extra.admin_servicios'))


@servicios_extra_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_servicio(id):
    url_backend = f"{API_BASE_URL}/restaurante/admin/servicios-extra/{id}"

    try:
        requests.delete(url_backend, timeout=5)
    except Timeout:
        print("Timeout al intentar eliminar servicio")
    except ConnectionError:
        print("Error de conexión al intentar eliminar servicio")
    except RequestException as e:
        print(f"Error con la API: {e}")

    return redirect(url_for('servicios_extra.admin_servicios'))


@servicios_extra_bp.route('/modificar', methods=['POST'])
def modificar_servicio():
    id = request.form.get('id_servicio')
    descripcion = request.form.get('dmservicio')
    activo = request.form.get('amservicio')

    url_backend = f"{API_BASE_URL}/restaurante/admin/servicios-extra/{id}"

    try:
        requests.patch(url_backend, json={
            "descripcion": descripcion,
            "activo": activo == "True"  # convierte string a booleano para el backend
        }, timeout=5)
    except Timeout:
        print("Timeout al intentar modificar servicio")
    except ConnectionError:
        print("Error de conexión al intentar modificar servicio")
    except RequestException as e:
        print(f"Error con la API: {e}")

    return redirect(url_for('servicios_extra.admin_servicios'))


