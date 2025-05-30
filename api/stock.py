from flask import Blueprint, jsonify, request
from models import db, Area, StockUbicacion, MovimientoStock
from models import TipoProducto, Marca, Modelo, Insumo, Toner, Bateria
from datetime import datetime
import uuid

stock_bp = Blueprint('stock_api', __name__, url_prefix='/api')

@stock_bp.route('/stock', methods=['GET'])
def get_stock():
    """Obtiene todo el stock con información del insumo"""
    stock_items = StockUbicacion.query.all()
    return jsonify([{
        "id": item.id,
        "insumo": {
            "id": item.insumo.id,
            "nombre_completo": item.insumo.nombre_completo,
            "tipo": item.insumo.tipo.nombre if item.insumo.tipo else None,
            "marca": {
                "id": item.insumo.marca.id if item.insumo.marca else None,
                "nombre": item.insumo.marca.nombre if item.insumo.marca else None
            },
            "modelo": {
                "id": item.insumo.modelo.id if item.insumo.modelo else None,
                "nombre": item.insumo.modelo.nombre if item.insumo.modelo else None
            },
            "descripcion": item.insumo.descripcion,
            "inventariable": item.insumo.inventariable,
            "toner": item.insumo.toner.nombre if item.insumo.toner else None,
            "bateria": item.insumo.bateria.cantidad if item.insumo.bateria else None,
            "url_imagen": item.insumo.url_imagen
        },
        "area": {
            "id": item.area.id,
            "nombre": item.area.nombre,
            "es_deposito": item.area.es_deposito
        },
        "cantidad": item.cantidad,
        "codigo": item.codigo,
        "estado": item.estado,
        "fecha_imputacion": item.fecha_imputacion.isoformat() if item.fecha_imputacion else None,
        "ultimo_movimiento": item.ultimo_movimiento.isoformat() if item.ultimo_movimiento else None
    } for item in stock_items])

@stock_bp.route('/stock/insumos', methods=['GET', 'POST'])
def insumos():
    if request.method == 'GET':
        insumos = Insumo.query.filter_by(activo=True).all()
        return jsonify([{
            "id": insumo.id,
            "nombre_completo": insumo.nombre_completo,
            "tipo": {"id": insumo.tipo.id, "nombre": insumo.tipo.nombre},
            "marca": {"id": insumo.marca.id, "nombre": insumo.marca.nombre},
            "modelo": {"id": insumo.modelo.id, "nombre": insumo.modelo.nombre},
            "descripcion": insumo.descripcion,
            "inventariable": insumo.inventariable,
            "toner": {"id": insumo.toner.id, "nombre": insumo.toner.nombre} if insumo.toner else None,
            "bateria": {"id": insumo.bateria.id, "cantidad": insumo.bateria.cantidad} if insumo.bateria else None,
            "url_imagen": insumo.url_imagen,
            "fecha_creacion": insumo.fecha_creacion.isoformat()
        } for insumo in insumos])
    
    # POST - Crear nuevo insumo
    data = request.get_json()
    tipo_id = data.get('tipo_id')
    marca_id = data.get('marca_id')
    modelo_id = data.get('modelo_id')
    descripcion = data.get('descripcion', '')
    inventariable = data.get('inventariable', True)
    toner_id = data.get('toner_id')
    bateria_id = data.get('bateria_id')
    url_imagen = data.get('url_imagen')

    if not all([tipo_id, marca_id, modelo_id]):
        return jsonify({"success": False, "message": "Tipo, marca y modelo son requeridos"}), 400

    try:
        # Validar que los modelos existan
        if not TipoProducto.query.get(tipo_id):
            return jsonify({"success": False, "message": "Tipo de producto no válido"}), 400
        if not Marca.query.get(marca_id):
            return jsonify({"success": False, "message": "Marca no válida"}), 400
        if not Modelo.query.get(modelo_id):
            return jsonify({"success": False, "message": "Modelo no válido"}), 400
        if toner_id and not Toner.query.get(toner_id):
            return jsonify({"success": False, "message": "Tóner no válido"}), 400
        if bateria_id and not Bateria.query.get(bateria_id):
            return jsonify({"success": False, "message": "Batería no válida"}), 400

        # Verificar si ya existe un insumo igual
        insumo_existente = Insumo.query.filter_by(
            tipo_id=tipo_id,
            marca_id=marca_id,
            modelo_id=modelo_id,
            descripcion=descripcion,
            toner_id=toner_id,
            bateria_id=bateria_id,
            activo=True
        ).first()

        if insumo_existente:
            return jsonify({
                "success": False, 
                "message": "Ya existe un insumo con estas características",
                "insumo_existente": {
                    "id": insumo_existente.id,
                    "nombre_completo": insumo_existente.nombre_completo
                }
            }), 409

        # Crear nuevo insumo
        nuevo_insumo = Insumo(
            tipo_id=tipo_id,
            marca_id=marca_id,
            modelo_id=modelo_id,
            descripcion=descripcion,
            inventariable=inventariable,
            toner_id=toner_id if toner_id else None,
            bateria_id=bateria_id if bateria_id else None,
            url_imagen=url_imagen
        )
        
        db.session.add(nuevo_insumo)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Insumo creado correctamente",
            "insumo": {
                "id": nuevo_insumo.id,
                "nombre_completo": nuevo_insumo.nombre_completo
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@stock_bp.route('/stock/imputar', methods=['POST'])
def imputar_stock():
    """Imputa un insumo existente a un área"""
    data = request.get_json()
    insumo_id = data.get('insumo_id')
    area_id = data.get('area_id')
    cantidad = data.get('cantidad', 1)
    responsable = data.get('responsable', '')
    observacion = data.get('observacion', '')

    if not all([insumo_id, area_id, cantidad]):
        return jsonify({"success": False, "message": "Insumo, área y cantidad son requeridos"}), 400

    try:
        insumo = Insumo.query.get_or_404(insumo_id)
        area = Area.query.get_or_404(area_id)

        if not insumo.activo:
            return jsonify({"success": False, "message": "El insumo no está activo"}), 400

        codigos_creados = []

        if insumo.inventariable:
            # Para insumos inventariables, crear un registro por cada unidad con código único
            for _ in range(cantidad):
                # Generar código único
                codigo = f"{insumo.tipo.nombre[:3]}-{insumo.marca.nombre[:3]}-{str(uuid.uuid4())[:8]}".upper()
                
                stock = StockUbicacion(
                    insumo_id=insumo_id,
                    area_id=area_id,
                    cantidad=1,
                    codigo=codigo,
                    fecha_imputacion=datetime.utcnow()
                )
                db.session.add(stock)
                codigos_creados.append(codigo)
        else:
            # Para insumos no inventariables, buscar si ya existe y actualizar cantidad
            stock_existente = StockUbicacion.query.filter_by(
                insumo_id=insumo_id,
                area_id=area_id,
                codigo=None  # Los no inventariables no tienen código
            ).first()

            if stock_existente:
                stock_existente.cantidad += cantidad
                stock_existente.ultimo_movimiento = datetime.utcnow()
            else:
                stock = StockUbicacion(
                    insumo_id=insumo_id,
                    area_id=area_id,
                    cantidad=cantidad,
                    codigo=None,
                    fecha_imputacion=datetime.utcnow()
                )
                db.session.add(stock)

        # Registrar movimiento
        movimiento = MovimientoStock(
            stock_destino_id=None,  # Se actualizará después del commit si es necesario
            insumo_id=insumo_id,
            cantidad=cantidad,
            observacion=observacion or f"Imputación inicial a {area.nombre}",
            responsable=responsable
        )
        db.session.add(movimiento)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"{cantidad} unidad(es) de '{insumo.nombre_completo}' imputadas a '{area.nombre}'",
            "details": {
                "insumo": insumo.nombre_completo,
                "area": area.nombre,
                "cantidad": cantidad,
                "inventariable": insumo.inventariable,
                "codigos": codigos_creados if insumo.inventariable else None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@stock_bp.route('/stock/mover', methods=['POST'])
def mover_stock():
    """Mueve stock entre áreas"""
    data = request.get_json()
    stock_origen_id = data.get('stock_origen_id')
    area_destino_id = data.get('area_destino_id')
    cantidad_mover = data.get('cantidad', 1)
    responsable = data.get('responsable', '')
    observacion = data.get('observacion', '')

    if not all([stock_origen_id, area_destino_id]):
        return jsonify({"success": False, "message": "Stock origen y área destino son requeridos"}), 400

    try:
        stock_origen = StockUbicacion.query.get_or_404(stock_origen_id)
        area_destino = Area.query.get_or_404(area_destino_id)

        if stock_origen.area_id == area_destino_id:
            return jsonify({"success": False, "message": "El stock ya se encuentra en esa área"}), 400

        if stock_origen.insumo.inventariable:
            # Para inventariables, solo se puede mover de a 1 (el item completo)
            if cantidad_mover != 1:
                return jsonify({"success": False, "message": "Los items inventariables se mueven de a uno"}), 400
            
            # Cambiar la ubicación del item
            area_origen = stock_origen.area
            stock_origen.area_id = area_destino_id
            stock_origen.ultimo_movimiento = datetime.utcnow()

            # Registrar movimiento
            movimiento = MovimientoStock(
                stock_origen_id=stock_origen_id,
                stock_destino_id=stock_origen_id,  # Mismo item, nueva ubicación
                insumo_id=stock_origen.insumo_id,
                cantidad=1,
                observacion=observacion or f"Movimiento de {area_origen.nombre} a {area_destino.nombre}",
                responsable=responsable
            )
            db.session.add(movimiento)

        else:
            # Para no inventariables, mover cantidad específica
            if stock_origen.cantidad < cantidad_mover:
                return jsonify({"success": False, "message": "No hay suficiente cantidad disponible"}), 400

            # Reducir cantidad en origen
            stock_origen.cantidad -= cantidad_mover
            stock_origen.ultimo_movimiento = datetime.utcnow()

            # Buscar o crear stock en destino
            stock_destino = StockUbicacion.query.filter_by(
                insumo_id=stock_origen.insumo_id,
                area_id=area_destino_id,
                codigo=None
            ).first()

            if stock_destino:
                stock_destino.cantidad += cantidad_mover
                stock_destino.ultimo_movimiento = datetime.utcnow()
            else:
                stock_destino = StockUbicacion(
                    insumo_id=stock_origen.insumo_id,
                    area_id=area_destino_id,
                    cantidad=cantidad_mover,
                    codigo=None,
                    fecha_imputacion=datetime.utcnow()
                )
                db.session.add(stock_destino)

            # Eliminar registro origen si cantidad queda en 0
            if stock_origen.cantidad == 0:
                db.session.delete(stock_origen)

            # Registrar movimiento
            movimiento = MovimientoStock(
                stock_origen_id=stock_origen_id if stock_origen.cantidad > 0 else None,
                stock_destino_id=None,  # Se actualizará después del commit
                insumo_id=stock_origen.insumo_id,
                cantidad=cantidad_mover,
                observacion=observacion or f"Movimiento de {stock_origen.area.nombre} a {area_destino.nombre}",
                responsable=responsable
            )
            db.session.add(movimiento)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Stock movido correctamente a {area_destino.nombre}",
            "movimiento": {
                "insumo": stock_origen.insumo.nombre_completo,
                "cantidad": cantidad_mover,
                "destino": area_destino.nombre,
                "responsable": responsable
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# Endpoints auxiliares
@stock_bp.route('/stock/tipos', methods=['GET'])
def get_tipos():
    tipos = TipoProducto.query.all()
    return jsonify([{"id": t.id, "nombre": t.nombre} for t in tipos])

@stock_bp.route('/stock/marcas', methods=['GET'])
def get_marcas():
    marcas = Marca.query.all()
    return jsonify([{"id": m.id, "nombre": m.nombre} for m in marcas])

@stock_bp.route('/stock/modelos', methods=['GET'])
def get_modelos():
    modelos = Modelo.query.all()
    return jsonify([{"id": m.id, "nombre": m.nombre, "marca_id": m.marca_id} for m in modelos])

@stock_bp.route('/stock/areas', methods=['GET'])
def get_areas():
    areas = Area.query.all()
    return jsonify([{
        "id": area.id,
        "nombre": area.nombre,
        "es_deposito": area.es_deposito,
        "unidad_organizativa": area.unidad_organizativa.nombre if area.unidad_organizativa else None
    } for area in areas])

@stock_bp.route('/stock/toners', methods=['GET'])
def get_toners_from_stock():
    """Obtiene todos los tóners"""
    toners = Toner.query.all()
    return jsonify([{"id": t.id, "nombre": t.nombre} for t in toners])

@stock_bp.route('/stock/baterias', methods=['GET'])
def get_baterias_from_stock():
    """Obtiene todas las baterías"""
    baterias = Bateria.query.all()
    return jsonify([{"id": b.id, "cantidad": b.cantidad} for b in baterias])

@stock_bp.route('/stock/insumos/<int:insumo_id>', methods=['PUT'])
def update_insumo(insumo_id):
    """Actualizar un insumo existente"""
    data = request.get_json()
    
    try:
        insumo = Insumo.query.get_or_404(insumo_id)
        
        # Validar que los modelos existan
        if data.get('tipo_id') and not TipoProducto.query.get(data['tipo_id']):
            return jsonify({"success": False, "message": "Tipo de producto no válido"}), 400
        if data.get('marca_id') and not Marca.query.get(data['marca_id']):
            return jsonify({"success": False, "message": "Marca no válida"}), 400
        if data.get('modelo_id') and not Modelo.query.get(data['modelo_id']):
            return jsonify({"success": False, "message": "Modelo no válido"}), 400
        if data.get('toner_id') and not Toner.query.get(data['toner_id']):
            return jsonify({"success": False, "message": "Tóner no válido"}), 400
        if data.get('bateria_id') and not Bateria.query.get(data['bateria_id']):
            return jsonify({"success": False, "message": "Batería no válida"}), 400
        
        # Actualizar campos
        if 'tipo_id' in data:
            insumo.tipo_id = data['tipo_id']
        if 'marca_id' in data:
            insumo.marca_id = data['marca_id']
        if 'modelo_id' in data:
            insumo.modelo_id = data['modelo_id']
        if 'descripcion' in data:
            insumo.descripcion = data['descripcion']
        if 'inventariable' in data:
            insumo.inventariable = data['inventariable']
        if 'toner_id' in data:
            insumo.toner_id = data['toner_id'] if data['toner_id'] else None
        if 'bateria_id' in data:
            insumo.bateria_id = data['bateria_id'] if data['bateria_id'] else None
        if 'url_imagen' in data:
            insumo.url_imagen = data['url_imagen']
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Insumo actualizado correctamente",
            "insumo": {
                "id": insumo.id,
                "nombre_completo": insumo.nombre_completo
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@stock_bp.route('/stock/baja', methods=['POST'])
def dar_baja_stock():
    """Dar de baja una imputación de stock"""
    data = request.get_json()
    stock_id = data.get('stock_id')
    motivo = data.get('motivo')
    responsable = data.get('responsable')
    observacion = data.get('observacion')
    
    if not stock_id or not motivo:
        return jsonify({"success": False, "message": "Stock ID y motivo son requeridos"}), 400
    
    try:
        stock_item = StockUbicacion.query.get_or_404(stock_id)
        
        # Actualizar estado a 'baja'
        stock_item.estado = 'baja'
        stock_item.ultimo_movimiento = datetime.utcnow()
        
        # Registrar movimiento de baja
        movimiento = MovimientoStock(
            stock_origen_id=stock_id,
            stock_destino_id=None,
            insumo_id=stock_item.insumo_id,
            cantidad=stock_item.cantidad,
            observacion=f"BAJA: {motivo}. {observacion or ''}",
            responsable=responsable or "Sistema",
            tipo_movimiento="baja"
        )
        db.session.add(movimiento)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Stock dado de baja correctamente. Motivo: {motivo}"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@stock_bp.route('/stock/insumos/<int:insumo_id>', methods=['DELETE'])
def delete_insumo(insumo_id):
    """Eliminar un insumo solo si no tiene stock activo"""
    try:
        insumo = Insumo.query.get_or_404(insumo_id)
        
        # Verificar si tiene stock activo (no dado de baja)
        stock_activo = StockUbicacion.query.filter(
            StockUbicacion.insumo_id == insumo_id,
            StockUbicacion.estado != 'baja'
        ).first()
        
        if stock_activo:
            return jsonify({
                "success": False, 
                "message": "No se puede eliminar el insumo porque tiene stock activo. Debe dar de baja todas las imputaciones primero."
            }), 400
        
        # Verificar si tiene movimientos históricos
        movimientos = MovimientoStock.query.filter_by(insumo_id=insumo_id).count()
        
        if movimientos > 0:
            # Si tiene movimientos históricos, solo desactivar
            insumo.activo = False
            mensaje = "Insumo desactivado correctamente (se conserva el historial)"
        else:
            # Si no tiene movimientos, eliminar completamente
            db.session.delete(insumo)
            mensaje = "Insumo eliminado correctamente"
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": mensaje
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@stock_bp.route('/stock/insumos', methods=['GET'])
def get_insumos():
    """Obtiene todos los insumos activos"""
    # Filtrar solo insumos activos
    insumos = Insumo.query.filter_by(activo=True).all()
    return jsonify([{
        "id": insumo.id,
        "nombre_completo": insumo.nombre_completo,
        "tipo": {"id": insumo.tipo.id, "nombre": insumo.tipo.nombre},
        "marca": {"id": insumo.marca.id, "nombre": insumo.marca.nombre},
        "modelo": {"id": insumo.modelo.id, "nombre": insumo.modelo.nombre},
        "descripcion": insumo.descripcion,
        "inventariable": insumo.inventariable,
        "toner": {"id": insumo.toner.id, "nombre": insumo.toner.nombre} if insumo.toner else None,
        "bateria": {"id": insumo.bateria.id, "cantidad": insumo.bateria.cantidad} if insumo.bateria else None,
        "url_imagen": insumo.url_imagen,
        "fecha_creacion": insumo.fecha_creacion.isoformat()
    } for insumo in insumos])