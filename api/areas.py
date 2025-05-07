from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, UnidadOrganizativa, Area

areas_bp = Blueprint('areas_api', __name__, url_prefix='/api')


# ----- ÁREAS -----
@areas_bp.route('/add_area', methods=['POST'])
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

@areas_bp.route('/set_deposito/<int:area_id>', methods=['POST'])
def set_deposito(area_id):
    # Desmarcar cualquier área previamente marcada como depósito
    Area.query.update({Area.es_deposito: False})
    db.session.commit()

    # Marcar el área seleccionada como depósito
    area = Area.query.get_or_404(area_id)
    area.es_deposito = True
    db.session.commit()

    flash(f"El área '{area.nombre}' ha sido marcada como depósito.", 'success')
    return redirect(url_for('lugares.lugares_index'))
