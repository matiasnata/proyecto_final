from flask import Blueprint, jsonify, request
from database.conexion import get_connection
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    conn = None
    cursor = None
    try:
        body = request.get_json()
        email = body.get("email")
        password = body.get("password")

        if not email or not password:
            return jsonify({
                "errors": [{
                    "code": "400",
                    "message": "Email y contraseña son requeridos",
                    "level": "error"
                }]
            }), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM administradores WHERE email = %s", (email,))
        admin = cursor.fetchone()

        if not admin:
            return jsonify({
                "errors": [{
                    "code": "401",
                    "message": "Credenciales incorrectas",
                    "level": "error"
                }]
            }), 401

        if not bcrypt.checkpw(password.encode("utf-8"), admin["password_hash"].encode("utf-8")):
            return jsonify({
                "errors": [{
                    "code": "401",
                    "message": "Credenciales incorrectas",
                    "level": "error"
                }]
            }), 401

        return jsonify({
            "message": "Login exitoso",
            "data": {
                "id": admin["id"],
                "nombre": admin["nombre"],
                "email": admin["email"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "level": "error",
                "description": f"{e}"
            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()