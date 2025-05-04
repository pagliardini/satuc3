from flask import Blueprint, jsonify, request, current_app
from models import db, TipoProducto, Marca, Modelo, Producto

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    productos_json = [
        {
            "id": producto.id,
            "tipo": producto.tipo.nombre,
            "marca": producto.marca.nombre,
            "modelo": producto.modelo.nombre,
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

@api_bp.route('/tipos', methods=['GET', 'POST'])
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

@api_bp.route('/tipos/<int:id>', methods=['PUT'])
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

@api_bp.route('/tipos/<int:id>', methods=['DELETE'])
def delete_tipo(id):
    tipo = TipoProducto.query.get_or_404(id)
    try:
        db.session.delete(tipo)
        db.session.commit()
        return jsonify({"success": True, "message": "Tipo eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "No se puede eliminar el tipo porque tiene productos asociados"}), 400

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