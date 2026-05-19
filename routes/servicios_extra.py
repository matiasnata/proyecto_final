from flask import Flask, jsonify, blueprints, render_template, Blueprint
from database import db


servicios_extra_bp= Blueprint('servicios_extra', __name__)

@servicios_extra_bp.route("/servicios-extra", methods =['GET'])
def ver_servicios_extra():
    dbs = db.get_connection()
    con = dbs.cursor(dictionary = True)
    query = """
    SELECT *
    FROM servicios_extra as s_e
    WHERE s_e.activo = True
    """
    con.execute(query)
    servicios_extra = con.fetchall()
    con.close()
    dbs.close()
    if not servicios_extra:
        return jsonify ({"Servicios extra":"Por el momento no contamos con ninguno"}), 200
    return jsonify(servicios_extra), 200