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