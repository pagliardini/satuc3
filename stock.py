from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Producto, Area, StockUbicacion, MovimientoStock

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# Ruta principal de stock
@stock_bp.route('/')
def stock_index():
    return render_template('stock.html')

# Ruta para registrar stock físico
@stock_bp.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    productos = Producto.query.all()
    areas = Area.query.all()

    # Obtener el último código generado para productos inventariables
    ultimo_codigo = db.session.query(db.func.max(StockUbicacion.codigo)).scalar()
    if not ultimo_codigo:
        ultimo_codigo = 500  # Comenzar desde 500 si no hay registros previos
    else:
        ultimo_codigo = int(ultimo_codigo)

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        area_id = request.form['area_id']
        cantidad = int(request.form['cantidad'])

        # Validar producto y área
        producto = Producto.query.get_or_404(producto_id)
        area = Area.query.get_or_404(area_id)

        # Obtener el nombre completo del producto
        producto_nombre = producto.nombre_completo

        if producto.inventariable:
            # Generar registros individuales para cada unidad
            for _ in range(cantidad):
                ultimo_codigo += 1
                stock = StockUbicacion(
                    area_id=area_id,
                    producto_nombre=producto_nombre,
                    codigo=str(ultimo_codigo),  # Generar código único
                    cantidad=1  # Cada registro representa una unidad
                )
                db.session.add(stock)
        else:
            # Crear un solo registro con la cantidad total
            stock_existente = StockUbicacion.query.filter_by(
                area_id=area_id,
                producto_nombre=producto_nombre
            ).first()

            if stock_existente:
                stock_existente.cantidad += cantidad
            else:
                stock = StockUbicacion(
                    area_id=area_id,
                    producto_nombre=producto_nombre,
                    codigo=str(ultimo_codigo + 1),  # Generar un código único
                    cantidad=cantidad
                )
                db.session.add(stock)

        db.session.commit()

        # Mensaje flash
        flash(f'Se registraron {cantidad} unidades del producto "{producto_nombre}" en el área "{area.nombre}".', 'success')

        # Redirigir a la misma página
        return redirect(url_for('stock.add_stock'))

    return render_template('add_stock.html', productos=productos, areas=areas)

@stock_bp.route('/inventario', methods=['GET'])
def inventario():
    # Consulta el inventario agrupado por área
    inventario = db.session.query(
        StockUbicacion,
        Area
    ).join(Area, StockUbicacion.area_id == Area.id)\
     .order_by(Area.nombre, StockUbicacion.producto_nombre).all()

    return render_template('inventario.html', inventario=inventario)

@stock_bp.route('/mover_stock', methods=['GET', 'POST'])
def mover_stock():
    print("Entrando a la función mover_stock")  # Mensaje de depuración
    areas = Area.query.all()
    inventario = StockUbicacion.query.all()

    if request.method == 'POST':
        stock_id = int(request.form['stock_id'])
        destino_area_id = int(request.form['destino_area_id'])
        cantidad = int(request.form['cantidad'])

        stock_origen = StockUbicacion.query.get_or_404(stock_id)
        destino_area = Area.query.get_or_404(destino_area_id)

        if stock_origen.area_id == destino_area_id:
            flash('El área de destino no puede ser la misma que el área de origen.', 'warning')
            return redirect(url_for('stock.mover_stock'))

        if stock_origen.cantidad < cantidad:
            flash('Cantidad insuficiente para realizar el movimiento.', 'danger')
            return redirect(url_for('stock.mover_stock'))

        # Caso inventariable (cantidad siempre es 1)
        if stock_origen.cantidad == 1 and cantidad == 1:
            stock_origen.area_id = destino_area_id  # Solo cambiamos de área
        else:
            # Reducimos del origen
            stock_origen.cantidad -= cantidad

            # Buscar si ya existe en el destino
            stock_destino = StockUbicacion.query.filter_by(
                area_id=destino_area_id,
                producto_nombre=stock_origen.producto_nombre
            ).first()

            if stock_destino:
                stock_destino.cantidad += cantidad
            else:
                nuevo_codigo = int(db.session.query(db.func.max(StockUbicacion.codigo)).scalar()) + 1
                stock_destino = StockUbicacion(
                    area_id=destino_area_id,
                    producto_nombre=stock_origen.producto_nombre,
                    codigo=str(nuevo_codigo),
                    cantidad=cantidad
                )
                db.session.add(stock_destino)

        # Registrar el movimiento
        movimiento = MovimientoStock(
            stock_origen_id=stock_origen.id,
            stock_destino_id=stock_destino.id if 'stock_destino' in locals() else None,
            cantidad=cantidad,
            observacion=request.form.get('observacion', '')
        )
        db.session.add(movimiento)
        db.session.commit()

        flash(f'Se movieron {cantidad} unidades de "{stock_origen.producto_nombre}" a "{destino_area.nombre}".', 'success')
        return redirect(url_for('stock.mover_stock'))

    return render_template('mover_stock.html', inventario=inventario, areas=areas)
