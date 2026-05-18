from flask import Blueprint, jsonify
from database.db import get_connection

menu_bp = Blueprint("menu",__name__)

@menu_bp.route("/menu", methods=["GET"])
def obtener_menu():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM menu"
        cursor.execute(query)

        menu = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(menu), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500