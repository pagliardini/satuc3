from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, UnidadOrganizativa, Area

areas_bp = Blueprint('areas_api', __name__, url_prefix='/api')

@areas_bp.route('/areas', methods=['GET', 'POST'])
def areas():
    if request.method == 'GET':
        areas = Area.query.all()
        return jsonify([{
            "id": area.id,
            "nombre": area.nombre,
            "unidad_organizativa_id": area.unidad_organizativa_id,
            "es_deposito": area.es_deposito
        } for area in areas])
    
    # POST method
    data = request.get_json()
    nombre = data.get('nombre')
    unidad_id = data.get('unidad_organizativa_id')

    if not nombre or not unidad_id:
        return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

    if not UnidadOrganizativa.query.get(unidad_id):
        return jsonify({'error': 'Unidad organizativa no válida.'}), 404

    existente = Area.query.filter_by(
        nombre=nombre, 
        unidad_organizativa_id=unidad_id
    ).first()
    
    if existente:
        return jsonify({
            'error': 'Esta área ya existe en la unidad organizativa.'
        }), 409

    nueva_area = Area(
        nombre=nombre, 
        unidad_organizativa_id=unidad_id
    )
    db.session.add(nueva_area)
    db.session.commit()

    return jsonify({
        'mensaje': 'Área agregada exitosamente.',
        'area': {
            'id': nueva_area.id,
            'nombre': nueva_area.nombre,
            'unidad_organizativa_id': nueva_area.unidad_organizativa_id,
            'es_deposito': nueva_area.es_deposito
        }
    }), 201

@areas_bp.route('/areas/<int:area_id>', methods=['GET', 'PUT', 'DELETE'])
def area_operaciones(area_id):
    area = Area.query.get_or_404(area_id)
    
    if request.method == 'GET':
        return jsonify({
            "id": area.id,
            "nombre": area.nombre,
            "unidad_organizativa_id": area.unidad_organizativa_id,
            "es_deposito": area.es_deposito
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        nombre = data.get('nombre')
        unidad_id = data.get('unidad_organizativa_id')

        if not nombre or not unidad_id:
            return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

        if not UnidadOrganizativa.query.get(unidad_id):
            return jsonify({'error': 'Unidad organizativa no válida.'}), 404

        existente = Area.query.filter(
            Area.nombre == nombre,
            Area.unidad_organizativa_id == unidad_id,
            Area.id != area_id
        ).first()
        
        if existente:
            return jsonify({
                'error': 'Ya existe un área con ese nombre en la unidad organizativa especificada.'
            }), 409

        area.nombre = nombre
        area.unidad_organizativa_id = unidad_id
        db.session.commit()

        return jsonify({
            'mensaje': 'Área actualizada exitosamente.',
            'area': {
                'id': area.id,
                'nombre': area.nombre,
                'unidad_organizativa_id': area.unidad_organizativa_id,
                'es_deposito': area.es_deposito
            }
        })

    elif request.method == 'DELETE':
        try:
            db.session.delete(area)
            db.session.commit()
            return jsonify({
                'mensaje': 'Área eliminada exitosamente.',
                'id': area_id
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'No se puede eliminar el área porque tiene dependencias.'
            }), 409

@areas_bp.route('/areas/<int:area_id>/set_deposito', methods=['PUT'])
def set_deposito(area_id):
    try:
        # Desmarcar cualquier área previamente marcada como depósito
        Area.query.update({Area.es_deposito: False})
        
        # Marcar el área seleccionada como depósito
        area = Area.query.get_or_404(area_id)
        area.es_deposito = True
        db.session.commit()

        return jsonify({
            'mensaje': f"El área '{area.nombre}' ha sido marcada como depósito.",
            'area': {
                'id': area.id,
                'nombre': area.nombre,
                'unidad_organizativa_id': area.unidad_organizativa_id,
                'es_deposito': area.es_deposito
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al establecer el área como depósito.'}), 500
