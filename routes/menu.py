from flask import Blueprint, request, jsonify
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


@menu_bp.route("/admin/menu/<int:id_plato>", methods=["PUT"])
def editar_plato_admin(id_plato):
    data = request.get_json()
    conn = None
    cursor = None

    if not data:
        return jsonify({
            "errors": [{
                "code": "400",
                "message": "Faltan los datos para actualizar",
                "level": "error"
            }]
        }), 400  # Bad request

    # Extrae los datos del JSON usando los nombres de la base de datos
    nombre_plato = data.get('nombre_plato')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    url_imagen = data.get('url_imagen')
    restricciones = data.get('restricciones')
    plato_disponible = data.get('plato_disponible')

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Verifica si el plato existe usando id_plato
        cursor.execute("SELECT id_plato FROM menu WHERE id_plato = %s", (id_plato,))
        if not cursor.fetchone():
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "El plato indicado no existe",
                    "level": "error"
                }]
            }), 404  # No encontrado

        # Ejecuta la actualización en la base de datos
        query = """
            UPDATE menu 
            SET nombre_plato = %s, descripcion = %s, precio = %s, url_imagen = %s, restricciones = %s, plato_disponible = %s
            WHERE id_plato = %s
        """
        cursor.execute(query, (nombre_plato, descripcion, precio, url_imagen, restricciones, plato_disponible, id_plato))
        conn.commit()

        return jsonify({
            "message": f"Plato con ID {id_plato} actualizado correctamente"
        }), 200  # Éxito

    except Exception as e:
        if conn: 
            conn.rollback()  # Deshace cambios si hay error
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error al intentar actualizar el plato",
                "description": str(e)
            }]
        }), 500  # Error interno del servidor
    
    # Cierra conexión de forma segura sin romper nada del GET    
    finally:
        if cursor: 
            cursor.close()
        if conn: 
            conn.close()
