from flask import Flask, jsonify, request, Blueprint
from database import conexion
from mysql.connector import Error

servicios_extra_bp= Blueprint('servicios_extra', __name__)

@servicios_extra_bp.route("/restaurante/servicios-extra", methods =['GET'])
def ver_servicios_extras():
    #dbs y cursor None caso donde no se conecto y se cierra con finally y ni existen las variables declaradas
    dbs = None
    cursor = None
    try:
        dbs = conexion.get_connection()
        cursor = dbs.cursor(dictionary = True)
        query = """
        SELECT id_servicio, nombre_servicio, descripcion
        FROM servicios_extras as s_e
        WHERE s_e.activo = True
        """
        cursor.execute(query)
        servicios_extras = cursor.fetchall()

        if not servicios_extras:
            return jsonify ({"message":"Por el momento no contamos con ninguno servicio extra"}), 200
        return jsonify(servicios_extras), 200

    except Error as e:
        return jsonify({
            "Error": [{
                "code": 500,
                "message": "Error con la conexion a la base de datos",
                "level": "error",
                "description": f"Fallo interno del servidor, {str(e)}"

            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if dbs and dbs.is_connected():
            dbs.close()

@servicios_extra_bp.route("/restaurante/admin/servicios-extra", methods =['POST'])
def agregar_servicio_extras():
    # dbs y cursor None caso donde no se conecto y se cierra con finally y ni existen las variables declaradas
    dbs = None
    cursor = None

    servicio = request.get_json()
    if not servicio or "nombre_servicio" not in servicio or "descripcion" not in servicio:
        return jsonify({
            "Error": [{
                "code": 400,
                "message": "todos los campos deben estar completos",
                "level": "error",
                "description": "Falta nombre de servicio o descripcion"
            }]
    }), 400

    nombre = servicio["nombre_servicio"]
    descripcion = servicio["descripcion"]
    if not nombre or not descripcion:
        return jsonify({
            "Error":[{
                "code": 400,
                "message": "Se necesita un servicio para agregar",
                "level": "error",
                "description": "Ingrese todos los valores para el servicio"
                }]
        }), 400
    try:
        dbs = conexion.get_connection()
        cursor = dbs.cursor(dictionary=True)
        validacion_query="""
        SELECT id_servicio, nombre_servicio
        FROM servicios_extras
        WHERE nombre_servicio = %s
        """
        cursor.execute(validacion_query, (nombre,))
        validacion = cursor.fetchone()
        if validacion:
            return jsonify ({
                "Error":[{
                    "code":409,
                    "message": "Ya existe ese servicio",
                    "level":"error",
                    "description": "Los servicio no se pueden repetir"
                }]
            }), 409

        query = """
                INSERT INTO servicios_extras
                (nombre_servicio, descripcion)
                VALUES (%s,%s)
                """
        cursor.execute(query, (nombre, descripcion))

        dbs.commit()

        nuevo_id = cursor.lastrowid
        return jsonify ({
            "message":"Su servicio extra fue agregado con exito a la base de datos",
            "id_servicio": f"el servicio se agrego con el numero de id: {nuevo_id}",
            "code":201,
        }), 201

    except Error as e:
        return jsonify({
            "Error": [{
                "code": 500,
                "message": "Error con la conexion a la base de datos",
                "level": "error",
                "description": f"Fallo interno del servidor, {str(e)}"

            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if dbs and dbs.is_connected():
            dbs.close()

@servicios_extra_bp.route("/restaurante/admin/servicios-extra/<int:id>", methods =['DELETE'])
def eliminar_servicio_extras(id):
    # dbs y cursor None caso donde no se conecto y se cierra con finally y ni existen las variables declaradas
    dbs = None
    cursor = None
    try:
        dbs = conexion.get_connection()
        cursor = dbs.cursor(dictionary = True)
        validacion_query="""
        SELECT id_servicio
        FROM servicios_extras 
        WHERE id_servicio = %s
        """
        cursor.execute(validacion_query, (id,))
        validacion = cursor.fetchone()
        if not validacion:
            return jsonify({
                "Error":[{
                    "code": 404,
                    "message":"No existe el servicio",
                    "level":"error",
                    "description": "No se encontro el servicio con ese numero de ID"
                }]
            }), 404
        query = """
        DELETE
        FROM servicios_extras
        WHERE id_servicio = %s
        """
        cursor.execute(query, (id,))
        dbs.commit()
        borrados = cursor.rowcount
        if borrados:
            return jsonify({
                "message":"El servicio fue borrado con exito",
                "code": 200 ,
                "level":"success",
            }), 200
    except Error as e:
        return jsonify({
            "Error": [{
                "code": 500,
                "message": "Error con la conexion a la base de datos",
                "level": "error",
                "description": f"Fallo interno del servidor, {str(e)}"

            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if dbs and dbs.is_connected():
            dbs.close()
@servicios_extra_bp.route("/restaurante/admin/servicios-extra/<int:id>", methods =['PATCH'])
def alta_baja_modificacion_servicio_extras(id):
    dbs = None
    cursor = None
    actualizar = request.get_json()
    if not actualizar or "descripcion" not in actualizar or "activo" not in actualizar:
        return jsonify({
            "Error":[{
                "code": 400,
                "message": "Se necesita un servicio para actualizar",
                "level": "error",
                "description": "Todos los campos son obligatorios"
            }]
        }), 400
    try:
        dbs = conexion.get_connection()
        cursor = dbs.cursor(dictionary = True)
        validacion_query="""
        SELECT id_servicio
        FROM servicios_extras
        WHERE id_servicio = %s
        """
        cursor.execute(validacion_query, (id,))
        validacion = cursor.fetchone()
        if not validacion:
            return jsonify({
                "Error":[{
                    "code": 404,
                    "message":"No existe el servicio",
                    "level":"error",
                    "description": "No se encontro un servicio con ese id en la base de datos"
                }]
            }), 404
        descripcion_actualizar = actualizar["descripcion"]
        estado_actualizar = actualizar["activo"]
        if not isinstance(estado_actualizar, bool):
            return jsonify({
                "Error":[{
                    "code": 400,
                    "message": "El campo activo debe ser true o false",
                    "level": "Error",
                    "description": "El campo activo solo acepta valores booleanos"
                }]
            }), 400
        query = """
        UPDATE servicios_extras
        SET descripcion = %s, activo = %s
        WHERE id_servicio = %s
        """
        cursor.execute(query, (descripcion_actualizar,estado_actualizar,id,))
        dbs.commit()
        verificacion = cursor.rowcount
        if verificacion:
            return jsonify({
                "message": "Se actualizo el servicio con exito",
                "code": 200
            }), 200
    except Error as e:
        return jsonify({
            "Error": [{
                "code": 500,
                "message": "Error con la conexion a la base de datos",
                "level": "error",
                "description": f"Fallo interno del servidor, {str(e)}"
            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if dbs and dbs.is_connected():
            dbs.close()
@servicios_extra_bp.route("/restaurante/servicios-extra/<int:id>", methods =['GET'])
def servicio_extras_por_id(id):
    dbs = None
    cursor = None
    try:
        dbs = conexion.get_connection()
        cursor = dbs.cursor(dictionary=True)
        query = """ 
        SELECT nombre_servicio, descripcion
        FROM servicios_extras 
        WHERE id_servicio = %s 
        """
        cursor.execute(query, (id,))
        validacion = cursor.fetchone()
        if not validacion:
            return jsonify({
                "Error": [{
                    "code": 404,
                    "message": "No existe el servicio",
                    "level": "error",
                    "description": "No se encontro el servicio con ese numero de ID"
                }]
            }), 404
        return jsonify ({
            "message":"Se encontro un servicio con ese numero de ID",
            "servicio": validacion,
            "code": 200
        }), 200
    except Error as e:
        return jsonify({
            "Error": [{
                "code": 500,
                "message": "Error con la conexion a la base de datos",
                "level": "error",
                "description": f"Fallo interno del servidor, {str(e)}"
            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if dbs and dbs.is_connected():
            dbs.close()
    
