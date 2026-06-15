#!/bin/bash

 
echo " Creando entorno virtual "
python3 -m venv venv

 
echo " Activando entorno virtual "
source venv/bin/activate

 
echo " Instalando librerías del backend "
pip install -r backend/requirements.txt

 
echo " Instalando librerías del frontend "
pip install -r frontend/requirements.txt
 
 

echo "Entorno virutal instalado con sus librerias"
