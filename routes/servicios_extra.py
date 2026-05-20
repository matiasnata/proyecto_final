
from flask import Flask, jsonify, request, Blueprint
from database import db
from mysql.connector import Error

servicios_extra_bp= Blueprint('servicios_extra', __name__)

@servicios_extra_bp.route("/restaurante/servicios-extra", methods =['GET'])
def ver_servicios_extra():
    #dbs y cursor None caso donde no se conecto y se cierra con finally y ni existen las variables declaradas
    dbs = None
    cursor = None
    try:
        dbs = db.get_connection()
        cursor = dbs.cursor(dictionary = True)
        query = """
        SELECT *
        FROM servicios_extra as s_e
        WHERE s_e.activo = True
        """
        cursor.execute(query)
        servicios_extra = cursor.fetchall()

        if not servicios_extra:
            return jsonify ({"message":"Por el momento no contamos con ninguno servicio extra"}), 200
        return jsonify(servicios_extra), 200

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
        cursor.close()
        dbs.close()

@servicios_extra_bp.route("/restaurante/admin/servicios-extra", methods =['POST'])
def agregar_servicio_extra():
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
        dbs = db.get_connection()
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


