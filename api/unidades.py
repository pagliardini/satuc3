from flask import Blueprint, request, jsonify
from models import db, Sede, UnidadOrganizativa

unidades_bp = Blueprint('unidades_api', __name__, url_prefix='/api')

@unidades_bp.route('/unidades', methods=['GET', 'POST'])
def unidades():
    if request.method == 'GET':
        unidades = UnidadOrganizativa.query.all()
        return jsonify([{"id": u.id, "nombre": u.nombre, "sede_id": u.sede_id} for u in unidades])
    
    # POST method
    data = request.get_json()
    nombre = data.get('nombre')
    sede_id = data.get('sede_id')

    if not nombre or not sede_id:
        return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

    if not Sede.query.get(sede_id):
        return jsonify({'error': 'Sede no válida.'}), 404

    existente = UnidadOrganizativa.query.filter_by(nombre=nombre, sede_id=sede_id).first()
    if existente:
        return jsonify({'error': 'Esta unidad ya existe en la sede.'}), 409

    nueva_unidad = UnidadOrganizativa(nombre=nombre, sede_id=sede_id)
    db.session.add(nueva_unidad)
    db.session.commit()

    return jsonify({
        'mensaje': 'Unidad organizativa agregada exitosamente.',
        'unidad': {
            'id': nueva_unidad.id,
            'nombre': nueva_unidad.nombre,
            'sede_id': nueva_unidad.sede_id
        }
    }), 201

@unidades_bp.route('/unidades/<int:unidad_id>', methods=['GET', 'PUT', 'DELETE'])
def unidad_operaciones(unidad_id):
    unidad = UnidadOrganizativa.query.get_or_404(unidad_id)
    
    if request.method == 'GET':
        return jsonify({
            "id": unidad.id, 
            "nombre": unidad.nombre, 
            "sede_id": unidad.sede_id
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        nombre = data.get('nombre')
        sede_id = data.get('sede_id')

        if not nombre or not sede_id:
            return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

        # Verificar si existe la sede
        if not Sede.query.get(sede_id):
            return jsonify({'error': 'Sede no válida.'}), 404

        # Verificar si ya existe otra unidad con el mismo nombre en la misma sede
        existente = UnidadOrganizativa.query.filter(
            UnidadOrganizativa.nombre == nombre,
            UnidadOrganizativa.sede_id == sede_id,
            UnidadOrganizativa.id != unidad_id
        ).first()
        
        if existente:
            return jsonify({'error': 'Ya existe una unidad con ese nombre en la sede especificada.'}), 409

        # Actualizar la unidad
        unidad.nombre = nombre
        unidad.sede_id = sede_id
        db.session.commit()

        return jsonify({
            'mensaje': 'Unidad organizativa actualizada exitosamente.',
            'unidad': {
                'id': unidad.id,
                'nombre': unidad.nombre,
                'sede_id': unidad.sede_id
            }
        })

    elif request.method == 'DELETE':
        try:
            db.session.delete(unidad)
            db.session.commit()
            return jsonify({
                'mensaje': 'Unidad organizativa eliminada exitosamente.',
                'id': unidad_id
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'No se puede eliminar la unidad organizativa porque tiene dependencias.'
            }), 409
