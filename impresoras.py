from flask import Blueprint, render_template

impresoras_bp = Blueprint('impresoras', __name__, url_prefix='/impresoras')

@impresoras_bp.route('/')
def impresoras_index():
    return render_template('impresoras.html')