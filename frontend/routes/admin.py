import logging
from flask import Blueprint, render_template
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from config import API_BASE_URL

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
        response = requests.get(f"{API_BASE_URL}/dashboard/estadisticas", timeout=5)
        if response.status_code == 200:
            resultado = response.json()
            datos = resultado["data"]
        else:
            error_estadisticas = True
    except Timeout:
        logger.error("Timeout: La API tardó demasiado en responder para estadísticas")
        error_estadisticas = True
    except ConnectionError:
        logger.error("ConnectionError: No se pudo conectar a la API para estadísticas")
        error_estadisticas = True
    except RequestException as e:
        logger.error("Error trayendo estadísticas: %s", e)
        error_estadisticas = True

    try:
        response_semana = requests.get(f"{API_BASE_URL}/dashboard/reservas-semana", timeout=5)
        if response_semana.status_code == 200:
            semana = response_semana.json()["data"]
            if len(semana) > 0:
                labels = [d["dia"] for d in semana]
                valores = [d["reservas"] for d in semana]
        else:
            error_semana = True
    except Timeout:
        logger.error("Timeout: La API tardó demasiado en responder para reservas semanales")
        error_semana = True
    except ConnectionError:
        logger.error("ConnectionError: No se pudo conectar a la API para reservas semanales")
        error_semana = True
    except RequestException as e:
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