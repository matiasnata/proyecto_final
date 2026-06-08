from database.conexion import get_connection
import bcrypt

nombre = input("Nombre del admin: ")
email = input("Email: ")
password = input("Contraseña: ")

hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute(
        "INSERT INTO administradores (nombre, email, password_hash) VALUES (%s, %s, %s)",
        (nombre, email, hash)
    )
    conn.commit()
    print(f"Admin '{nombre}' creado con éxito.")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()