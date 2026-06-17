from flask import Blueprint, render_template, request
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from config import API_BASE_URL
scanner_bp = Blueprint("scanner", __name__)

@scanner_bp.route("/admin/scanner")
def scanner():
    return render_template("admin_scanner.html", usuario_autenticado="Admin")

@scanner_bp.route("/admin/scanner/verificar", methods=["POST"])
def verificar_qr():
    data = request.get_json()
    try:
        response = requests.post(
            f"{API_BASE_URL}/reservas/verificar_qr",
            json={"token_qr": data["token_qr"]}, 
            timeout=5
        )
        return response.json(), response.status_code
    except Timeout:
        return {"error": "La API tardó demasiado en responder (Timeout)"}, 504
    except ConnectionError:
        return {"error": "No se pudo conectar con la API (Servidor caído)"}, 503
    except RequestException as e:
        return {"error": f"Error de petición: {str(e)}"}, 500