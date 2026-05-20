from flask import jsonify, Blueprint, request
from database import db
from utils import generar_paginacion


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
        query_conteo = """SELECT COUNT(*) as total FROM reseñas"""
        cursor.execute(query_conteo)
        total = cursor.fetchone()['total']
        
        query = """SELECT re.id_reserva, re.puntaje, re.comentario, re.fecha_publicacion, r.nombre_cliente
                   FROM reseñas re
                   INNER JOIN reservas r ON re.id_reserva = r.id_reserva
                   ORDER BY re.fecha_publicacion DESC
                   LIMIT %s OFFSET %s
                """
        
        cursor.execute(query, (limit, offset))
        resultados = cursor.fetchall()
        
        #convertimos las fechas a string para que no den error al serializar a json
        
        for fila in resultados:
            if fila:
                fila['fecha_publicacion'] = fila['fecha_publicacion'].strftime('%Y-%m-%d %H:%M:%S') #convertir un objeto de fecha y hora en texto (string) legible para humanos o para sistemas (como un JSON).
        
        
        
        links = generar_paginacion(limit, offset, request, total)
        
        
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

@reseñas_bp.route("", methods=['POST'])
def crear_reseña():
    data = request.get_json()
    conn = None
    cursor = None
    
    if not data:
        return jsonify({
            "errors":[{
                "code":"400",
                "message":"Ingrese los datos correspondientes de la reseña",
                "level":"error",
                "Description": "Faltan los datos de la reseña"
            }]
        }), 400
    
    puntaje = data.get('puntaje')
    id_reserva = data.get('id_reserva')
    comentario = data.get('comentario')
    
    if not puntaje or not id_reserva or not comentario:
        return jsonify({
            "errors":[{
                "code":"400",
                "message":"Por favor ingrese todos los datos correspondientes",
                "level":"error",
                "Description": "Falta alguno de los datos de la reseña"
            }]
        }), 400
        
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        # 3. Validar si la reserva existe y si el estado es 'asistio'
        query_check = "SELECT estado_reserva FROM reservas WHERE id_reservas = %s"
        cursor.execute(query_check, (id_reserva,))
        reserva = cursor.fetchone()
        
        if not reserva:
            return jsonify({
                'errors': [{
                    'code': '404',
                    'message': 'La reserva indicada no existe',
                    'level': 'error',
                    'description': f'No se encontro una reserva para el id reserva: {id_reserva}'
                }]
            }), 404
        
        if reserva['estado_reserva'] != 'asistio':
            return jsonify({
                "errors":[{
                    "code": "403",
                    "message": "Solo puedes enviar una reseña si ya asistitste al restaurante",
                    "level": "error",
                    "description": "El estado de la reserva no es el correspondiente para ingresar a una reserva"
                }]
            }), 403
        
        query_duplicado = "SELECT id_resena FROM resenas WHERE id_reserva = %s"
        cursor.execute(query_duplicado, (id_reserva,))
        if cursor.fetchone():
            return jsonify({
                "errors":[{
                    "code":"409",
                    "message": "Ya se hizo una reseña para la correspondiente reserva",
                    "level": "error",
                    "description": "Por favor si quiere hacer una reseña nueva haga una nueva reserva, o modifique la que ya hizo"
                }]
            }), 409
            
        query_insert = "INSERT INTO resenas (id_reserva, estrellas, comentario) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (id_reserva, puntaje, comentario))
        conn.commit()

        return jsonify({
            "message": "Reseña guardada con éxito",
            "id_resena": cursor.lastrowid
        }), 201
        
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

@reseñas_bp.route('/buscar', methods=['GET'])
def buscar_reseñas_por_email():
    email = request.args.get('email')
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    
    except ValueError:
        offset = 0
        limit = 10
    
    if not email:
        return jsonify({
            "errors":[{
                "code":"400",
                "message":"Por favor ingrese el email que queres buscar",
                "level":"error",
                "Description": "Falta el mail por el cual buscar"
            }]
        }), 400
       
    conn = None
    cursor = None
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query_conteo = """
                      SELECT COUNT(*) as total 
                      FROM reseñas re
                      INNER JOIN reservas r ON re.id_reserva = r.id_reserva
                      WHERE r.cliente_email = %s
                      """
        cursor.execute(query_conteo,(email))
        total = cursor.fetchone()['total']

        query = """
            SELECT re.id_reseña, re.puntaje, re.comentario, re.fecha_publicacion, r.id_reserva, r.nombre_cliente, r.cliente_email
            FROM reseñas re
            INNER JOIN reservas r ON re.id_reserva = r.id_reserva
            WHERE r.cliente_email = %s
            ORDER BY re.fecha_publicacion DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (email, limit, offset))
        resultados = cursor.fetchall()

        for fila in resultados:
            if fila['fecha_publicacion']:
                fila['fecha_publicacion'] = fila['fecha_publicacion'].strftime('%Y-%m-%d %H:%M:%S')
        
        links = generar_paginacion(limit, offset, request, total)
        

        return jsonify({
            "message": f"Reseñas de {email}",
            "resultado": resultados,
            "links": links
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


@reseñas_bp.route('/admin/reseñas', methods=['GET'])
def obtener_reseñas_admin():
    conn = None
    cursor = None
    try:

        limit = int(request.args.get('_limit', 10)) #para traer 10 registros
        offset = int(request.args.get('_offset', 0))

        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query_conteo = """
            SELECT COUNT(*) as total
            FROM reseñas
        """#aca conteo la cantidad de resultados, necesario si bien muestro las primeras 10, asi puedo verificar la cantidad de paginas

        cursor.execute(query_conteo)
        total = cursor.fetchone()['total']

        query = """
            SELECT id_reseña,
                   puntaje,
                   comentario,
                   fecha_publicacion,
                   r.nombre_cliente,
                   r.cliente_email,
                   r.estado_reserva
            FROM reseñas 
            INNER JOIN reservas r
                ON reseñas.id_reserva = r.id_reserva
            ORDER BY fecha_publicacion DESC
            LIMIT %s OFFSET %s
        """

        cursor.execute(query, (limit, offset)) #ejecuto la query con los limites de paginacion

        resultados = cursor.fetchall() #trae todos los resultados, sin el limit

        for fila in resultados:
            if fila['fecha_publicacion']:
                fila['fecha_publicacion'] = fila['fecha_publicacion'].strftime('%Y-%m-%d %H:%M:%S') #esto es para mostrar las fechas en el json, ya que el datetime aveces no lo puede mostrar

        links = generar_paginacion(limit, offset, request, total)

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        return jsonify({
            "message": "Listado de reseñas para administrador",
            "resultado": resultados,
            "_links": links
        }), 200

    except Exception as e:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error interno del servidor",
                "description": str(e)
            }]
        }), 500


    
    