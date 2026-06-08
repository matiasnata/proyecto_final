from flask import Flask, render_template
from routes.inicio import inicio_bp
from routes.menu import menu_bp
from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.scanner import scanner_bp
from routes.servicios_extra import servicios_extra_bp

app = Flask(__name__)

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
    return render_template('404.html', usuario_autenticado="Juan"), 404

@app.errorhandler(500)
def error_interno_servidor(e):
    return render_template('500.html', usuario_autenticado="Juan"), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)