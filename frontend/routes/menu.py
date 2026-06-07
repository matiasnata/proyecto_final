from flask import Blueprint, render_template, request, redirect, url_for
import requests

menu_bp = Blueprint('menu', __name__, url_prefix='/admin/menu')

@menu_bp.route('', methods=['GET'])
def admin_menu():
    try:
        respuesta = requests.get("http://127.0.0.1:5001/platos")
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
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        lista_platos = []

    return render_template('admin_menu.html', platos=lista_platos, usuario_autenticado="Admin")


@menu_bp.route('/agregar', methods=['POST'])
def agregar_plato():
    try:
        requests.post("http://127.0.0.1:5001/platos", json={
            "nombre_plato": request.form.get('nombre_plato'),
            "descripcion": request.form.get('descripcion'),
            "precio": float(request.form.get('precio')),
            "url_imagen": request.form.get('url_imagen') or None,
            "restricciones": request.form.get('restricciones') or None,
            "plato_disponible": request.form.get('plato_disponible') == 'True'
        })
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")

    return redirect(url_for('menu.admin_menu'))


@menu_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_plato(id):
    try:
        requests.delete(f"http://127.0.0.1:5001/platos/{id}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")

    return redirect(url_for('menu.admin_menu'))


@menu_bp.route('/modificar/<int:id>', methods=['POST'])
def modificar_plato(id):
    try:
        requests.put(f"http://127.0.0.1:5001/platos/{id}", json={
            "nombre_plato": request.form.get('nombre_plato'),
            "descripcion": request.form.get('descripcion'),
            "precio": float(request.form.get('precio')),
            "url_imagen": request.form.get('url_imagen') or None,
            "restricciones": request.form.get('restricciones') or None,
            "plato_disponible": request.form.get('plato_disponible') == 'True'
        })
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")

    return redirect(url_for('menu.admin_menu'))
