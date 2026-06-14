import logging
from flask import Blueprint, render_template
import requests

logger = logging.getLogger(__name__)

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin():
    datos = {
        "total_reservas": 0,
        "comensales_esperados": 0,
        "cancelaciones": 0
    }
    labels = []
    valores = []
    error_estadisticas = False
    error_semana = False

    try:
        response = requests.get("http://localhost:5001/dashboard/estadisticas")
        if response.status_code == 200:
            resultado = response.json()
            datos = resultado["data"]
        else:
            error_estadisticas = True
    except Exception as e:
        logger.error("Error trayendo estadísticas: %s", e)
        error_estadisticas = True

    try:
        response_semana = requests.get("http://localhost:5001/dashboard/reservas-semana")
        if response_semana.status_code == 200:
            semana = response_semana.json()["data"]
            if len(semana) > 0:
                labels = [d["dia"] for d in semana]
                valores = [d["reservas"] for d in semana]
        else:
            error_semana = True
    except Exception as e:
        logger.error("Error trayendo reservas semanales: %s", e)
        error_semana = True

    return render_template(
        "admin_panel_de_control.html",
        usuario_autenticado="Admin",
        total_reservas=datos["total_reservas"],
        comensales_esperados=datos["comensales_esperados"],
        cancelaciones=datos["cancelaciones"],
        labels=labels,
        valores=valores,
        error_estadisticas=error_estadisticas,
        error_semana=error_semana
    )