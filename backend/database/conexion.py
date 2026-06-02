import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password ='1234', 
            database = 'restaurante',
        )
        return connection 
    except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None