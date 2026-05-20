from flask import Blueprint, request, jsonify, render_template
from database.db import get_connection
from mysql.connector import Error
import uuid #Esto sirve para generar el codigo QR

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route('/reservas/<int:id_reservas>', methods=['GET'])
def buscar_reserva_por_id(id_reservas):
    if id_reservas <= 0:
        return jsonify({
            'errors': [{
                'code': 400,
                'message': 'Parametros invalidos',
                'description': 'El id buscado tiene que ser un numero entero y positivo.'
            }]
        }), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM reservas WHERE id_reservas = %s"
        cursor.execute(query, (id_reservas,))
        resultado = cursor.fetchone()
        
        
        if resultado == None:
            cursor.close()
            conn.close() 
            return jsonify({
                'errors':[{
                    'code':'404',
                    'message':'Dato inexistente',
                    'description':'El id buscado no tiene una reserva asignada'
                }]
            }), 404
        else:
            cursor.close()
            conn.close()
            return jsonify(resultado),200
    except:
        return jsonify({
            'errors': [{
                'code': 500,
                'message': "Error interno del servidor",
                'description': 'Fallo interno del servidor'
                }]
            }), 500

@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():
    data = request.json
    if not data or 'nombre_cliente' not in data or 'cliente_email' not in data or 'cantidad_personas' not in data or 'fecha' not in data or 'hora' not in data:
        return jsonify({
            'errors':[{
                'code': '400',
                'message': 'Parametros invalidos',
                'description': 'Corroborar datos ingresados'
            }]
        }), 400
    
    conn = get_connection
    cursor = conn.cursor(dictionary=True)
        
    try:
        query_busqueda = "SELECT cliente_email FROM reservas WHERE cliente_email = %s"
        cursor.execute(query_busqueda, (data['cliente_email'],))
        email_buscado = cursor.fetchone()
        if email_buscado is not None:
            cursor.close()
            conn.close()
            return jsonify({
                'errors': [{
                    'code': '409',
                    'message': 'Email duplicado',
                    'description': 'El email ya existe, ingresa otro'
                }]
            }), 409
            
            
        else:
            token_qr = str(uuid.uuid4)
            guarda_valores = f"INSERT INTO reservas(nombre_cliente, cliente_email, cantidad_personas, fecha, hora, token_qr, estado_reserva) VALUES (%s,%s,%s,%s,%s,%s,'pendiente' )"
            valores = (data["nombre_cliente"], data["cliente_email"], data["cantidad_personas"], data["fecha"], data["hora"], token_qr)
            cursor.execute(guarda_valores, valores)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify ({
                'message':'La reserva fue creada con exito',
                'token_qr': token_qr
                }), 201
        
    except:
        return jsonify({
            'errors': [{
                'code': 500,
                'message': "Error interno del servidor",
                'description': 'Fallo interno del servidor'
                }]
            }), 500

@reservas_bp.route('/reservas/<int:id_reservas>', methods=['PUT'])
def actualizar_reserva_id(id_reservas):
    data = request.json
    if not data or 'nombre_cliente' not in data or 'cliente_email' not in data or 'cantidad_personas' not in data or 'fecha' not in data or 'hora' not in data:
        return jsonify({
            'errors':[{
                'code': '400',
                'message': 'Parametros invalidos',
                'description': 'Corroborar datos ingresados'
            }]
        }), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT cliente_email FROM reservas WHERE cliente_email = %s", (data['cliente_email'],))
        email_buscado = cursor.fetchone()
        if email_buscado is not None:
            cursor.close()
            conn.close()
            return jsonify({
                'errors': [{
                    'code': '409',
                    'message': 'Email duplicado',
                    'description': 'El email ya existe, ingresa otro'
                }]
            }), 409
        
        else: 
            nombre_ingresado = data["nombre_cliente"]
            email_ingresado = data["cliente_email"]
            cantidad_personas_ingresada= data["cantidad_personas"]
            fecha_ingresada = data["fecha"]
            hora_ingresada = data["hora"]

            cursor.execute ("SELECT * FROM reservas where id_reservas = %s", (id_reservas,))    
            actualizar= cursor.fetchone()
            
            if actualizar:
                query_update = "UPDATE reservas SET nombre_cliente = %s, cliente_email = %s, cantidad_personas = %s, fecha = %s, hora = %s WHERE id_reservas = %s"
                valores_update = (nombre_ingresado, email_ingresado, cantidad_personas_ingresada, fecha_ingresada, hora_ingresada, id_reservas)
                cursor.execute(query_update, valores_update)
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({"message": "La reserva fue modificada con exito"}), 200
            
            else:
                cursor.close()
                conn.close()
                return jsonify({
                    'errors': [{
                        'code': '404',
                        'message': 'Dato inexistente',
                        'description': f'No se encontro ninguna reserva con el id {id_reservas} para modificar.'
                    }]
                }), 404
        
    except:
        return jsonify({
            'errors': [{
                'code': '500',
                'message': "Error interno del servidor",
                'description': 'Fallo interno del servidor'
                }]
            }), 500

@reservas_bp.route('/reservas/<int:id_reservas>/cancelar', methods=['PATCH'])
def cancelar_reserva_id(id_reservas):
    if id_reservas <= 0:
        return jsonify({
            'errors':[ {
                'code': '400',
                'message': 'Parametros invalidos',
                'description': 'El id buscado tiene que ser un numero entero y positivo.'
            }]
        }), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        estado_nuevo = 'cancelada'
        cursor.execute("SELECT * FROM reservas where id_reservas = %s", (id_reservas,))
        actualizar = cursor.fetchone()

        if actualizar:
            query_update = "UPDATE reservas SET estado_reserva = %s WHERE id_reservas = %s"
            valores_update = (estado_nuevo, id_reservas)
            
            cursor.execute(query_update, valores_update)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": f"La reserva {id_reservas} fue cancelada con exito"}), 200
            
        else:
            cursor.close()
            conn.close()
            return jsonify({
                'errors': [ {
                    'code': '404',
                    'message': 'Dato inexistente',
                    'description': f'No se encontro ninguna reserva con el id {id_reservas} para cancelar.'
                }]
            }), 404

    except:
        return jsonify({
            'errors': [ {
                'code': '500',
                'message': "Error interno del servidor",
                'description': 'Fallo interno del servidor'
            }]
        }), 500

def consultar_disponiblidad_hora():
    fecha = request.args.get('fecha')
    turnos_fijos = ['11:00', '12:30', '14:00', '15:30', '17:00', '20:00', '21:30', '23:00']
    conn = None
    cursor = None
    capacidad_max = 100
    if not fecha:
        return jsonify({
            "errors":[{
                "code":"400",
                "message":"Eija primero la fecha",
                "level":"error",
                "Description": "Falta el parametro fecha"
            }]
        }), 400
    
    try:
        conn = get_connection()
        cursor = conn.cusor(dictionary=True)
        
        query = """SELECT hora, COALESCE(SUM(cantidad_personas), o
        0) as total_personas
        FROM reservas
        WHERE fecha=%s AND estado_reserva IN ('pendiente', 'confirmada')
        GROUP BY hora"""
        
        cursor.execute(query,(fecha,))
        resultados = cursor.fecthall()
        
        ocupacion_por_hora = {}
        
        for fila in resultados:
            hora_str = str(fila['hora'])[:5]
            ocupacion_por_hora[hora_str] = int['total_personas']
            
        turnos_disponibles = []
        
        for turno in turnos_fijos:
            ocupacion_actual = ocupacion_por_hora.get(turno, 0)
            
            if ocupacion_actual < capacidad_max:
                turnos_disponibles.append(turno)
                
        return jsonify({
            "fecha": fecha,
            "horarios_disponibles": turnos_disponibles
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
    
@reservas_bp.route("/reservas/admin", methods = ["GET"])        
def mostrar_reservas_dashboard():
    
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT nombre_cliente, cantidad_personas, fecha, hora, estado_reserva FROM reservas"
    cursor.execute(query)
    reservas = cursor.fetchall()
    cursor.close()
    
    return render_template("admin.html", total_reservas = reservas)
      
    