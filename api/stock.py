from flask import Blueprint, jsonify, request
from models import db, Area, StockUbicacion, MovimientoStock
from models import TipoProducto, Marca, Modelo  # Ya no necesitamos Producto
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
            "tipo": {
                "id": item.tipo.id,
                "nombre": item.tipo.nombre
            },
            "marca": {
                "id": item.marca.id,
                "nombre": item.marca.nombre
            },
            "modelo": {
                "id": item.modelo.id,
                "nombre": item.modelo.nombre
            },
            "descripcion": item.descripcion,
            "inventariable": item.inventariable,
            "codigo": item.codigo,
            "cantidad": item.cantidad,
            "nombre_completo": item.nombre_completo,
            "fecha_imputacion": item.fecha_imputacion.isoformat() if item.fecha_imputacion else None
        } for item in stock_items])

    # POST method
    data = request.get_json()
    area_id = data.get('area_id')
    tipo_id = data.get('tipo_id')
    marca_id = data.get('marca_id')
    modelo_id = data.get('modelo_id')
    descripcion = data.get('descripcion', '')
    inventariable = data.get('inventariable', True)
    cantidad = data.get('cantidad')

    # Validar campos requeridos básicos
    if not all([area_id, tipo_id, marca_id, modelo_id, cantidad]):
        return jsonify({"success": False, "message": "Área, tipo, marca, modelo y cantidad son requeridos"}), 400

    try:
        # Validar que los modelos existan
        errores = []
        if not tipo_id or not TipoProducto.query.get(tipo_id):
            errores.append('Tipo de producto inválido o inexistente.')
        if not marca_id or not Marca.query.get(marca_id):
            errores.append('Marca inválida o inexistente.')
        if not modelo_id or not Modelo.query.get(modelo_id):
            errores.append('Modelo inválido o inexistente.')
        if not area_id or not Area.query.get(area_id):
            errores.append('Área inválida o inexistente.')
            
        if errores:
            return jsonify({"success": False, "errors": errores}), 400
            
        area = Area.query.get(area_id)
        tipo = TipoProducto.query.get(tipo_id)
        marca = Marca.query.get(marca_id)
        modelo = Modelo.query.get(modelo_id)
        
        codigos_creados = []

        # Obtener el último código utilizado
        ultimo_codigo = db.session.query(db.func.max(StockUbicacion.codigo)).filter(
            StockUbicacion.codigo.isnot(None)
        ).scalar()
        ultimo_codigo = int(ultimo_codigo) if ultimo_codigo else 10000000

        if inventariable:
            # Para items inventariables, crear un registro individual por cada unidad
            for _ in range(cantidad):
                ultimo_codigo += 1
                stock = StockUbicacion(
                    area_id=area_id,
                    tipo_id=tipo_id,
                    marca_id=marca_id,
                    modelo_id=modelo_id,
                    descripcion=descripcion,
                    inventariable=inventariable,
                    codigo=str(ultimo_codigo),
                    cantidad=1,
                    fecha_imputacion=datetime.utcnow()
                )
                db.session.add(stock)
                codigos_creados.append(str(ultimo_codigo))
        else:
            # Para items no inventariables, buscar si ya existe un registro y actualizar cantidad
            stock_existente = StockUbicacion.query.filter_by(
                area_id=area_id,
                tipo_id=tipo_id,
                marca_id=marca_id,
                modelo_id=modelo_id,
                inventariable=False,
                codigo=None
            ).first()

            if stock_existente:
                stock_existente.cantidad += cantidad
                stock = stock_existente
                db.session.add(stock)
            else:
                # Crear nuevo registro para item no inventariable
                stock = StockUbicacion(
                    area_id=area_id,
                    tipo_id=tipo_id,
                    marca_id=marca_id,
                    modelo_id=modelo_id,
                    descripcion=descripcion,
                    inventariable=inventariable,
                    codigo=None,
                    cantidad=cantidad,
                    fecha_imputacion=datetime.utcnow()
                )
                db.session.add(stock)

        db.session.commit()

        nombre_completo = f"{tipo.nombre} {marca.nombre} {modelo.nombre}"
        
        respuesta = {
            "success": True,
            "message": "Stock registrado correctamente",
            "stock": {
                "nombre": nombre_completo,
                "area": area.nombre,
                "cantidad": cantidad,
                "codigos": codigos_creados if inventariable else None
            }
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
        "tipo": {
            "id": stock.tipo.id,
            "nombre": stock.tipo.nombre
        },
        "marca": {
            "id": stock.marca.id,
            "nombre": stock.marca.nombre
        },
        "modelo": {
            "id": stock.modelo.id,
            "nombre": stock.modelo.nombre
        },
        "descripcion": stock.descripcion,
        "inventariable": stock.inventariable,
        "codigo": stock.codigo,
        "cantidad": stock.cantidad,
        "nombre_completo": stock.nombre_completo,
        "fecha_imputacion": stock.fecha_imputacion.isoformat() if stock.fecha_imputacion else None,
        "ultimo_movimiento": stock.ultimo_movimiento.isoformat() if stock.ultimo_movimiento else None
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

        # Manejo de ítems inventariables vs. no inventariables
        if stock_origen.inventariable:
            # Para ítems inventariables, solo se permite mover de uno en uno
            if cantidad != 1 or stock_origen.cantidad != 1:
                return jsonify({"success": False, "message": "Los ítems inventariables solo pueden moverse de uno en uno"}), 400
            
            # Simplemente actualizar el area_id del stock existente
            stock_origen.area_id = destino_area_id
            stock_destino = stock_origen
        else:
            # Para ítems no inventariables, reducir cantidad del origen
            stock_origen.cantidad -= cantidad
            
            # Buscar si existe stock en el destino o crear uno nuevo
            stock_destino = StockUbicacion.query.filter_by(
                area_id=destino_area_id,
                tipo_id=stock_origen.tipo_id,
                marca_id=stock_origen.marca_id,
                modelo_id=stock_origen.modelo_id,
                inventariable=False,
                codigo=None
            ).first()

            if not stock_destino:
                # Crear nuevo registro en el destino
                stock_destino = StockUbicacion(
                    area_id=destino_area_id,
                    tipo_id=stock_origen.tipo_id,
                    marca_id=stock_origen.marca_id,
                    modelo_id=stock_origen.modelo_id,
                    descripcion=stock_origen.descripcion,
                    inventariable=stock_origen.inventariable,
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
        if stock_origen.cantidad == 0 and not stock_origen.inventariable:
            db.session.delete(stock_origen)
            
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Stock movido correctamente",
            "movimiento": {
                "origen": Area.query.get(stock_origen.area_id).nombre,
                "destino": destino_area.nombre,
                "item": stock_origen.nombre_completo,
                "cantidad": cantidad
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500