from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, TipoProducto, Marca, Modelo, Producto, Sede, Area, StockUbicacion, MovimientoStock

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

# Ruta para la lista de productos
@productos_bp.route('/')
def productos_index():
    productos = Producto.query.all()
    return render_template('productos_list.html', productos=productos)

@productos_bp.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    tipos = TipoProducto.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()

    if request.method == 'POST':
        tipo_id = request.form['tipo_id']
        marca_id = request.form['marca_id']
        modelo_id = request.form['modelo_id']
        descripcion = request.form.get('descripcion')
        inventariable = request.form.get('inventariable', 'off') == 'on'
        activo = request.form.get('activo', 'off') == 'on'

        if not tipo_id or not marca_id or not modelo_id:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('productos.add_producto'))

        # Crear un registro para el producto
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

        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('productos.productos_index'))

    return render_template('add_producto.html', tipos=tipos, marcas=marcas, modelos=modelos)

# Ruta para editar un producto
@productos_bp.route('/edit_producto/<int:id>', methods=['GET', 'POST'])
def edit_producto(id):
    producto = Producto.query.get_or_404(id)
    tipos = TipoProducto.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()

    if request.method == 'POST':
        producto.tipo_id = request.form['tipo_id']
        producto.marca_id = request.form['marca_id']
        producto.modelo_id = request.form['modelo_id']
        producto.descripcion = request.form.get('descripcion')
        producto.activo = request.form.get('activo', 'off') == 'on'

        db.session.commit()
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('productos.productos_index'))

    return render_template('edit_producto.html', producto=producto, tipos=tipos, marcas=marcas, modelos=modelos)

# Ruta para eliminar un producto
@productos_bp.route('/delete_producto/<int:id>', methods=['POST'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('productos.productos_index'))

@productos_bp.route('/add_movimiento_stock', methods=['GET', 'POST'])
def add_movimiento_stock():
    productos = Producto.query.all()
    sedes = Sede.query.all()
    areas = Area.query.all()

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        desde_sede_id = request.form.get('desde_sede_id') or None
        desde_area_id = request.form.get('desde_area_id') or None
        hacia_sede_id = request.form['hacia_sede_id']
        hacia_area_id = request.form['hacia_area_id']
        cantidad = int(request.form['cantidad'])

        # Actualiza o crea stock en destino
        stock_destino = StockUbicacion.query.filter_by(
            producto_id=producto_id,
            sede_id=hacia_sede_id,
            area_id=hacia_area_id
        ).first()

        if not stock_destino:
            stock_destino = StockUbicacion(
                producto_id=producto_id,
                sede_id=hacia_sede_id,
                area_id=hacia_area_id,
                cantidad=0
            )
            db.session.add(stock_destino)

        stock_destino.cantidad += cantidad

        # Si es una transferencia, descuenta de origen
        if desde_sede_id and desde_area_id:
            stock_origen = StockUbicacion.query.filter_by(
                producto_id=producto_id,
                sede_id=desde_sede_id,
                area_id=desde_area_id
            ).first()

            if not stock_origen or stock_origen.cantidad < cantidad:
                flash('Stock insuficiente en el origen.', 'error')
                return redirect(url_for('productos.add_movimiento_stock'))

            stock_origen.cantidad -= cantidad

        # Registra el movimiento
        movimiento = MovimientoStock(
            producto_id=producto_id,
            desde_sede_id=desde_sede_id,
            desde_area_id=desde_area_id,
            hacia_sede_id=hacia_sede_id,
            hacia_area_id=hacia_area_id,
            cantidad=cantidad
        )

        db.session.add(movimiento)
        db.session.commit()

        flash('Movimiento registrado correctamente.', 'success')
        return redirect(url_for('productos.add_movimiento_stock'))

    return render_template('add_movimiento_stock.html', productos=productos, sedes=sedes, areas=areas)