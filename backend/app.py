import os
import logging
from flask import Flask
from flask_mail import Mail
from routes.menu import menu_bp
from routes.reservas import reservas_bp, init_mail
from routes.panel_control_dashboard import dashboard_bp
from routes.servicios_extra import servicios_extra_bp
from routes.reseñas import reseñas_bp
from routes.auth import auth_bp
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Pasamos el objeto mail al blueprint de reservas
init_mail(mail)

app.register_blueprint(menu_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(reseñas_bp)   
app.register_blueprint(servicios_extra_bp)   
app.register_blueprint(dashboard_bp)     
app.register_blueprint(auth_bp)   

if __name__ == '__main__':
    app.run(port=5001, debug=True)