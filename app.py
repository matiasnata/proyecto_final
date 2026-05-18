from flask import Flask
from routes.inicio import inicio_bp
from routes.menu import menu_bp       
from routes.reservas import reservas_bp 

app = Flask(__name__)

app.register_blueprint(inicio_bp)
app.register_blueprint(menu_bp)      
app.register_blueprint(reservas_bp)   

if __name__ == '__main__':
    app.run(port=8080, debug=True)