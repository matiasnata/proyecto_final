from flask import jsonify, Blueprint, render_template
from database.db import get_connection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/estadistica", methods=["GET"])
def mostrar_dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT COUNT(*) AS total FROM reservas WHERE estado_reserva = 'pendiente' "
    cursor.execute(query)
    resultado = cursor.fetchone()
    total_pendientes = resultado["total"]

    query = """ SELECT COUNT(*) AS total FROM reservas WHERE estado_reserva IN 
            ('confirmada', 'asistio') AND MONTH(fecha) = MONTH(CURRENT_DATE())
            AND YEAR(fecha) = YEAR(CURRENT_DATE())"""
    cursor.execute(query)
    resultado = cursor.fetchone()
    total_reservas_mes = resultado["total"]

    query = "SELECT SUM(cantidad_personas) AS total FROM reservas WHERE estado_reserva = 'confirmada' "
    cursor.execute(query)
    resultado = cursor.fetchone()
    total_personas_esperadas = resultado["total"] if resultado['total'] is not None else 0
    
    cursor.close()
    conn.close()


    return render_template("admin.html", pendientes=total_pendientes, 
                           personas_esperadas=total_personas_esperadas, 
                           reservas_mes = total_reservas_mes)


@dashboard_bp.route('/admin/promedio', methods=["GET"])
def obtener_promedio_puntaje():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                ROUND(AVG(puntaje), 1) as promedio, 
                COUNT(*) as total_reseñas 
            FROM reseñas
        """
        cursor.execute(query)
        resultado = cursor.fetchone()
        
        promedio = resultado['promedio'] if resultado['promedio'] is not None else 0.0
        total = resultado['total_reseñas']
        
        return jsonify({
            "promedio": promedio,
            "total_reseñas": total
        }), 200

    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error inesperado al calcular el promedio de las reseñas",
                "level": "error",
                "description": f"Error interno del servidor: {e}"
            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
