from flask import jsonify, Blueprint, request
from database import db


reseñas_bp = Blueprint('reseñas', __name__, url_prefix="/api/reseñas")

@reseñas_bp.route('', methods=["GET"])
def obtener_reseñas():
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    
    except ValueError:
        offset = 0
        limit = 10
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT re.id_reserva", re.puntaje, re.comentario, re.fecha_publicacion, r.nombre_cliente, r.cliente_email
                   FROM reseñas re
                   INNER JOIN reservas r ON re.id_reserva = r.id_reserva
                   ORDER BY re.fecha_publicacion DESC
                   LIMIT %s OFFSET %s
                """
        
        cursor.execute(query, (limit, offset))
        resultados = cursor.fetchall()
        
        #convertimos las fechas a string para que no den error al serializar a json
        
        for fila in resultados:
            fila['fecha_publicacion'] = fila['fecha_publicacion'].strftime('%Y-%M-%D %H:%m:%S')
        
        links = generar_links_paginacion(request, limit, offset)
        
        
        return jsonify({
            'message':"Se han encontrado las ultimas 10 reseñas.",
            "resultado": resultados,
            "_links": links
        }), 200
        
    except Exception as e:
        return jsonify({
            "errors":[{
                "code": "500",
                "message": "Error inesperado al conetarse con la base de datos",
                "level": "error",
                "description":f"Error interno del servidor: {e}"
            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        
        
        