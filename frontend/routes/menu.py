from flask import Blueprint, render_template, request
import requests

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu")
def menu():
    response = requests.get("http://localhost:5001/api/menu")
    platos = response.json()
    return render_template("menu.html", platos=platos)