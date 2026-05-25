from flask import jsonify, Blueprint, request
from database import db
from utils import generar_paginacion
from datetime import datetime

reseñas_bp = Blueprint('reseñas', __name__, url_prefix="/api/reseñas")

@reseñas_bp.route('', methods=["GET"])
def obtener_reseñas():
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    
    except ValueError:
        offset = 0
        limit = 10
    
    email = request.args.get('email',"")
    
        
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query_conteo = """SELECT COUNT(*) as total FROM reseñas re 
                          INNER JOIN reservas r ON re.id_reserva = r.id_reserva"""
        
        query_base= """SELECT re.id_reseña, re.id_reserva, re.puntaje, re.comentario, re.fecha_publicacion, r.nombre_cliente, r.cliente_email
                   FROM reseñas re
                   INNER JOIN reservas r ON re.id_reserva = r.id_reserva
                """
        condiciones = []
        params_filtro = []

        if email:
            condiciones.append("r.cliente_email = %s")
            params_filtro.append(email)

        # Si hay condiciones (como el email), se las agregamos a AMBAS consultas
        if condiciones:
            clausula_where = " WHERE " + " AND ".join(condiciones) #.join es genial ya que si hay mas de una ondiion se agregaria un and.
            query_conteo += clausula_where
            query_base += clausula_where

        # 4. Ejecutamos el conteo primero (usando los parámetros de filtro)
        cursor.execute(query_conteo, params_filtro)
        total = cursor.fetchone()['total']

        # 5. Terminamos de armar la consulta principal agregando ORDER y LIMIT
        query_base += " ORDER BY re.fecha_publicacion DESC LIMIT %s OFFSET %s"
        
        # Sumamos los parámetros del filtro con los del límite
        params_finales = params_filtro + [limit, offset]
        
        # Ejecutamos la búsqueda principal
        cursor.execute(query_base, params_finales)
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
            
        query_insert = "INSERT INTO reseñas (id_reserva, puntaje, comentario) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (id_reserva, puntaje, comentario))
        conn.commit()

        return jsonify({
            "message": "Reseña guardada con éxito",
            "id_reseña": cursor.lastrowid
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

@reseñas_bp.route('/admin', methods=['GET'])
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

        resultados = cursor.fetchall() #trae todos los resultados devueltos por la query

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


@reseñas_bp.route('/admin/<int:id>', methods=['DELETE'])
def eliminar_reseña_admin(id):
    conn = None
    cursor = None
    try:
        conn = db.get_connection()  # Conexión con la DB
        cursor = conn.cursor(dictionary=True)  # Como se van a traer los datos de la DB

        # Verifico si existe la reseña
        query_check = "SELECT id_reseña FROM reseñas WHERE id_reseña = %s"  
        cursor.execute(query_check, (id,))  # Busca coincidencia en la DB con el id
        reseña = cursor.fetchone()  # Guarda el resultado en reseña

        if not reseña:
            return jsonify({
                'errors': [{
                    'code': '404',  
                    'message': 'La reseña indicada no existe',
                    'level': 'error',
                    'description': f'No se encontró una reseña con el id: {id}'
                }]
            }), 404  # No encontrado

        # Si existe la reseña, la elimina
        query_delete = "DELETE FROM reseñas WHERE id_reseña = %s"
        cursor.execute(query_delete, (id,))
        conn.commit()  # Guarda los cambios en la DB

        return jsonify({
            "message": f"Reseña {id} eliminada con éxito"
        }), 200  # Éxito

    except Exception as e:
        if conn:
            conn.rollback()  # Si algo falla, se deshace cualquier cambio a medias
            
        return jsonify({
            "errors": [{
                "code": "500",  
                "message": "Error al intentar eliminar la reseña",
                "level": "error",
                "description": str(e)
            }]
        }), 500  # Error interno del servidor
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reseñas_bp.route('/admin/promedio', methods=['GET'])
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
        conn = db.get_connection()
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

    
    