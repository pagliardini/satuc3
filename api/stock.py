from flask import Blueprint, jsonify, request
from models import db, Producto, Area, StockUbicacion, MovimientoStock

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
            "producto_nombre": item.producto_nombre,
            "codigo": item.codigo,
            "cantidad": item.cantidad
        } for item in stock_items])

    # POST method
    data = request.get_json()
    producto_id = data.get('producto_id')
    area_id = data.get('area_id')
    cantidad = data.get('cantidad')

    if not all([producto_id, area_id, cantidad]):
        return jsonify({"success": False, "message": "Producto, área y cantidad son requeridos"}), 400

    try:
        producto = Producto.query.get_or_404(producto_id)
        area = Area.query.get_or_404(area_id)
        producto_nombre = producto.nombre_completo
        codigos_creados = []

        ultimo_codigo = db.session.query(db.func.max(StockUbicacion.codigo)).scalar()
        ultimo_codigo = int(ultimo_codigo) if ultimo_codigo else 500

        if producto.inventariable:
            for _ in range(cantidad):
                ultimo_codigo += 1
                stock = StockUbicacion(
                    area_id=area_id,
                    producto_nombre=producto_nombre,
                    codigo=str(ultimo_codigo),
                    cantidad=1
                )
                db.session.add(stock)
                codigos_creados.append(str(ultimo_codigo))
        else:
            stock_existente = StockUbicacion.query.filter_by(
                area_id=area_id,
                producto_nombre=producto_nombre
            ).first()

            if stock_existente:
                stock_existente.cantidad += cantidad
                codigos_creados.append(stock_existente.codigo)
            else:
                nuevo_codigo = str(ultimo_codigo + 1)
                stock = StockUbicacion(
                    area_id=area_id,
                    producto_nombre=producto_nombre,
                    codigo=nuevo_codigo,
                    cantidad=cantidad
                )
                db.session.add(stock)
                codigos_creados.append(nuevo_codigo)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock registrado correctamente",
            "stock": {
                "producto": producto_nombre,
                "area": area.nombre,
                "cantidad": cantidad,
                "codigos": codigos_creados
            }
        }), 201

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
        "producto_nombre": stock.producto_nombre,
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

        if stock_origen.area_id == destino_area_id:
            return jsonify({"success": False, "message": "El área de destino no puede ser la misma que el área de origen"}), 400

        if stock_origen.cantidad < cantidad:
            return jsonify({"success": False, "message": "Cantidad insuficiente para realizar el movimiento"}), 400

        if stock_origen.cantidad == 1 and cantidad == 1:
            stock_origen.area_id = destino_area_id
            stock_destino = stock_origen
        else:
            stock_origen.cantidad -= cantidad
            stock_destino = StockUbicacion.query.filter_by(
                area_id=destino_area_id,
                producto_nombre=stock_origen.producto_nombre
            ).first()

            if not stock_destino:
                nuevo_codigo = int(db.session.query(db.func.max(StockUbicacion.codigo)).scalar()) + 1
                stock_destino = StockUbicacion(
                    area_id=destino_area_id,
                    producto_nombre=stock_origen.producto_nombre,
                    codigo=str(nuevo_codigo),
                    cantidad=cantidad
                )
                db.session.add(stock_destino)
            else:
                stock_destino.cantidad += cantidad

        movimiento = MovimientoStock(
            stock_origen_id=stock_origen.id,
            stock_destino_id=stock_destino.id,
            cantidad=cantidad,
            observacion=observacion
        )
        db.session.add(movimiento)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock movido correctamente",
            "movimiento": {
                "origen": stock_origen.area.nombre,
                "destino": destino_area.nombre,
                "producto": stock_origen.producto_nombre,
                "cantidad": cantidad
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500