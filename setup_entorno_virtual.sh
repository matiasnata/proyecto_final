#!/bin/bash

echo " Setup completo de proyecto_final"

read -p "¿Ya creaste el .env? Presioná ENTER para continuar..."

echo ""
read -sp "Ingresá la contraseña de root de MySQL: " MYSQL_ROOT_PASSWORD
echo ""

echo "Creando base de datos y tablas..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" < backend/database/database.sql

if [ $? -eq 0 ]; then
    echo "Base de datos y tablas creadas correctamente."
else
    echo "ERROR: no se pudo crear la base de datos."
    exit 1
fi

echo ""
echo " Creando entorno virtual "
python3 -m venv venv

echo "Activando entorno virtual"
source venv/bin/activate

echo ""
echo "Instalando librerías del backend..."
pip install -r backend/requirements.txt

echo "Instalando librerías del frontend..."
pip install -r frontend/requirements.txt

cd backend
source venv/bin/activate
python crear_admin.py
echo ""
echo " Setup terminado con éxito"
echo ""
echo "Ahora levanta ambos servidores"