from flask import request, jsonify
from database.conexion import get_connection
from mysql.connector import Error

 
def paginar_tabla(nombre_tabla, base_url):
    try:
        limit_arg = request.args.get('_limit', default='5')  
        offset_arg = request.args.get('_offset', default='0') 
        
        if not (limit_arg.isdigit() and offset_arg.isdigit()):
            return jsonify({
                'errors':[{
                    'code': 400,
                    'message': 'Parámetros inválidos',
                    'description': 'Los parámetros _limit y _offset deben ser números enteros.'
                }]
            }), 400
            
        limit = int(limit_arg)
        offset = int(offset_arg)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        
        cursor.execute(f'SELECT COUNT(*) as total FROM {nombre_tabla}')
        total_registros = cursor.fetchone()['total']
        
        query = f'SELECT * FROM {nombre_tabla} LIMIT {limit} OFFSET {offset}'
        cursor.execute(query, (limit, offset))
        resultado = cursor.fetchall()
        
        if not resultado:
            cursor.close()
            conn.close()
            return '', 204
        
        ultimo_offset = max(0, ((total_registros - 1) // limit) * limit)
        prev_offset = max(0, offset - limit) if offset > 0 else 0
        
        links = {
            '_first': {'href': f'{base_url}?_limit={limit}&_offset=0'},
            '_prev': {'href': f'{base_url}?_limit={limit}&_offset={prev_offset}'},
            '_next': {'href': f'{base_url}?_limit={limit}&_offset={offset + limit}'},
            '_last': {'href': f'{base_url}?_limit={limit}&_offset={ultimo_offset}'},
        }
        
        cursor.close()
        conn.close()
        
        
        return jsonify({
            'datos': resultado,
            '_links': links
        }), 200 

    except Exception as e:
        return jsonify({
            'errors': [{
                'code': 500,
                'message': "Error interno del servidor",
                'description': str(e)
            }]
        }), 500