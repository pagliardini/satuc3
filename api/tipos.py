from flask import Blueprint, jsonify, request, current_app
from models import db, TipoProducto, Marca, Modelo

tipos_bp = Blueprint('tipos_api', __name__, url_prefix='/api')

@tipos_bp.route('/tipos', methods=['GET', 'POST'])
def tipos():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"success": False, "message": "El nombre es requerido"}), 400

        try:
            tipo = TipoProducto(nombre=nombre)
            db.session.add(tipo)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Tipo creado correctamente",
                "tipo": {"id": tipo.id, "nombre": tipo.nombre}
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

    # GET method
    tipos = TipoProducto.query.all()
    return jsonify([{"id": t.id, "nombre": t.nombre} for t in tipos])

@tipos_bp.route('/tipos/<int:id>', methods=['PUT'])
def edit_tipo(id):
    tipo = TipoProducto.query.get_or_404(id)
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({"success": False, "message": "El nombre es requerido"}), 400

    try:
        tipo.nombre = nombre
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Tipo actualizado correctamente",
            "tipo": {"id": tipo.id, "nombre": tipo.nombre}
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@tipos_bp.route('/tipos/<int:id>', methods=['DELETE'])
def delete_tipo(id):
    tipo = TipoProducto.query.get_or_404(id)
    try:
        db.session.delete(tipo)
        db.session.commit()
        return jsonify({"success": True, "message": "Tipo eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "No se puede eliminar el tipo porque tiene productos asociados"}), 400
