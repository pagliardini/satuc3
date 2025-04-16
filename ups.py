from flask import Blueprint, render_template

ups_bp = Blueprint('ups', __name__, url_prefix='/ups')

@ups_bp.route('/')
def ups_index():
    return render_template('ups.html')