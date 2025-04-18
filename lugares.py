from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Sede, Area

lugares_bp = Blueprint('lugares', __name__, url_prefix='/lugares')

# Ruta principal para lugares
@lugares_bp.route('/')
def lugares_index():
    return render_template('lugares_list.html')

# Ruta para listar sedes
@lugares_bp.route('/sedes')
def listar_sedes():
    sedes = Sede.query.all()
    return render_template('sedes_list.html', sedes=sedes)

# Ruta para agregar una nueva sede
@lugares_bp.route('/add_sede', methods=['GET', 'POST'])
def add_sede():
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre de la sede es obligatorio.', 'error')
            return redirect(url_for('lugares.add_sede'))

        # Verificar si la sede ya existe
        sede_existente = Sede.query.filter_by(nombre=nombre).first()
        if sede_existente:
            flash('Esta sede ya existe.', 'error')
            return redirect(url_for('lugares.add_sede'))

        # Crear una nueva sede
        nueva_sede = Sede(nombre=nombre)
        db.session.add(nueva_sede)
        db.session.commit()
        flash('Sede agregada exitosamente.', 'success')
        return redirect(url_for('lugares.listar_sedes'))

    return render_template('add_sede.html')

# Ruta para listar áreas
@lugares_bp.route('/areas')
def listar_areas():
    areas = Area.query.all()
    return render_template('areas_list.html', areas=areas)

# Ruta para agregar una nueva área
@lugares_bp.route('/add_area', methods=['GET', 'POST'])
def add_area():
    sedes = Sede.query.all()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        sede_id = request.form.get('sede_id')

        if not nombre or not sede_id:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('lugares.add_area'))

        # Verificar si el área ya existe en la sede
        area_existente = Area.query.filter_by(nombre=nombre, sede_id=sede_id).first()
        if area_existente:
            flash('Esta área ya existe en la sede seleccionada.', 'error')
            return redirect(url_for('lugares.add_area'))

        # Crear una nueva área
        nueva_area = Area(nombre=nombre, sede_id=sede_id)
        db.session.add(nueva_area)
        db.session.commit()
        flash('Área agregada exitosamente.', 'success')
        return redirect(url_for('lugares.listar_areas'))

    return render_template('add_area.html', sedes=sedes)