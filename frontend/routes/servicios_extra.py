from flask import Flask, jsonify, request, Blueprint, render_template, redirect, abort, url_for
import requests

servicios_extra_bp= Blueprint('servicios_extra', __name__, url_prefix='/admin/servicios')

# Definimos dónde está corriendo tu API backend (ajustá el puerto según el tuyo)
URL_API_BACKEND = "http://127.0.0.1:5001"

@servicios_extra_bp.route('', methods=['GET'])
def admin_servicios():
    try:

        url_completa = f"{URL_API_BACKEND}/restaurante/admin/servicios-extra"
        respuesta = requests.get(url_completa)

        lista_servicios = respuesta.json()

    except requests.exceptions.RequestException as e:
        # Manejo de errores si backend ENTERO no solo base de datos esta apagado
        print(f"Error de conexión con la API: {e}")
        return render_template('500.html', usuario_autenticado="Juan"), 500

    # API backend manda error
    if respuesta.status_code == 500:
            print(respuesta.json())
            abort(500)

    return render_template('admin_servicios.html', servicios=lista_servicios, usuario_autenticado="Juan")


@servicios_extra_bp.route('/agregar', methods=['POST'])
def agregar_servicio():
    nombre = request.form.get('nservicio')
    descripcion = request.form.get('dservicio')

    url_backend = f"{URL_API_BACKEND}/restaurante/admin/servicios-extra"

    try:
        respuesta = requests.post(url_backend, json={
            "nombre_servicio": nombre,
            "descripcion": descripcion
        })

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")

    return redirect(url_for('servicios_extra.admin_servicios'))


@servicios_extra_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_servicio(id):
    url_backend = f"{URL_API_BACKEND}/restaurante/admin/servicios-extra/{id}"

    try:
        requests.delete(url_backend)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")

    return redirect(url_for('servicios_extra.admin_servicios'))


@servicios_extra_bp.route('/modificar', methods=['POST'])
def modificar_servicio():
    id = request.form.get('id_servicio')
    descripcion = request.form.get('dmservicio')
    activo = request.form.get('amservicio')

    url_backend = f"{URL_API_BACKEND}/restaurante/admin/servicios-extra/{id}"

    try:
        requests.patch(url_backend, json={
            "descripcion": descripcion,
            "activo": activo == "True"  # convierte string a booleano para el backend
        })
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")

    return redirect(url_for('servicios_extra.admin_servicios'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)