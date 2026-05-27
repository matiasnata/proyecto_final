from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/admin/servicios')
def admin_servicios():
    servicios = [
        {"id_servicio": 1, "nombre_servicio": "Wifi", "descripcion": "gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggInternet gratis", "activo": True},
        {"id_servicio": 2, "nombre_servicio": "Estacionamiento", "descripcion": "Parking disponible", "activo": True},
    ]
    return render_template('admin_servicios.html', servicios=servicios, usuario_autenticado="Juan")

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('base_admin.html', usuario_autenticado="Juan")

@app.route('/admin/menu')
def admin_menu():
    return render_template('admin_menu.html', usuario_autenticado="Juan")

@app.route('/admin/resenas')
def admin_resenas():
    return render_template('admin_resenas.html', usuario_autenticado="Juan")

@app.route('/admin/reservas')
def admin_reservas():
    return render_template('admin_reservas.html', usuario_autenticado="Juan")

@app.route('/admin/estadisticas')
def admin_estadisticas():
    return render_template('admin_estadisticas.html', usuario_autenticado="Juan")

@app.route('/')
def inicio():
    return render_template('index.html', usuario_autenticado="Juan")

@app.route('/admin/servicios/gestionar', methods=['POST'])
def gestionar_servicios():
    return redirect(url_for('admin_servicios'))


if __name__ == '__main__':
    app.run(port=5001, debug=True)

