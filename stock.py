from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Producto, Area, StockUbicacion, MovimientoStock

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# Ruta principal de stock
@stock_bp.route('/')
def stock_index():
    return render_template('stock.html')

# Ruta para registrar movimiento de stock
@stock_bp.route('/add_movimiento_stock', methods=['GET', 'POST'])
def add_movimiento_stock():
    productos = Producto.query.all()
    areas = Area.query.all()

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        desde_area_id = request.form.get('desde_area_id') or None
        hacia_area_id = request.form['hacia_area_id']
        cantidad = int(request.form['cantidad'])

        # Stock en destino
        stock_destino = StockUbicacion.query.filter_by(
            producto_id=producto_id,
            area_id=hacia_area_id
        ).first()

        if not stock_destino:
            stock_destino = StockUbicacion(
                producto_id=producto_id,
                area_id=hacia_area_id,
                cantidad=0
            )
            db.session.add(stock_destino)

        stock_destino.cantidad += cantidad

        # Si es traslado, descuenta del origen
        if desde_area_id:
            stock_origen = StockUbicacion.query.filter_by(
                producto_id=producto_id,
                area_id=desde_area_id
            ).first()

            if not stock_origen or stock_origen.cantidad < cantidad:
                flash('Stock insuficiente en el origen.', 'error')
                return redirect(url_for('stock.add_movimiento_stock'))

            stock_origen.cantidad -= cantidad

        # Registrar movimiento
        movimiento = MovimientoStock(
            producto_id=producto_id,
            origen_area_id=desde_area_id,
            destino_area_id=hacia_area_id,
            cantidad=cantidad
        )

        db.session.add(movimiento)
        db.session.commit()

        flash('Movimiento registrado correctamente.', 'success')
        return redirect(url_for('stock.add_movimiento_stock'))

    return render_template('add_movimiento_stock.html', productos=productos, areas=areas)

# Ruta para registrar stock físico
@stock_bp.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    productos = Producto.query.all()
    areas = Area.query.all()

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        area_id = request.form['area_id']
        cantidad = int(request.form['cantidad'])

        # Validar producto y área
        producto = Producto.query.get_or_404(producto_id)
        area = Area.query.get_or_404(area_id)

        # Registrar stock en el área
        stock_existente = StockUbicacion.query.filter_by(
            producto_id=producto_id,
            area_id=area_id
        ).first()

        if stock_existente:
            stock_existente.cantidad += cantidad
        else:
            stock_existente = StockUbicacion(
                producto_id=producto_id,
                area_id=area_id,
                cantidad=cantidad
            )
            db.session.add(stock_existente)

        db.session.commit()

        flash(f'Se registraron {cantidad} unidades del producto "{producto.descripcion}" en el área "{area.nombre}".', 'success')
        return redirect(url_for('stock.add_stock'))

    return render_template('add_stock.html', productos=productos, areas=areas)