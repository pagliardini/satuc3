from flask import Blueprint, jsonify, request, current_app
from models import db, TipoProducto, Marca, Modelo

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/marcas', methods=['GET', 'POST'])
def marcas():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"success": False, "message": "El nombre es requerido"}), 400

        try:    
            marca = Marca(nombre=nombre)
            db.session.add(marca)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Marca creada correctamente",
                "marca": {"id": marca.id, "nombre": marca.nombre}
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

    # GET method
    marcas = Marca.query.all()
    return jsonify([{"id": m.id, "nombre": m.nombre} for m in marcas])

@api_bp.route('/marcas/<int:id>', methods=['PUT'])
def edit_marca(id):
    marca = Marca.query.get_or_404(id)
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({"success": False, "message": "El nombre es requerido"}), 400

    try:
        marca.nombre = nombre
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Marca actualizada correctamente",
            "marca": {"id": marca.id, "nombre": marca.nombre}
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/marcas/<int:id>', methods=['DELETE'])
def delete_marca(id):
    marca = Marca.query.get_or_404(id)
    try:
        db.session.delete(marca)
        db.session.commit()
        return jsonify({"success": True, "message": "Marca eliminada correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "No se puede eliminar la marca porque tiene productos o modelos asociados"}), 400
