from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, TipoProducto, Marca, Modelo, Producto, Sede, Area, StockUbicacion, MovimientoStock

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

# Ruta para la lista de productos
@productos_bp.route('/')
def productos_index():
    productos = Producto.query.all()
    return render_template('productos_list.html', productos=productos)

# Ruta para agregar producto
@productos_bp.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    tipos = TipoProducto.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()

    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form

        tipo_id = data.get('tipo_id')
        marca_id = data.get('marca_id')
        modelo_id = data.get('modelo_id')
        descripcion = data.get('descripcion', '')
        inventariable = data.get('inventariable', False)
        activo = data.get('activo', False)

        # Procesa checkboxes si viene del formulario
        if not request.is_json:
            inventariable = True if data.get('inventariable', 'off') == 'on' else False
            activo = True if data.get('activo', 'off') == 'on' else False

        errores = []

        # Validaciones
        if not tipo_id or not TipoProducto.query.get(tipo_id):
            errores.append('Tipo de producto inválido o inexistente.')

        if not marca_id or not Marca.query.get(marca_id):
            errores.append('Marca inválida o inexistente.')



        # Eliminar validación de unicidad
        # producto_existente = Producto.query.filter_by(marca_id=marca_id, modelo_id=modelo_id).first()
        # if producto_existente:
        #     errores.append('Ya existe un producto con esta combinación de marca y modelo.')

        if errores:
            if request.is_json:
                return {"success": False, "errors": errores}, 400
            else:
                for error in errores:
                    flash(error, 'error')
                return redirect(url_for('productos.add_producto'))

        # Crear producto
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

        if request.is_json:
            return {"success": True, "message": "Producto creado correctamente."}, 201
        else:
            flash('Producto creado correctamente.', 'success')
            return redirect(url_for('productos.productos_index'))

    return render_template('add_producto.html', tipos=tipos, marcas=marcas, modelos=modelos)

# Ruta para editar producto
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

# Ruta para eliminar producto
@productos_bp.route('/delete_producto/<int:id>', methods=['POST'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('productos.productos_index'))

