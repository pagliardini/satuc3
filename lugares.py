from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Sede, UnidadOrganizativa, Area

lugares_bp = Blueprint('lugares', __name__, url_prefix='/lugares')

@lugares_bp.route('/', methods=['GET'])
def lugares_index():
    sedes = Sede.query.all()
    unidades = UnidadOrganizativa.query.all()
    areas = Area.query.all()
    return render_template('lugares.html', sedes=sedes, unidades=unidades, areas=areas)

# ----- SEDES -----
@lugares_bp.route('/add_sede', methods=['POST'])
def add_sede():
    data = request.get_json() if request.is_json else request.form
    nombre = data.get('nombre')

    if not nombre:
        msg = 'El nombre de la sede es obligatorio.'
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    if Sede.query.filter_by(nombre=nombre).first():
        msg = 'Esta sede ya existe.'
        if request.is_json:
            return jsonify({'error': msg}), 409
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    nueva_sede = Sede(nombre=nombre)
    db.session.add(nueva_sede)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Sede agregada exitosamente.', 'id': nueva_sede.id}), 201

    flash('Sede agregada exitosamente.', 'success')
    return redirect(url_for('lugares.lugares_index'))

# ----- UNIDADES -----
@lugares_bp.route('/add_unidad', methods=['POST'])
def add_unidad():
    data = request.get_json() if request.is_json else request.form
    nombre = data.get('nombre')
    sede_id = data.get('sede_id')

    if not nombre or not sede_id:
        msg = 'Todos los campos son obligatorios.'
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    if not Sede.query.get(sede_id):
        msg = 'Sede no válida.'
        if request.is_json:
            return jsonify({'error': msg}), 404
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    existente = UnidadOrganizativa.query.filter_by(nombre=nombre, sede_id=sede_id).first()
    if existente:
        msg = 'Esta unidad ya existe en la sede.'
        if request.is_json:
            return jsonify({'error': msg}), 409
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    nueva_unidad = UnidadOrganizativa(nombre=nombre, sede_id=sede_id)
    db.session.add(nueva_unidad)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Unidad organizativa agregada exitosamente.', 'id': nueva_unidad.id}), 201

    flash('Unidad organizativa agregada exitosamente.', 'success')
    return redirect(url_for('lugares.lugares_index'))

# ----- ÁREAS -----
@lugares_bp.route('/add_area', methods=['POST'])
def add_area():
    data = request.get_json() if request.is_json else request.form
    nombre = data.get('nombre')
    unidad_id = data.get('unidad_organizativa_id')

    if not nombre or not unidad_id:
        msg = 'Todos los campos son obligatorios.'
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    if not UnidadOrganizativa.query.get(unidad_id):
        msg = 'Unidad organizativa no válida.'
        if request.is_json:
            return jsonify({'error': msg}), 404
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    existente = Area.query.filter_by(nombre=nombre, unidad_organizativa_id=unidad_id).first()
    if existente:
        msg = 'Esta área ya existe en la unidad organizativa.'
        if request.is_json:
            return jsonify({'error': msg}), 409
        flash(msg, 'error')
        return redirect(url_for('lugares.lugares_index'))

    nueva_area = Area(nombre=nombre, unidad_organizativa_id=unidad_id)
    db.session.add(nueva_area)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Área agregada exitosamente.', 'id': nueva_area.id}), 201

    flash('Área agregada exitosamente.', 'success')
    return redirect(url_for('lugares.lugares_index'))
