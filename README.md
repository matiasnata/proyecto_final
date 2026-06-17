Flames JB - API REST de Restaurante

Requisitos

- Python 3.10+
- MySQL 8.0+
- Git

---

Instalación

1. Clonar el repositorio

bash
git clone <url-del-repo>
cd proyecto_final


2. Instalar MySQL
bash
sudo apt update
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo mysql_secure_installation


Durante `mysql_secure_installation` seteás la contraseña de root. Recomendamos usar `1234` para desarrollo local.

3. Copiar los datos de .env_example y crear .env

cd backend/
cat .env_example

Copias los datos.

touch .env
nano .env

Pegas los datos de ejemplo e ingresas los reales.


4. Ejecutar setup
Desde la carpeta raiz:
bash setup_entorno_virtual.sh

Seguis los pasos para la creacion del entorno y user del administador.

---

Levantar el proyecto

Abrís **dos terminales**:

Terminal 1 - Backend:
source venv/bin/activate
cd backend/
python3 app.py


Terminal 2 - Frontend:
source venv/bin/activate
cd frontend/
python3 app.py


El frontend estará disponible en: `http://localhost:5000`  
El backend estará disponible en: `http://localhost:5001`  
El panel de administración en: `http://localhost:5000/admin`

---

Tecnologías utilizadas

- Backend: Flask, MySQL, Flask-Mail, bcrypt, qrcode
- Frontend: Flask, Jinja2, HTML, CSS, JavaScript
- Base de datos: MySQL
