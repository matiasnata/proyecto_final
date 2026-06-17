from flask import Blueprint, render_template
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from config import API_BASE_URL

inicio_bp = Blueprint("inicio", __name__)

@inicio_bp.route("/")
def inicio():
    platos = []
    reseñas = []
    servicios_extra = []
    
    try:
        resultado_backend_platos = requests.get(f"{API_BASE_URL}/platos", timeout=5)
        if resultado_backend_platos.status_code == 200:
            platos = resultado_backend_platos.json()
    except Timeout:
        print("Error: Timeout al obtener platos")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener platos")
    except RequestException as e:
        print(f"Error inesperado al obtener platos: {e}")

    try:
        resultado_backend_reseñas = requests.get(f"{API_BASE_URL}/reseñas?_limit=6", timeout=5)
        if resultado_backend_reseñas.status_code == 200:
            reseñas = resultado_backend_reseñas.json().get("resultado", [])
    except Timeout:
        print("Error: Timeout al obtener reseñas")
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener reseñas")
    except RequestException as e:
        print(f"Error inesperado al obtener reseñas: {e}")
        
    try: 
        resultado_backend_servicios_extra = requests.get(f"{API_BASE_URL}/restaurante/servicios-extra", timeout=5) 
        if resultado_backend_servicios_extra.status_code == 200:
            servicios_extra = resultado_backend_servicios_extra.json()
    except Timeout:
        print("Error: Timeout al obtener servicios extra")       
    except ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener servicios_extra")  
    except RequestException as e:
        print(f"Error inesperado al obtener servicios extra: {e}")     
    
    return render_template("index.html", platos=platos, reseñas=reseñas,servicios_extra=servicios_extra)