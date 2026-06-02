from flask import Flask
from flask_cors import CORS
from routes.menu import menu_bp       
from routes.reservas import reservas_bp 
from routes.panel_control_dashboard import dashboard_bp
from routes.servicios_extra import servicios_extra_bp
from routes.reseñas import reseñas_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(menu_bp)      
app.register_blueprint(reservas_bp)
app.register_blueprint(reseñas_bp)   
app.register_blueprint(servicios_extra_bp)   
app.register_blueprint(dashboard_bp)      

if __name__ == '__main__':
    app.run(port=5001, debug=True)