from flask import Blueprint, jsonify, request
from models import db, TipoProducto, Marca, Modelo, Producto

productos_bp = Blueprint('productos_bp', __name__, url_prefix='/api')

@productos_bp.route('/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'GET':
        productos = Producto.query.all()
        return jsonify([{
            "id": producto.id,
            "tipo": producto.tipo.nombre,
            "marca": producto.marca.nombre,
            "modelo": producto.modelo.nombre,
            "descripcion": producto.descripcion,
            "inventariable": producto.inventariable,
            "activo": producto.activo,
            "fecha_creacion": producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
        } for producto in productos])

    # POST method
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

    try:
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

        return jsonify({
            "success": True,
            "message": "Producto creado correctamente",
            "producto": {
                "id": nuevo_producto.id,
                "tipo": nuevo_producto.tipo.nombre,
                "marca": nuevo_producto.marca.nombre,
                "modelo": nuevo_producto.modelo.nombre,
                "descripcion": nuevo_producto.descripcion,
                "inventariable": nuevo_producto.inventariable,
                "activo": nuevo_producto.activo
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@productos_bp.route('/productos/<int:producto_id>', methods=['GET', 'PUT', 'DELETE'])
def producto_operations(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    
    if request.method == 'GET':
        return jsonify({
            "id": producto.id,
            "tipo": producto.tipo.nombre,
            "marca": producto.marca.nombre,
            "modelo": producto.modelo.nombre,
            "descripcion": producto.descripcion,
            "inventariable": producto.inventariable,
            "activo": producto.activo,
            "fecha_creacion": producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        try:
            producto.tipo_id = data.get('tipo_id', producto.tipo_id)
            producto.marca_id = data.get('marca_id', producto.marca_id)
            producto.modelo_id = data.get('modelo_id', producto.modelo_id)
            producto.descripcion = data.get('descripcion', producto.descripcion)
            producto.activo = data.get('activo', producto.activo)
            producto.inventariable = data.get('inventariable', producto.inventariable)
            
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Producto actualizado correctamente",
                "producto": {
                    "id": producto.id,
                    "tipo": producto.tipo.nombre,
                    "marca": producto.marca.nombre,
                    "modelo": producto.modelo.nombre,
                    "descripcion": producto.descripcion,
                    "inventariable": producto.inventariable,
                    "activo": producto.activo
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Producto eliminado correctamente"
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
