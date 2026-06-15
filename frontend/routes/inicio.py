from flask import Blueprint, render_template
import requests
from config import API_BASE_URL

inicio_bp = Blueprint("inicio", __name__)

@inicio_bp.route("/")
def inicio():
    platos = []
    reseñas = []
    servicios_extra = []
    
    try:
        resultado_backend_platos = requests.get(f"{API_BASE_URL}/platos")
        if resultado_backend_platos.status_code == 200:
            platos = resultado_backend_platos.json()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener platos")

    try:
        resultado_backend_reseñas = requests.get(f"{API_BASE_URL}/reseñas?_limit=6")
        if resultado_backend_reseñas.status_code == 200:
            reseñas = resultado_backend_reseñas.json().get("resultado", [])
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener reseñas")
        
    try: 
        resultado_backend_servicios_extra = requests.get(f"{API_BASE_URL}/restaurante/servicios-extra") 
        if resultado_backend_servicios_extra.status_code == 200:
            servicios_extra = resultado_backend_servicios_extra.json()
            
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el Backend para obtener servicios_extra")       
    
    return render_template("index.html", platos=platos, reseñas=reseñas,servicios_extra=servicios_extra)