from datetime import datetime
from flask import Blueprint, render_template, url_for, request, redirect
import requests

reseñas_bp = Blueprint('reseñas', __name__,)

@reseñas_bp.route('/admin/resenas', methods=['GET'])
def admin_resenas():
    # con el formulario, se le agrega a la url una query param con lo que envio el usuario, el valor se guarda en la variable email_buscSO
    email_ingresado = request.args.get('email_buscado')
    limit = request.args.get('_limit', 5)   # 10 por defecto si no viene ninguno
    offset = request.args.get('_offset', 0)  # 0 por defecto para la primera página

    # Definimos la URL nuestro backend
    url_backend = 'http://127.0.0.1:5001/reseñas'

    # Armamos la caja que contiene los parametros para enviar al backend
    parametros_para_backend = {
        '_limit': limit,
        '_offset': offset
    }
    
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
        links = datos.get('links', {}) #si no encuentra nada devuelve un diccionario vacio
        
        url_frontend_base = url_for('reseñas.admin_resenas')
        
        def corregir_link(link_backend):
            if link_backend and 'href' in link_backend:
                # Reemplazamos el dominio del backend por el del frontend
                link_backend['href'] = link_backend['href'].replace('http://127.0.0.1:5001/reseñas', url_frontend_base)
                # Reemplazamos 'email=' por 'email_buscado=' para mantener el filtro en el HTML
                link_backend['href'] = link_backend['href'].replace('email=', 'email_buscado=')
            return link_backend
        
        link_prev = corregir_link(links.get('prev', {}))
        link_next = corregir_link(links.get('next', {}))
        link_first = corregir_link(links.get('first', {}))
        link_last = corregir_link(links.get('last', {}))


    except Exception as e:
        # Por si te olvidaste de encender el backend o hay un error de conexión
        print(f"Error al conectar con el backend: {e}")
        lista_resenas = [] # Mandamos una lista vacía para que la página no se rompa
        link_prev = link_next = link_first = link_last = {}

    # Pasamos la lista de reseñas al HTML (Jinja2) asi ejeutara el for para estas reseñas obtenidas.
    return render_template(
        'admin_resenas.html', 
        resultado=lista_resenas,
        link_prev=link_prev,
        link_next=link_next,
        link_first=link_first,
        link_last=link_last,
        usuario_autenticado="Juan",
    )

@reseñas_bp.route('/admin/resenas/eliminar/<int:id>', methods=['POST'])
def eliminar_reseña_frontend(id):
    # 1. Definimos la URL exacta del backend para esa reseña específica
    url_backend = f'http://127.0.0.1:5001/reseñas/{id}'
    
    try:
        # 2. ¡El Frontend llama al Backend!
        # En lugar de requests.get(), usamos requests.delete()
        respuesta = requests.delete(url_backend)
        
        
    except Exception as e:
        print(f"Error al intentar enviar el DELETE al backend: {e}")
        
    # 3. Sin importar qué pasó, recargamos la página principal de reseñas
    # Esto hará que se vuelva a hacer el GET y la tabla se muestre sin la reseña eliminada
    return redirect(url_for('reseñas.admin_resenas'))

@reseñas_bp.route('/admin/resenas/estadisticas', methods=['GET'])
def estadisticas_reseñas():
    anio_actual = datetime.now().year
    
    # 1. Capturamos el año (si no viene en la URL, usamos el actual)
    anio_str = request.args.get('anio')
    anio_buscar = int(anio_str) if anio_str else anio_actual
    
    # NUEVO: Generamos la lista de años (desde el actual hasta 2024, de reversa)
    anios_disponibles = list(range(anio_actual, 2023, -1)) 
    
    url_grafico = 'http://127.0.0.1:5001/reseñas/grafico-resenas'
    url_promedio = 'http://127.0.0.1:5001/reseñas/promedio'
    
    try:
        respuesta_grafico = requests.get(url_grafico, params={'anio': anio_buscar})
        datos_grafico = respuesta_grafico.json()
    
        meses_grafico = datos_grafico.get('meses', [])
        promedios_grafico = datos_grafico.get('promedios', [])
        
    except Exception as e:
        # Por si te olvidaste de encender el backend o hay un error de conexión
        print(f"Error al conectar con el backend: {e}")
        meses_grafico = []
        promedios_grafico = []
    
    try:
        respuesta_promedio = requests.get(url_promedio, params={'anio': anio_buscar})
        data = respuesta_promedio.json()
        promedio_general = data.get('promedio_general', 0)
        total_reseñas = data.get('total_reseñas', 0)
        
    except Exception as e:
        print(f"Error al conectar con el backend para el promedio: {e}")
        promedio_general = 0
        total_reseñas = 0
              
    return render_template(
        'admin_reseñas_estadisticas.html',
        anio_seleccionado=anio_buscar,
        anios_disponibles=anios_disponibles, # PASAMOS LA LISTA AL HTML
        meses_grafico=meses_grafico,
        promedios_grafico=promedios_grafico,
        promedio_general=promedio_general,
        total_reseñas=total_reseñas,
        usuario_autenticado="Juan"
    )
    
@reseñas_bp.route('/crear/reseña/<int:id_reserva>', methods=['GET'])
def formulario_resena(id_reserva):
    return render_template('crear_reseña.html', id_reserva=id_reserva)

@reseñas_bp.route('/resena', methods=['POST'])
def enviar_resena():
    data = {
        'id_reserva': request.form.get('id_reserva'),
        'puntaje': int(request.form.get('puntaje')),
        'comentario': request.form.get('comentario')
    }
    
    id_reserva = request.form.get('id_reserva')
    
    try:
        response = requests.post('http://127.0.0.1:5001/reseñas', json=data)
        if response.status_code == 201:
            return render_template('crear_reseña.html', id_reserva=id_reserva, exito='¡Gracias por tu reseña!')
        else:
            return render_template('crear_reseña.html', id_reserva=id_reserva, error='Hubo un error,quizas ya hiciste una reseña, si no es asi intenta de nuevo')
    except Exception as e:
        return render_template('crear_reseña.html', id_reserva=id_reserva, error='No se pudo conectar con el servidor, intenta mas tarde.')