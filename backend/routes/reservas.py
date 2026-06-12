from flask import Blueprint, request, jsonify, render_template
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

# ── QR ────────────────────────────────────────────────────────
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

# ── EMAILS ────────────────────────────────────────────────────
def enviar_email_reserva_creada(nombre, email_cliente, fecha, hora, personas, token_qr):
    print(f"Intentando enviar mail a {email_cliente}")
    try:
        qr_bytes = generar_qr_bytes(token_qr)

        msg = Message(
            subject='¡Tu reserva en Flames JB está confirmada!',
            sender=mail.default_sender,
            recipients=[email_cliente]
        )
        msg.html = render_template(
            'emails/reserva_creada.html',
            nombre=nombre,
            fecha=fecha,
            hora=hora,
            personas=personas,
            token_qr=token_qr
        )
        msg.attach(
            filename='qr.png',
            content_type='image/png',
            data=qr_bytes,
            disposition='inline',
            headers={'Content-ID': '<qr_reserva>'}
        )
        mail.send(msg)
        print("Mail enviado con exito")
        return True
    except Exception as e:
        print(f"Error al enviar email: {type(e).__name__}: {e}")
        return False


def enviar_email_cambio_estado(nombre, email_cliente, estado, fecha, hora, id_reserva=None):
    try:
        if estado == 'confirmada':
            asunto = 'Tu reserva en Flames JB fue confirmada'
            html = render_template(
                'emails/reserva_confirmada.html',
                nombre=nombre,
                fecha=fecha,
                hora=hora,
                id_reserva=id_reserva
            )
        elif estado == 'cancelada':
            asunto = 'Tu reserva en Flames JB fue cancelada'
            html = render_template(
                'emails/reserva_cancelada.html',
                nombre=nombre,
                fecha=fecha,
                hora=hora
            )
        elif estado == 'asistio':
            asunto = 'Contanos cómo fue tu experiencia en Flames JB'
            html = render_template(
                'emails/reserva_asistio.html',
                nombre=nombre,
                fecha=fecha,
                id_reserva=id_reserva
            )
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


# ── ENDPOINTS ─────────────────────────────────────────────────
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

        query_busqueda = "SELECT cliente_email FROM reservas WHERE cliente_email = %s AND estado_reserva = 'confirmada'"
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
        guarda_valores = "INSERT INTO reservas(nombre_cliente, cliente_email, cantidad_personas, fecha, hora, token_qr, estado_reserva) VALUES (%s,%s,%s,%s,%s,%s,'confirmada')"
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
            "message": "Reserva creada con exito",
            "token_qr": token_qr
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'errors': [{
                'code': '500',
                'message': "Error interno del servidor",
                'description': str(e)
            }]
        }), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@reservas_bp.route('/reservas/<int:id_reservas>', methods=['PUT'])
def editar_reserva(id_reservas):
    data = request.get_json()
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reservas = %s", (id_reservas,))
        actual = cursor.fetchone()

        if not actual:
            return jsonify({
                'errors': [{'code': '404', 'message': 'Reserva no encontrada'}]
            }), 404

        nuevo_nombre    = data.get('nombre_cliente',    actual['nombre_cliente'])
        nuevas_personas = data.get('cantidad_personas', actual['cantidad_personas'])
        nueva_fecha     = data.get('fecha',             actual['fecha'])
        nueva_hora      = data.get('hora',              actual['hora'])
        nuevo_estado    = data.get('estado_reserva',    actual['estado_reserva'])
        estado_anterior = actual['estado_reserva']

        cursor.execute(
            """UPDATE reservas
               SET nombre_cliente=%s, cantidad_personas=%s, fecha=%s, hora=%s, estado_reserva=%s
               WHERE id_reservas=%s""",
            (nuevo_nombre, nuevas_personas, nueva_fecha, nueva_hora, nuevo_estado, id_reservas)
        )
        conn.commit()

        if nuevo_estado != estado_anterior and nuevo_estado in ('asistio', 'cancelada'):
            enviar_email_cambio_estado(
                nombre=actual["nombre_cliente"],
                email_cliente=actual["cliente_email"],
                estado=nuevo_estado,
                fecha=str(nueva_fecha),
                hora=str(nueva_hora),
                id_reserva=id_reservas
            )

        return jsonify({"message": "La reserva fue modificada con exito"}), 200

    except Exception as e:
        return jsonify({'errors': [{'code': '500', 'message': str(e)}]}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


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
        if cursor: cursor.close()
        if conn: conn.close()


@reservas_bp.route("/reservas/verificar_qr", methods=['POST'])
def verificar_qr():
    data = request.get_json()

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

        if reserva['estado_reserva'] == 'asistio':
            return jsonify({
                'message': 'Este qr ya fue escaneado anteriormente',
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
            ('asistio', data['token_qr'])
        )
        conn.commit()

        enviar_email_cambio_estado(
            nombre=reserva["nombre_cliente"],
            email_cliente=reserva["cliente_email"],
            estado='asistio',
            fecha=str(reserva["fecha"]),
            hora=str(reserva["hora"]),
            id_reserva=reserva["id_reservas"]
        )

        return jsonify({
            'message': 'Asistencia confirmada con exito',
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
        if cursor: cursor.close()
        if conn: conn.close()


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
            return render_template('cancelar/cancelar_no_encontrada.html'), 404

        if reserva['estado_reserva'] == 'cancelada':
            return render_template('cancelar/cancelar_ya_cancelada.html'), 200

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

        return render_template('cancelar/cancelar_exitosa.html'), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


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