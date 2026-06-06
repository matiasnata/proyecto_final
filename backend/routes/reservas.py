from flask import Blueprint, request, jsonify
from database.conexion import get_connection
from flask_mail import Mail, Message
import qrcode
import uuid
import io

reservas_bp = Blueprint("reservas", __name__)

mail = None

def init_mail(mail_instance):
    global mail
    mail = mail_instance

def generar_qr_bytes(token_qr):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(token_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()

def enviar_email_reserva_creada(nombre, email_cliente, fecha, hora, personas, token_qr):
    try:
        qr_bytes = generar_qr_bytes(token_qr)

        msg = Message(
            subject='¡Tu reserva en Flames JB está confirmada!',
            sender=mail.default_sender,
            recipients=[email_cliente]
        )

        msg.html = f'''
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2>Hola {nombre},</h2>
            <p>Tu reserva fue creada con éxito. Acá están los detalles:</p>
            <ul>
                <li>📅 <strong>Fecha:</strong> {fecha}</li>
                <li>🕐 <strong>Hora:</strong> {hora}</li>
                <li>👥 <strong>Personas:</strong> {personas}</li>
            </ul>
            <p>Adjuntamos tu código QR. Presentalo al llegar al restaurante.</p>
            <br>
            <a href="http://127.0.0.1:5001/reservas/cancelar/{token_qr}"
               style="background-color: #c0392b; color: white; padding: 12px 24px;
                      text-decoration: none; border-radius: 6px; font-size: 16px;">
                Cancelar mi reserva
            </a>
            <br><br>
            <p>¡Te esperamos en Flames JB!<br>
            Av San Juan 1234, Boedo<br>
            📞 +54 9 11 3435-6787</p>
        </body>
        </html>
        '''

        msg.attach(
            filename='reserva_qr.png',
            content_type='image/png',
            data=qr_bytes
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Error al enviar email de reserva creada: {e}')
        return False

def enviar_email_cambio_estado(nombre, email_cliente, estado, fecha, hora):
    try:
        if estado == 'confirmada':
            asunto = 'Tu reserva en Flames JB fue confirmada'
            html = f'''
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>Hola {nombre},</h2>
                <p>¡Buenas noticias! Tu reserva fue confirmada por nuestro equipo.</p>
                <ul>
                    <li>📅 <strong>Fecha:</strong> {fecha}</li>
                    <li>🕐 <strong>Hora:</strong> {hora}</li>
                </ul>
                <p>¡Te esperamos en Flames JB!<br>
                Av San Juan 1234, Boedo<br>
                📞 +54 9 11 3435-6787</p>
            </body>
            </html>
            '''
        elif estado == 'cancelada':
            asunto = 'Tu reserva en Flames JB fue cancelada'
            html = f'''
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>Hola {nombre},</h2>
                <p>Tu reserva del <strong>{fecha}</strong> a las <strong>{hora}</strong> fue cancelada.</p>
                <p>Si tenés alguna duda, comunicate con nosotros.</p>
                <p>Flames JB<br>
                Av San Juan 1234, Boedo<br>
                📞 +54 9 11 3435-6787</p>
            </body>
            </html>
            '''
        else:
            return False

        msg = Message(
            subject=asunto,
            sender=mail.default_sender,
            recipients=[email_cliente]
        )
        msg.html = html
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Error al enviar email de cambio de estado: {e}')
        return False


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

        if resultado is None:
            cursor.close()
            conn.close()
            return jsonify({
                'errors':[{
                    'code': '404',
                    'message': 'Dato inexistente',
                    'description': 'El id buscado no tiene una reserva asignada'
                }]
            }), 404
        else:
            cursor.close()
            conn.close()
            return jsonify(resultado), 200
    except Exception as e:
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

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query_busqueda = "SELECT cliente_email FROM reservas WHERE cliente_email = %s"
        cursor.execute(query_busqueda, (data['cliente_email'],))
        email_buscado = cursor.fetchone()

        if email_buscado is not None:
            return jsonify({
                'errors': [{
                    'code': '409',
                    'message': 'Email duplicado',
                    'description': 'El email ya existe, ingresa otro'
                }]
            }), 409

        token_qr = str(uuid.uuid4())
        guarda_valores = "INSERT INTO reservas(nombre_cliente, cliente_email, cantidad_personas, fecha, hora, token_qr, estado_reserva) VALUES (%s,%s,%s,%s,%s,%s,'pendiente')"
        valores = (
            data["nombre_cliente"],
            data["cliente_email"],
            data["cantidad_personas"],
            data["fecha"],
            data["hora"],
            token_qr
        )
        cursor.execute(guarda_valores, valores)
        conn.commit()

        enviar_email_reserva_creada(
            nombre=data["nombre_cliente"],
            email_cliente=data["cliente_email"],
            fecha=data["fecha"],
            hora=data["hora"],
            personas=data["cantidad_personas"],
            token_qr=token_qr
        )

        return jsonify({
            'message': 'La reserva fue creada con exito',
            'token_qr': token_qr
        }), 201

    except Exception as e:
        print(f'ERROR DETALLADO: {e}')
        return jsonify({
            'errors': [{
                'code': 500,
                'message': "Error interno del servidor",
                'description': f'Fallo interno del servidor: {e}'
            }]
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reservas_bp.route("/reservas/admin", methods=["GET"])
def mostrar_reservas_dashboard():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_reservas, nombre_cliente, cliente_email, cantidad_personas, fecha, hora, estado_reserva FROM reservas"
        cursor.execute(query)
        reservas = cursor.fetchall()
        cursor.close()
        conn.close()

        for reserva in reservas:
            if reserva.get('fecha') is not None:
                reserva['fecha'] = str(reserva['fecha'])  # str(datetime.date) devuelve "2024-06-15"
            if reserva.get('hora') is not None:
                total_seg = int(reserva['hora'].total_seconds())  # convierte timedelta a segundos
                horas = total_seg // 3600
                minutos = (total_seg % 3600) // 60
                reserva['hora'] = f"{horas:02d}:{minutos:02d}"  # 19:00

        return jsonify({"data": reservas}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reservas_bp.route('/reservas/<int:id_reservas>', methods=['PUT'])
def actualizar_reserva_id(id_reservas):
    data = request.json

    if not data or 'nombre_cliente' not in data or 'cantidad_personas' not in data or 'fecha' not in data or 'hora' not in data:
        return jsonify({
            'errors':[{
                'code': '400',
                'message': 'Parametros invalidos',
                'description': 'Corroborar datos ingresados'
            }]
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reservas = %s", (id_reservas,))
        actualizar = cursor.fetchone()

        if actualizar:
            nuevo_estado = data.get("estado_reserva", actualizar["estado_reserva"])
            estado_anterior = actualizar["estado_reserva"]

            query_update = "UPDATE reservas SET nombre_cliente = %s, cantidad_personas = %s, fecha = %s, hora = %s, estado_reserva = %s WHERE id_reservas = %s"
            valores_update = (
                data["nombre_cliente"],
                data["cantidad_personas"],
                data["fecha"],
                data["hora"],
                nuevo_estado,
                id_reservas
            )
            cursor.execute(query_update, valores_update)
            conn.commit()

            if nuevo_estado != estado_anterior and nuevo_estado in ('confirmada', 'cancelada'):
                enviar_email_cambio_estado(
                    nombre=actualizar["nombre_cliente"],
                    email_cliente=actualizar["cliente_email"],
                    estado=nuevo_estado,
                    fecha=data["fecha"],
                    hora=data["hora"]
                )

            return jsonify({"message": "La reserva fue modificada con exito"}), 200

        else:
            return jsonify({
                'errors': [{
                    'code': '404',
                    'message': 'Dato inexistente',
                    'description': f'No se encontro ninguna reserva con el id {id_reservas} para modificar.'
                }]
            }), 404

    except Exception as e:
        return jsonify({
            'errors': [{
                'code': '500',
                'message': "Error interno del servidor",
                'description': f'Fallo interno del servidor: {e}'
            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reservas_bp.route('/reservas/<int:id_reservas>', methods=['DELETE'])
def cancelar_reserva_id(id_reservas):
    if id_reservas <= 0:
        return jsonify({
            'errors':[{
                'code': '400',
                'message': 'Parametros invalidos',
                'description': 'El id buscado tiene que ser un numero entero y positivo.'
            }]
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reservas = %s", (id_reservas,))
        reserva = cursor.fetchone()

        if reserva:
            cursor.execute(
                "UPDATE reservas SET estado_reserva = %s WHERE id_reservas = %s",
                ('cancelada', id_reservas)
            )
            conn.commit()

            enviar_email_cambio_estado(
                nombre=reserva["nombre_cliente"],
                email_cliente=reserva["cliente_email"],
                estado='cancelada',
                fecha=str(reserva["fecha"]),
                hora=str(reserva["hora"])
            )

            return jsonify({"message": f"La reserva {id_reservas} fue cancelada con exito"}), 200

        else:
            return jsonify({
                'errors':[{
                    'code': '404',
                    'message': 'Dato inexistente',
                    'description': f'No se encontro ninguna reserva con el id {id_reservas} para cancelar.'
                }]
            }), 404

    except Exception as e:
        return jsonify({
            'errors':[{
                'code': '500',
                'message': "Error interno del servidor",
                'description': f'Fallo interno del servidor: {e}'
            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reservas_bp.route("/reservas/disponibilidad", methods=['GET'])
def consultar_disponiblidad_hora():
    fecha = request.args.get('fecha')
    turnos_fijos = ['11:00', '12:30', '14:00', '15:30', '17:00', '20:00', '21:30', '23:00']
    conn = None
    cursor = None
    capacidad_max = 100

    if not fecha:
        return jsonify({
            "errors":[{
                "code": "400",
                "message": "Elija primero la fecha",
                "level": "error",
                "Description": "Falta el parametro fecha"
            }]
        }), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT hora, COALESCE(SUM(cantidad_personas), 0) as total_personas
        FROM reservas
        WHERE fecha=%s AND estado_reserva IN ('pendiente', 'confirmada')
        GROUP BY hora"""

        cursor.execute(query, (fecha,))
        resultados = cursor.fetchall()

        ocupacion_por_hora = {}
        for fila in resultados:
            hora_str = str(fila['hora'])[:5]
            ocupacion_por_hora[hora_str] = int(fila['total_personas'])

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
                "message": "Error inesperado al conectarse con la base de datos",
                "level": "error",
                "description": f"Error interno del servidor: {e}"
            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reservas_bp.route("/reservas/verificar_qr", methods=['POST'])
def verificar_qr():
    data = request.json

    if not data or 'token_qr' not in data:
        return jsonify({
            'errors':[{
                'code': '400',
                'message': 'Parametros invalidos',
                'description': 'Falta el token_qr'
            }]
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE token_qr = %s", (data['token_qr'],))
        reserva = cursor.fetchone()

        if reserva is None:
            return jsonify({
                'errors':[{
                    'code': '404',
                    'message': 'QR invalido',
                    'description': 'No se encontro ninguna reserva con ese codigo QR'
                }]
            }), 404

        if reserva['estado_reserva'] == 'confirmada':
            return jsonify({
                'message': 'Esta reserva ya fue confirmada anteriormente',
                'reserva': reserva
            }), 200

        if reserva['estado_reserva'] == 'cancelada':
            return jsonify({
                'errors':[{
                    'code': '409',
                    'message': 'Reserva cancelada',
                    'description': 'Esta reserva fue cancelada y no puede confirmarse'
                }]
            }), 409

        cursor.execute(
            "UPDATE reservas SET estado_reserva = %s WHERE token_qr = %s",
            ('confirmada', data['token_qr'])
        )
        conn.commit()

        enviar_email_cambio_estado(
            nombre=reserva["nombre_cliente"],
            email_cliente=reserva["cliente_email"],
            estado='confirmada',
            fecha=str(reserva["fecha"]),
            hora=str(reserva["hora"])
        )

        return jsonify({
            'message': 'Reserva confirmada con exito',
            'reserva': {
                'nombre_cliente': reserva['nombre_cliente'],
                'fecha': str(reserva['fecha']),
                'hora': str(reserva['hora']),
                'cantidad_personas': reserva['cantidad_personas']
            }
        }), 200

    except Exception as e:
        return jsonify({
            'errors':[{
                'code': '500',
                'message': "Error interno del servidor",
                'description': f'Fallo interno del servidor: {e}'
            }]
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@reservas_bp.route('/reservas/cancelar/<string:token_qr>', methods=['GET'])
def cancelar_por_token(token_qr):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE token_qr = %s", (token_qr,))
        reserva = cursor.fetchone()

        if not reserva:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2>❌ Reserva no encontrada</h2>
                <p>No encontramos ninguna reserva asociada a este link.</p>
            </body>
            </html>
            ''', 404

        if reserva['estado_reserva'] == 'cancelada':
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2>ℹ️ Tu reserva ya estaba cancelada.</h2>
                <p>Si tenés alguna duda escribinos.</p>
            </body>
            </html>
            ''', 200

        cursor.execute(
            "UPDATE reservas SET estado_reserva = %s WHERE token_qr = %s",
            ('cancelada', token_qr)
        )
        conn.commit()

        enviar_email_cambio_estado(
            nombre=reserva["nombre_cliente"],
            email_cliente=reserva["cliente_email"],
            estado='cancelada',
            fecha=str(reserva["fecha"]),
            hora=str(reserva["hora"])
        )

        return '''
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2>✅ Reserva cancelada con éxito</h2>
            <p>Pronto te llegará un mail confirmando la cancelación.</p>
        </body>
        </html>
        ''', 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()