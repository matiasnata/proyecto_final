from flask import jsonify, Blueprint, render_template, request
from database.db import get_connection
from datetime import datetime

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


@dashboard_bp.route('/dashboard/promedio', methods=['GET'])
def obtener_promedio_reseñas():
    # Capturamos la fecha desde la URL, ej: ?fecha_desde=2024-01-01
    fecha_desde = request.args.get('fecha_desde')

    # 1. Validación de seguridad: Comprobar que la fecha tenga el formato correcto
    if fecha_desde:
        try:
            # Intentamos leer la fecha para asegurar que sea YYYY-MM-DD, chequea que el formato coincida y si conicide lo pasa a un objeto time que reocnoce sql.
            datetime.strptime(fecha_desde, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "errors": [{
                    "code": "400",
                    "message": "Formato de fecha inválido",
                    "level": "error",
                    "description": "El parámetro fecha_desde debe tener el formato YYYY-MM-DD"
                }]
            }), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 2. Armamos la consulta base
        query = """
            SELECT 
                ROUND(AVG(puntaje), 1) as promedio, 
                COUNT(*) as total_reseñas 
            FROM reseñas
        """
        
        parametros = ()

        # 3. Si mandaron una fecha, le agregamos el filtro WHERE a la consulta
        if fecha_desde:
            query += " WHERE fecha_publicacion >= %s"
            parametros = (fecha_desde,)

        # Ejecutamos la consulta pasándole los parámetros (si los hay)
        cursor.execute(query, parametros)
        resultado = cursor.fetchone()

        promedio = resultado['promedio'] if resultado['promedio'] is not None else 0.0
        total = resultado['total_reseñas']

        return jsonify({
            "message": f"Promedio calculado {'desde ' + fecha_desde if fecha_desde else 'histórico'}",
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
