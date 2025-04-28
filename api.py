from flask import Blueprint, jsonify, request, current_app
from models import db, TipoProducto, Marca, Modelo, Producto

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    productos_json = [
        {
            "id": producto.id,
            "tipo_id": producto.tipo_id,
            "marca_id": producto.marca_id,
            "modelo_id": producto.modelo_id,
            "descripcion": producto.descripcion,
            "inventariable": producto.inventariable,
            "activo": producto.activo,
            "fecha_creacion": producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
        }
        for producto in productos
    ]
    return jsonify(productos_json)

@api_bp.route('/debug')
def debug():
    return jsonify({"blueprints": list(current_app.blueprints.keys())})