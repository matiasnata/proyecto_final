@app.route('/inicio', methods=['GET'])
def pagina_principal():
    return render_template('index.html')

@app.route('/inicio/reserva', methods=['GET'])
def obtener_reservas():
    try:
        limit_arg = request.args.get ('_limit', default = '10')
        offset_arg = request.arg.get ('_offset', default = '10') 
        if not (limit_arg.isdigit() and offset_arg.isdigit()):
            return jsonify({
                'errors':[{
                    "code": 400,
                    'message': 'Parametros invalidos',
                    'description': 'los parametros _limit y _offset deben ser numeros enteros.'
                }]
            }), 400
        limit = int(limit_arg)
        offset = int(offset_arg)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) as total FROM reservas')
        total_reservas = cursor.fetchone()['total']
        cursor.execute(f'SELECT * FROM reservas LIMIT {limit} OFFSET {offset}')
        resultado = cursor.fetchall()
        if not resultado:
            conn.close()
            return'', 204
        base_url = 'http://127.0.0.1:8080/reservas'
        ultimo_offset = max(0, ((total_reservas -1) //limit)* limit)
        prev_offset = 0
        if offset > 0:
            prev_offset = max(0, offset - limit)
            links ={
                '_first': {'href': f'{base_url}?_limit={limit}&_offset=0'},
                '_prev': {'href': f'{base_url}?_limit={limit}&_offset={prev_offset}'},
                '_next': {'href': f'{base_url}?_limit={limit}&_offset={offset + limit}'},
                '_last': {'href': f'{base_url}?_limit={limit}&_offset={ultimo_offset}'},
            }
            
            cursor.close()
            conn.close()
            return jsonify({
                'Reservas': resultado,
                '_links' : links
            }), 200
    except:
        return jsonify({
            'errors': [{
                'code': 500,
                'message': "Error interno del servidor",
                'description': 'Fallo interno del servidor'
            }]
        }), 500

if __name__ == '__main__':
    app.run(port=8080 bug=True)