from flask import Blueprint, request, jsonify, render_template, redirect, url_for

return redirect(url_for('inicio.inicio'))

reservas_bp = Blueprint("reservas", __name__)