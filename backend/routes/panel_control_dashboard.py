from flask import jsonify, Blueprint, render_template, request
from database.conexion import get_connection
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)
    
@dashboard_bp.route('/dashboard/estadisticas', methods=["GET"])
def obtener_resumen_mensual():
    conn = None
    cursor = None
    try:
        # Obtenemos el mes y año actual
        hoy = datetime.now()
        mes_actual = hoy.month
        anio_actual = hoy.year

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

       
        query = """
            SELECT 
            
                COUNT(CASE WHEN estado_reserva != 'cancelada' THEN 1 END) AS total_reservas,
                
                COALESCE(SUM(CASE WHEN estado_reserva IN ('pendiente', 'confirmada') THEN cantidad_personas END), 0) AS comensales_esperados,
                
                COUNT(CASE WHEN estado_reserva = 'cancelada' THEN 1 END) AS cancelaciones
            FROM reservas
            WHERE MONTH(fecha) = %s AND YEAR(fecha) = %s
        """
        
        cursor.execute(query, (mes_actual, anio_actual))
        resultado = cursor.fetchone()

        return jsonify({
            "message": "Estadísticas mensuales obtenidas con éxito",
            "data": {
                "total_reservas": resultado['total_reservas'],
                "comensales_esperados": int(resultado['comensales_esperados']), # int() por si COALESCE devuelve un Decimal
                "cancelaciones": resultado['cancelaciones'],
                "mes": mes_actual,
                "anio": anio_actual
            }
        }), 200

    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error al conectarse con la base de datos",
                "level": "error",
                "description": f"Error interno del servidor: {e}"
            }]
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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


@dashboard_bp.route('/dashboard/reservas-semana', methods=["GET"])
def obtener_reservas_semana():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                DAYOFWEEK(fecha) as dia_numero,
                DATE(fecha) as fecha,
                COUNT(*) as reservas
            FROM reservas
            WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            AND estado_reserva != 'cancelada'
            GROUP BY DATE(fecha), DAYOFWEEK(fecha)
            ORDER BY fecha ASC
        """

        cursor.execute(query)
        resultado = cursor.fetchall()

        dias_map = {1: "Dom", 2: "Lun", 3: "Mar", 4: "Mié", 5: "Jue", 6: "Vie", 7: "Sáb"}

        data = [
            {
                "dia": dias_map.get(row["dia_numero"], "?"),
                "reservas": row["reservas"]
            }
            for row in resultado
        ]

        return jsonify({
            "message": "Reservas de los últimos 7 días obtenidas con éxito",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error al obtener reservas semanales",
                "level": "error",
                "description": f"Error interno del servidor: {e}"
            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()