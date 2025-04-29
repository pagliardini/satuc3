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

@api_bp.route('/productos/add_producto', methods=['POST'])
def add_producto_api():
    data = request.get_json()

    tipo_id = data.get('tipo_id')
    marca_id = data.get('marca_id')
    modelo_id = data.get('modelo_id')
    descripcion = data.get('descripcion', '')
    inventariable = data.get('inventariable', False)
    activo = data.get('activo', False)

    errores = []

    # Validaciones
    if not tipo_id or not TipoProducto.query.get(tipo_id):
        errores.append('Tipo de producto inválido o inexistente.')

    if not marca_id or not Marca.query.get(marca_id):
        errores.append('Marca inválida o inexistente.')

    if not modelo_id or not Modelo.query.get(modelo_id):
        errores.append('Modelo inválido o inexistente.')

    if errores:
        return jsonify({"success": False, "errors": errores}), 400

    # Crear producto
    nuevo_producto = Producto(
        tipo_id=tipo_id,
        marca_id=marca_id,
        modelo_id=modelo_id,
        descripcion=descripcion,
        inventariable=inventariable,
        activo=activo
    )
    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify({"success": True, "message": "Producto creado correctamente.", "producto_id": nuevo_producto.id}), 201

@api_bp.route('/productos/<int:id>', methods=['PUT'])
def edit_producto_api(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()

    producto.tipo_id = data.get('tipo_id', producto.tipo_id)
    producto.marca_id = data.get('marca_id', producto.marca_id)
    producto.modelo_id = data.get('modelo_id', producto.modelo_id)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.activo = data.get('activo', producto.activo)
    producto.inventariable = data.get('inventariable', producto.inventariable)

    db.session.commit()

    return jsonify({"success": True, "message": "Producto actualizado correctamente."})

@api_bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto_api(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    return jsonify({"success": True, "message": "Producto eliminado correctamente."})

@api_bp.route('/debug')
def debug():
    return jsonify({"blueprints": list(current_app.blueprints.keys())})