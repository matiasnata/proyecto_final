import mysql.connector
import os

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '1234'),
            database=os.getenv('DB_NAME', 'restaurante'),
            port=int(os.getenv('DB_PORT', '3306'))
        )
        return connection
    except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None