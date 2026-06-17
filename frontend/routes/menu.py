from flask import Blueprint, render_template, request, redirect, url_for
import logging
from flask import render_template, abort
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from config import API_BASE_URL

logger = logging.getLogger(__name__)
menu_bp = Blueprint('menu', __name__, url_prefix='/admin/menu')

@menu_bp.route('', methods=['GET'])
def admin_menu():
    try:
        respuesta = requests.get(f"{API_BASE_URL}/platos", timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        # valido si la API devolvió un diccionario de error o si no devolvió una lista válida
        if isinstance(datos, dict) and 'error' in datos:
            print(f"La API devolvió un error: {datos['error']}")
            lista_platos = []
        elif not isinstance(datos, list):
            print("La API no devolvió un formato de lista válido.")
            lista_platos = []
        else:
            lista_platos = datos  # si todo está bien, asigno la lista de platos

    except (Timeout, ConnectionError, RequestException) as e:
        logging.error(f"[ERROR - menu] No se pudo conectar con la API: {e}")
        abort(500)

    return render_template('admin_menu.html', platos=lista_platos, usuario_autenticado="Admin")

@menu_bp.route('', methods=['POST'])
def agregar_plato():
    try:
        response = requests.post(f"{API_BASE_URL}/platos", json={
            "nombre_plato": request.form.get('nombre_plato'),
            "descripcion": request.form.get('descripcion'),
            "precio": float(request.form.get('precio')),
            "url_imagen": request.form.get('url_imagen') or None,
            "restricciones": request.form.get('restricciones') or None,
            "plato_disponible": request.form.get('plato_disponible') == 'True'
        }, timeout=5)

        if response.status_code != 201:
            return redirect(url_for('menu.admin_menu'))

    except Timeout:
        return redirect(url_for('menu.admin_menu'))
    except ConnectionError:
        return redirect(url_for('menu.admin_menu'))
    except RequestException as e:
        return redirect(url_for('menu.admin_menu'))

    return redirect(url_for('menu.admin_menu'))

@menu_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_plato(id):
    try:
        requests.delete(f"{API_BASE_URL}/platos/{id}", timeout=5)
    except Timeout:
        print("Error: Timeout al eliminar plato")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para eliminar plato")
    except RequestException as e:
        print(f"Error inesperado al eliminar plato: {e}")

    return redirect(url_for('menu.admin_menu'))


@menu_bp.route('/modificar/<int:id>', methods=['POST'])
def modificar_plato(id):
    try:
        requests.put(f"{API_BASE_URL}/platos/{id}", json={
            "nombre_plato": request.form.get('nombre_plato'),
            "descripcion": request.form.get('descripcion'),
            "precio": float(request.form.get('precio')),
            "url_imagen": request.form.get('url_imagen') or None,
            "restricciones": request.form.get('restricciones') or None,
            "plato_disponible": request.form.get('plato_disponible') == 'True'
        }, timeout=5)
    except Timeout:
        print("Error: Timeout al modificar plato")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para modificar plato")
    except RequestException as e:
        print(f"Error inesperado al modificar plato: {e}")
        
    return redirect(url_for('menu.admin_menu'))
