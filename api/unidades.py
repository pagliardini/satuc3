from flask import Blueprint,request, redirect, url_for, flash, jsonify
from models import db, Sede, UnidadOrganizativa

unidades_bp = Blueprint('unidades_api', __name__, url_prefix='/api')


# ----- UNIDADES -----
@unidades_bp.route('/unidades', methods=['GET'])
def unidades():
    unidades = UnidadOrganizativa.query.all()
    return jsonify([{"id": u.id, "nombre": u.nombre, "sede_id": u.sede_id} for u in unidades])

# Eliminar este endpoint redundante
# @unidades_bp.route('/unidades/<int:sede_id>', methods=['GET'])
# def unidades_por_sede(sede_id):
#     unidades = UnidadOrganizativa.query.filter_by(sede_id=sede_id).all()
#     return jsonify([{"id": u.id, "nombre": u.nombre} for u in unidades])

# Mantener este endpoint para obtener una unidad específica
@unidades_bp.route('/unidades/<int:unidad_id>', methods=['GET'])
def unidad_por_id(unidad_id):
    unidad = UnidadOrganizativa.query.get_or_404(unidad_id)
    return jsonify({"id": unidad.id, "nombre": unidad.nombre, "sede_id": unidad.sede_id})



@unidades_bp.route('/add_unidad', methods=['POST'])
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
