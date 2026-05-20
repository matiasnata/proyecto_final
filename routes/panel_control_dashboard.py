from flask import Blueprint, render_template
from database.db import get_connection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/panel_de_control", methods=["GET"])
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