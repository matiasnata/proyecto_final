from flask import Blueprint, request, jsonify

reservas_bp = Blueprint('reservas', __name__,url_prefix='/api/reservas')
from database import db



@reservas_bp.route('/disponibilidad', methods=['GET'])
def consultar_disponiblidad_hora():
    fecha = request.args.get('fecha')
    turnos_fijos = ['11:00', '12:30', '14:00', '15:30', '17:00', '20:00', '21:30', '23:00']
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
        conn = db.get_connection()
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
    
    
            
        
        
        
    
    
        
    

    