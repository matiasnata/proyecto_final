from flask import Flask
from routes.inicio import inicio_bp

app = Flask(__name__)

app.register_blueprint(inicio_bp)

if __name__ == '__main__':
    app.run(port=8080, debug=True)