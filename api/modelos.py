from flask import Blueprint, jsonify, request, current_app
from models import db, TipoProducto, Marca, Modelo

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/modelos', methods=['GET', 'POST'])
def modelos():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        marca_id = data.get('marca_id')

        if not nombre or not marca_id:
            return jsonify({
                "success": False, 
                "message": "El nombre y marca_id son requeridos"
            }), 400

        # Verificar si la marca existe
        marca = Marca.query.get(marca_id)
        if not marca:
            return jsonify({
                "success": False, 
                "message": "La marca especificada no existe"
            }), 404

        try:
            modelo = Modelo(
                nombre=nombre,
                marca_id=marca_id
            )
            db.session.add(modelo)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Modelo creado correctamente",
                "modelo": {
                    "id": modelo.id,
                    "nombre": modelo.nombre,
                    "marca_id": modelo.marca_id
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

    # GET method
    modelos = Modelo.query.all()
    return jsonify([{
        "id": m.id,
        "nombre": m.nombre,
        "marca_id": m.marca_id
    } for m in modelos])

@api_bp.route('/modelos/<int:id>', methods=['PUT'])
def edit_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    data = request.get_json()
    nombre = data.get('nombre')
    marca_id = data.get('marca_id')

    if not nombre or not marca_id:
        return jsonify({"success": False, "message": "El nombre y marca_id son requeridos"}), 400

    # Verificar si la marca existe
    if not Marca.query.get(marca_id):
        return jsonify({"success": False, "message": "La marca especificada no existe"}), 404

    try:
        modelo.nombre = nombre
        modelo.marca_id = marca_id
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Modelo actualizado correctamente",
            "modelo": {
                "id": modelo.id,
                "nombre": modelo.nombre,
                "marca_id": modelo.marca_id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/modelos/<int:id>', methods=['DELETE'])
def delete_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    try:
        db.session.delete(modelo)
        db.session.commit()
        return jsonify({"success": True, "message": "Modelo eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "No se puede eliminar el modelo porque tiene productos asociados"}), 400

@api_bp.route('/debug')
def debug():
    return jsonify({"blueprints": list(current_app.blueprints.keys())})