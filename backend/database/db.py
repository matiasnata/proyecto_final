import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = '',
            password ='', 
            database = '',
        )
        return connection 
    except mysql.connector.Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None