from flask import Flask, render_template, request, session, redirect, url_for
from routes.inicio import inicio_bp
from routes.menu import menu_bp
from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.scanner import scanner_bp
from routes.servicios_extra import servicios_extra_bp
from dotenv import load_dotenv
import os
load_dotenv()  

app = Flask(__name__)
# secret_key es necesaria para usar session en Flask
# session permite recordar que el admin está logueado mientras navega por el panel
app.secret_key = os.getenv('SECRET_KEY', 'clave_super_secreta')
@app.before_request
def verificar_sesion_admin():
    # verifica si la URL a la que el usuario quiere entrar empieza con "/admin"
    if request.path.startswith('/admin'):
        # si es una ruta de admin, verificamos si no tiene la sesión iniciada
        if 'admin' not in session:
            # si no está logueado, lo mando al login
            return redirect(url_for('auth.login'))

app.register_blueprint(auth_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(reseñas_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(servicios_extra_bp)
app.register_blueprint(scanner_bp)

@app.errorhandler(404)
def pagina_no_encontrada(e):
    usuario = session.get('admin') or None
    return render_template('404.html', usuario_autenticado=usuario), 404

@app.errorhandler(500)
def error_interno_servidor(e):
    usuario = session.get('admin') or None
    return render_template('500.html', usuario_autenticado=usuario), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)