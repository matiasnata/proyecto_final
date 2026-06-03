from flask import jsonify, Blueprint, request
from database import conexion
from utils import generar_paginacion
from datetime import datetime

reseñas_bp = Blueprint('reseñas', __name__, url_prefix="/reseñas")

@reseñas_bp.route('', methods=["GET"])
def obtener_reseñas():
    try:
        limit = int(request.args.get('_limit', 5))
        offset = int(request.args.get('_offset', 0))
    
    except ValueError:
        offset = 0
        limit = 5
    
    email = request.args.get('email',"")
    
        
    try:
        conn = conexion.get_connection()
        cursor = conn.cursor(dictionary=True)
        query_conteo = """SELECT COUNT(*) as total FROM reseñas re 
                          INNER JOIN reservas r ON re.id_reserva = r.id_reservas"""
        
        query_base= """SELECT re.id_reseña, re.id_reserva, re.puntaje, re.comentario, re.fecha_publicacion, r.nombre_cliente, r.cliente_email
                   FROM reseñas re
                   INNER JOIN reservas r ON re.id_reserva = r.id_reservas
                """
        condiciones = []
        params_filtro = []

        if email:
            condiciones.append("r.cliente_email = %s")
            params_filtro.append(email)

        # Si hay condiciones (como el email), se las agregamos a AMBAS consultas
        if condiciones:
            clausula_where = " WHERE " + " AND ".join(condiciones) #.join es genial ya que si hay mas de una condiion se agregaria un and.
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
            'message':f"Se han encontrado {len(resultados)} reseñas.",
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
        conn = conexion.get_connection()
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
        
        query_duplicado = "SELECT id_reseña FROM reseñas WHERE id_reserva = %s"
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

@reseñas_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_reseña_admin(id):
    conn = None
    cursor = None
    try:
        conn = conexion.get_connection()  # Conexión con la DB
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

@reseñas_bp.route('/grafico-resenas', methods=['GET'])
def grafico_tendencia_reseñas():
    conn = None
    cursor = None
    
    anio_str = request.args.get('anio')
    anio_buscar = int(anio_str) if anio_str else datetime.now().year

    try:
        conn = conexion.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query_verificacion = "SELECT * FROM reseñas WHERE YEAR(fecha_publicacion) = %s LIMIT 1"
        cursor.execute(query_verificacion, (anio_buscar,))
        reseña_año = cursor.fetchone()
        
        if not reseña_año:
            return jsonify({
                "errors": [{
                    "code": "404",
                    "message": "No se encontraron reseñas para el año especificado",
                    "level": "error",
                    "description": f"No hay datos disponibles para el año {anio_buscar}"
                }]
            }), 404

        # 2. Buscamos el promedio agrupado por NÚMERO de mes, filtrando por el año
        query = """
            SELECT 
                MONTH(fecha_publicacion) AS mes_num,
                ROUND(AVG(puntaje), 1) AS promedio_mensual
            FROM reseñas
            WHERE YEAR(fecha_publicacion) = %s
            GROUP BY mes_num
            ORDER BY mes_num ASC
        """
        
        cursor.execute(query, (anio_buscar,))
        resultados = cursor.fetchall()

        # 3. Preparamos una lista vacía con los 12 meses (por defecto en 0), a la que luego le asignaremos el promedio que corresponde a cada mes. 
        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        promedios = [0] * 12 

        # 4. Rellenamos los meses que sí tienen datos
        for fila in resultados:
            indice_mes = fila['mes_num'] - 1 # Enero es 1, pero en la lista es el índice 0
            promedios[indice_mes] = fila['promedio_mensual']

        return jsonify({
            "meses": meses_nombres,
            "promedios": promedios
        }), 200

    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "500",
                "message": "Error inesperado al generar el gráfico de reseñas",
                "level": "error",
                "description": f"Error interno del servidor: {e}"
            }]
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            

@reseñas_bp.route('/promedio', methods=['GET'])
def obtener_promedio_reseñas():
    # Capturamos la fecha desde la URL, ej: ?fecha_desde=2024-01-01
    anio = request.args.get('anio')

    # 1. Validación de seguridad: Comprobar que la fecha tenga el formato correcto
    if anio:
        if not (anio.isdigit() and len(anio) == 4):
            return jsonify({
                "errors": [{
                    "code": "400",
                    "message": "Formato de año inválido",
                    "level": "error",
                    "description": "El parámetro anio debe ser un número de 4 dígitos, ej: 2024"
                }]
            }), 400
    conn = None
    cursor = None
    try:
        conn = conexion.get_connection()
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
        if anio:
            query += " WHERE YEAR(fecha_publicacion) = %s"
            parametros = (anio,)

        # Ejecutamos la consulta pasándole los parámetros (si los hay)
        cursor.execute(query, parametros)
        resultado = cursor.fetchone()

        promedio = resultado['promedio'] if resultado['promedio'] is not None else 0.0
        total = resultado['total_reseñas']

        return jsonify({
            "message": f"Promedio calculado {'para el año ' + anio if anio else 'de todas las reseñas'}",
            "promedio_general": promedio,
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
