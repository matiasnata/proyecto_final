from flask import Blueprint, render_template, request
import requests
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
            json={"token_qr": data["token_qr"]}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500