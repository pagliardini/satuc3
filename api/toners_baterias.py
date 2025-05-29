from flask import Blueprint, jsonify, request, current_app
from models import db, TipoProducto, Marca, Modelo, Toner, Bateria

tonersbaterias_bp = Blueprint('tonersbaterias_api', __name__, url_prefix='/api')

@tonersbaterias_bp.route('/toners_baterias', methods=['GET'])
def get_toners():
    """Obtiene todos los tóners"""
    toners = Toner.query.all()
    return jsonify([{"id": t.id, "nombre": t.nombre} for t in toners])

@tonersbaterias_bp.route('/baterias', methods=['GET'])
def get_baterias():
    """Obtiene todas las baterías"""
    baterias = Bateria.query.all()
    return jsonify([{"id": b.id, "cantidad": b.cantidad} for b in baterias])

@tonersbaterias_bp.route('/toners_baterias', methods=['POST'])
def create_toner():
    """Crea un nuevo tóner"""
    data = request.get_json()
    nombre = data.get('nombre')
    
    if not nombre:
        return jsonify({"success": False, "message": "El nombre es requerido"}), 400
    
    try:
        # Verificar si ya existe
        if Toner.query.filter_by(nombre=nombre).first():
            return jsonify({"success": False, "message": "Ya existe un tóner con ese nombre"}), 409
        
        nuevo_toner = Toner(nombre=nombre)
        db.session.add(nuevo_toner)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Tóner creado correctamente",
            "id": nuevo_toner.id,
            "toner": {"id": nuevo_toner.id, "nombre": nuevo_toner.nombre}
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@tonersbaterias_bp.route('/baterias', methods=['POST'])
def create_bateria():
    """Crea una nueva batería"""
    data = request.get_json()
    cantidad = data.get('cantidad')
    
    if not cantidad:
        return jsonify({"success": False, "message": "La cantidad es requerida"}), 400
    
    try:
        # Verificar si ya existe
        if Bateria.query.filter_by(cantidad=cantidad).first():
            return jsonify({"success": False, "message": "Ya existe una batería con esa cantidad"}), 409
        
        nueva_bateria = Bateria(cantidad=cantidad)
        db.session.add(nueva_bateria)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Batería creada correctamente",
            "id": nueva_bateria.id,
            "bateria": {"id": nueva_bateria.id, "cantidad": nueva_bateria.cantidad}
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500