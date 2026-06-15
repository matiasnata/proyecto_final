from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from config import API_BASE_URL

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
        # si el admin ya está logueado, lo mando directo al panel
    if 'admin' in session:
        return redirect(url_for('admin.admin'))
    return render_template("login.html", error=None)

@auth_bp.route("/login", methods=["POST"])
def login_post():
    # obtengo los datos del formulario
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # llamo al backend con las credenciales
        respuesta = requests.post(f"{API_BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })

        datos = respuesta.json()

        if respuesta.status_code == 200:
            # guarda los datos del admin en la sesión
            # session es como una "memoria" que Flask guarda mientras el usuario navega
            # si el admin cierra el navegador o hace logout, la sesión se borra
            session['admin'] = datos['data']
            return redirect(url_for('admin.admin'))
        else:
            # si las credenciales son incorrectas, mostramos el error en el formulario
            error = datos['errors'][0]['message']
            return render_template("login.html", error=error)

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return render_template("login.html", error="No se pudo conectar con el servidor")