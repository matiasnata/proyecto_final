from flask import Flask
from routes.inicio import inicio_bp
from routes.menu import menu_bp
from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp
from routes.admin import admin_bp
from routes.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(reseñas_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)