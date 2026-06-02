from flask import Blueprint, render_template
import requests


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin():

    datos = {
        "total_reservas": 0,
        "comensales_esperados": 0,
        "cancelaciones": 0
    }

    try:
        response = requests.get(
            "http://localhost:5001/dashboard/estadisticas"
        )

        if response.status_code == 200:
            resultado = response.json()
            datos = resultado["data"]

    except Exception as e:
        print("Error trayendo estadísticas:", e)

    return render_template(
        "admin_panel_de_control.html",
        usuario_autenticado="Admin",
        total_reservas=datos["total_reservas"],
        comensales_esperados=datos["comensales_esperados"],
        cancelaciones=datos["cancelaciones"]
    )