from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, MarcaImpresora

impresoras_bp = Blueprint('impresoras', __name__, url_prefix='/impresoras')

@impresoras_bp.route('/')
def impresoras_index():
    # Renderizar la página principal de impresoras
    return render_template('impresoras.html')

@impresoras_bp.route('/add_marca', methods=['GET', 'POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre de la marca es obligatorio.', 'error')
            return redirect(url_for('impresoras.add_marca'))

        # Verificar si la marca ya existe
        existing_marca = MarcaImpresora.query.filter_by(nombre=nombre).first()
        if existing_marca:
            flash('La marca ya existe.', 'error')
            return redirect(url_for('impresoras.add_marca'))

        # Crear una nueva marca
        nueva_marca = MarcaImpresora(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()

        flash('Marca agregada exitosamente.', 'success')
        return redirect(url_for('impresoras.add_marca'))

    # Renderizar el formulario para agregar una nueva marca
    marcas = MarcaImpresora.query.all()
    return render_template('impresoras_marcas.html', marcas=marcas)