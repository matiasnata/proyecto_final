from flask import Blueprint, render_template, url_for, request, redirect
import requests

reseñas_bp = Blueprint('reseñas', __name__,  url_prefix='/admin/resenas')

@reseñas_bp.route('', methods=['GET'])
def admin_resenas():
    # con el formulario, se le agrega a la url una query param con lo que envio el usuario, el valor se guarda en la variable email_buscSO
    email_ingresado = request.args.get('email_buscado')

    # Definimos la URL nuestro backend
    url_backend = 'http://127.0.0.1:5000/api/reseñas'

    # Armamos la caja que contiene los parametros para enviar al backend
    parametros_para_backend = {}
    
    if email_ingresado:
        # el backend esta programado para buscar el parametro 'email'
        parametros_para_backend['email'] = email_ingresado

    try:
        # con request.get ya automaticmente armamos la url correspondiente  para el bakckend con la query param en caso de que se la hayan pasado, si no se la pasaron simplemente nos da la url limpia
        respuesta = requests.get(url_backend, params=parametros_para_backend)
        
        #convertio la respuesta que nos da el backend en un diccionario de python.
        datos = respuesta.json()
        
        # Extraemos solo la lista de reseñas para mandarla al HTML, ya que nuestro backend devuelve en la variable resultado la lista de reseñas.
        lista_resenas = datos.get('resultado', []) #si no encuentra nada devuelve una lista en blanco

    except Exception as e:
        # Por si te olvidaste de encender el backend o hay un error de conexión
        print(f"Error al conectar con el backend: {e}")
        lista_resenas = [] # Mandamos una lista vacía para que la página no se rompa

    # Pasamos la lista de reseñas al HTML (Jinja2) asi ejeutara el for para estas reseñas obtenidas.
    return render_template(
        'admin_resenas.html', 
        resultado=lista_resenas
    )

@reseñas_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_reseña_frontend(id):
    # 1. Definimos la URL exacta del backend para esa reseña específica
    url_backend = f'http://127.0.0.1:5000/api/reseñas/{id}'
    
    try:
        # 2. ¡El Frontend llama al Backend!
        # En lugar de requests.get(), usamos requests.delete()
        respuesta = requests.delete(url_backend)
        
        
    except Exception as e:
        print(f"Error al intentar enviar el DELETE al backend: {e}")
        
    # 3. Sin importar qué pasó, recargamos la página principal de reseñas
    # Esto hará que se vuelva a hacer el GET y la tabla se muestre sin la reseña eliminada
    return redirect(url_for('reseñas.admin_resenas'))