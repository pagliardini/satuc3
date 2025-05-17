from flask import Blueprint, jsonify, request
from models import db, Producto, Area, StockUbicacion, MovimientoStock
from models import TipoProducto, Marca, Modelo  # Añadimos estos imports
from datetime import datetime  # Importar datetime

stock_bp = Blueprint('stock_api', __name__, url_prefix='/api')

@stock_bp.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'GET':
        stock_items = StockUbicacion.query.all()
        return jsonify([{
            "id": item.id,
            "area": {
                "id": item.area.id,
                "nombre": item.area.nombre
            },
            "producto": {
                "id": item.producto.id,
                "nombre": item.producto.nombre_completo
            },
            "codigo": item.codigo,
            "cantidad": item.cantidad,
            "fecha_imputacion": item.fecha_imputacion.isoformat() if hasattr(item, 'fecha_imputacion') and item.fecha_imputacion else None
        } for item in stock_items])

    # POST method
    data = request.get_json()
    producto_id = data.get('producto_id')
    area_id = data.get('area_id')
    cantidad = data.get('cantidad')
    
    # Nuevos campos para la creación de productos
    crear_producto = data.get('crear_producto', False)
    tipo_id = data.get('tipo_id')
    marca_id = data.get('marca_id')
    modelo_id = data.get('modelo_id')
    descripcion = data.get('descripcion', '')
    inventariable = data.get('inventariable', True)
    activo = data.get('activo', True)

    # Validar campos requeridos básicos
    if not area_id or not cantidad:
        return jsonify({"success": False, "message": "Área y cantidad son requeridos"}), 400

    # Si no se proporciona producto_id, debe indicarse crear_producto=True y enviar los datos
    if not producto_id and not crear_producto:
        return jsonify({"success": False, "message": "Debe proporcionar un producto_id o solicitar la creación de un producto"}), 400

    try:
        # Si se solicita crear un producto nuevo
        if crear_producto:
            errores = []
            # Validaciones para la creación del producto
            if not tipo_id or not TipoProducto.query.get(tipo_id):
                errores.append('Tipo de producto inválido o inexistente.')
            if not marca_id or not Marca.query.get(marca_id):
                errores.append('Marca inválida o inexistente.')
            if not modelo_id or not Modelo.query.get(modelo_id):
                errores.append('Modelo inválido o inexistente.')
                
            if errores:
                return jsonify({"success": False, "errors": errores}), 400
                
            # Crear el nuevo producto
            nuevo_producto = Producto(
                tipo_id=tipo_id,
                marca_id=marca_id,
                modelo_id=modelo_id,
                descripcion=descripcion,
                inventariable=inventariable,
                activo=activo
            )
            db.session.add(nuevo_producto)
            db.session.flush()  # Para obtener el ID sin hacer commit
            
            producto_id = nuevo_producto.id
            producto = nuevo_producto
        else:
            # Usar producto existente
            producto = Producto.query.get_or_404(producto_id)
        
        area = Area.query.get_or_404(area_id)
        codigos_creados = []

        # Obtener el último código utilizado
        ultimo_codigo = db.session.query(db.func.max(StockUbicacion.codigo)).filter(
            StockUbicacion.codigo.isnot(None)
        ).scalar()
        ultimo_codigo = int(ultimo_codigo) if ultimo_codigo else 10000000

        if producto.inventariable:
            # Para productos inventariables, crear un registro individual por cada unidad
            for _ in range(cantidad):
                ultimo_codigo += 1
                stock = StockUbicacion(
                    area_id=area_id,
                    producto_id=producto_id,
                    codigo=str(ultimo_codigo),
                    cantidad=1,
                    fecha_imputacion=datetime.utcnow()  # Agregamos fecha de imputación
                )
                db.session.add(stock)
                codigos_creados.append(str(ultimo_codigo))
        else:
            # Para productos no inventariables, buscar si ya existe un registro y actualizar cantidad
            stock_existente = StockUbicacion.query.filter_by(
                area_id=area_id,
                producto_id=producto_id,
                codigo=None
            ).first()

            if stock_existente:
                stock_existente.cantidad += cantidad
                db.session.add(stock_existente)
            else:
                # Crear nuevo registro para producto no inventariable
                stock = StockUbicacion(
                    area_id=area_id,
                    producto_id=producto_id,
                    codigo=None,
                    cantidad=cantidad,
                    fecha_imputacion=datetime.utcnow()  # Agregamos fecha de imputación
                )
                db.session.add(stock)

        db.session.commit()

        respuesta = {
            "success": True,
            "message": "Stock registrado correctamente",
            "stock": {
                "producto": producto.nombre_completo,
                "area": area.nombre,
                "cantidad": cantidad,
                "codigos": codigos_creados if producto.inventariable else None
            }
        }
        
        # Si creamos un producto, incluir info del producto en la respuesta
        if crear_producto:
            respuesta["producto_creado"] = {
                "id": producto.id,
                "tipo": producto.tipo.nombre,
                "marca": producto.marca.nombre,
                "modelo": producto.modelo.nombre,
                "descripcion": producto.descripcion,
                "inventariable": producto.inventariable
            }
            
        return jsonify(respuesta), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@stock_bp.route('/stock/<int:stock_id>', methods=['GET'])
def get_stock(stock_id):
    stock = StockUbicacion.query.get_or_404(stock_id)
    return jsonify({
        "id": stock.id,
        "area": {
            "id": stock.area.id,
            "nombre": stock.area.nombre
        },
        "producto": {
            "id": stock.producto.id,
            "nombre": stock.producto.nombre_completo,
            "inventariable": stock.producto.inventariable
        },
        "codigo": stock.codigo,
        "cantidad": stock.cantidad
    })

@stock_bp.route('/stock/movimientos', methods=['POST'])
def stock_movement():
    data = request.get_json()
    stock_id = data.get('stock_id')
    destino_area_id = data.get('destino_area_id')
    cantidad = data.get('cantidad')
    observacion = data.get('observacion', '')

    if not all([stock_id, destino_area_id, cantidad]):
        return jsonify({"success": False, "message": "stock_id, destino_area_id y cantidad son requeridos"}), 400

    try:
        stock_origen = StockUbicacion.query.get_or_404(stock_id)
        destino_area = Area.query.get_or_404(destino_area_id)
        producto = stock_origen.producto

        if stock_origen.area_id == destino_area_id:
            return jsonify({"success": False, "message": "El área de destino no puede ser la misma que el área de origen"}), 400

        if stock_origen.cantidad < cantidad:
            return jsonify({"success": False, "message": "Cantidad insuficiente para realizar el movimiento"}), 400

        # Manejo de productos inventariables vs. no inventariables
        if producto.inventariable:
            # Para productos inventariables, solo se permite mover de uno en uno
            if cantidad != 1 or stock_origen.cantidad != 1:
                return jsonify({"success": False, "message": "Los productos inventariables solo pueden moverse de uno en uno"}), 400
            
            # Simplemente actualizar el area_id del stock existente
            stock_origen.area_id = destino_area_id
            stock_destino = stock_origen
        else:
            # Para productos no inventariables, reducir cantidad del origen
            stock_origen.cantidad -= cantidad
            
            # Buscar si existe stock en el destino o crear uno nuevo
            stock_destino = StockUbicacion.query.filter_by(
                area_id=destino_area_id,
                producto_id=producto.id,
                codigo=None
            ).first()

            if not stock_destino:
                # Crear nuevo registro en el destino
                stock_destino = StockUbicacion(
                    area_id=destino_area_id,
                    producto_id=producto.id,
                    codigo=None,
                    cantidad=cantidad
                )
                db.session.add(stock_destino)
                db.session.flush()  # Para obtener el ID
            else:
                # Actualizar cantidad en el destino existente
                stock_destino.cantidad += cantidad

        # Registrar el movimiento
        movimiento = MovimientoStock(
            stock_origen_id=stock_origen.id,
            stock_destino_id=stock_destino.id if stock_destino.id != stock_origen.id else None,
            cantidad=cantidad,
            observacion=observacion
        )
        db.session.add(movimiento)
        
        # Eliminar el registro de origen si la cantidad es cero
        if stock_origen.cantidad == 0 and not producto.inventariable:
            db.session.delete(stock_origen)
            
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock movido correctamente",
            "movimiento": {
                "origen": Area.query.get(stock_origen.area_id).nombre,
                "destino": destino_area.nombre,
                "producto": producto.nombre_completo,
                "cantidad": cantidad
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500