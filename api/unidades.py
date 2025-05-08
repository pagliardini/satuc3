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

@unidades_bp.route('/unidades/<int:unidad_id>', methods=['GET'])
def unidad_por_id(unidad_id):
    unidad = UnidadOrganizativa.query.get_or_404(unidad_id)
    return jsonify({"id": unidad.id, "nombre": unidad.nombre, "sede_id": unidad.sede_id})
