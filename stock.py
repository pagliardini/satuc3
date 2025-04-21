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

        # Mensaje flash
        flash(f'Se registraron {cantidad} unidades del producto "{producto.nombre_completo}" en el área "{area.nombre}".', 'success')

        # Redirigir a la misma página
        return redirect(url_for('stock.add_stock'))

    return render_template('add_stock.html', productos=productos, areas=areas)

@stock_bp.route('/inventario', methods=['GET'])
def inventario():
    # Consulta el inventario agrupado por área
    inventario = db.session.query(
        StockUbicacion,
        Producto,
        Area
    ).join(Producto, StockUbicacion.producto_id == Producto.id)\
     .join(Area, StockUbicacion.area_id == Area.id)\
     .order_by(Area.nombre, Producto.marca_id, Producto.modelo_id).all()

    return render_template('inventario.html', inventario=inventario)