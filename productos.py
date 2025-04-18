from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, TipoProducto, Marca, Modelo, Producto

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
        cantidad = request.form.get('cantidad', 0, type=int)
        inventariable = request.form.get('inventariable', 'off') == 'on'
        activo = request.form.get('activo', 'off') == 'on'

        if not tipo_id or not marca_id or not modelo_id:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('productos.add_producto'))

        # Si es inventariable y la cantidad es mayor a 1, crear múltiples registros
        if inventariable:
            if cantidad < 1:
                flash('La cantidad debe ser al menos 1 para productos inventariables.', 'error')
                return redirect(url_for('productos.add_producto'))

            for _ in range(cantidad):
                nuevo_producto = Producto(
                    tipo_id=tipo_id,
                    marca_id=marca_id,
                    modelo_id=modelo_id,
                    descripcion=descripcion,
                    cantidad=1,  # Cada registro tiene cantidad 1
                    inventariable=inventariable,
                    activo=activo
                )
                db.session.add(nuevo_producto)

            flash(f'{cantidad} productos inventariables creados exitosamente.', 'success')

        # Si no es inventariable, crear un solo registro con la cantidad indicada
        else:
            nuevo_producto = Producto(
                tipo_id=tipo_id,
                marca_id=marca_id,
                modelo_id=modelo_id,
                descripcion=descripcion,
                cantidad=cantidad,  # Se almacena la cantidad total
                inventariable=inventariable,
                activo=activo
            )
            db.session.add(nuevo_producto)
            flash('Producto no inventariable creado exitosamente.', 'success')

        db.session.commit()
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

# Ruta para agregar un nuevo tipo de producto
@productos_bp.route('/add_tipo', methods=['GET', 'POST'])
def add_tipo():
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre del tipo es obligatorio.', 'error')
            return redirect(url_for('productos.add_tipo'))

        tipo_existente = TipoProducto.query.filter_by(nombre=nombre).first()
        if tipo_existente:
            flash('Este tipo de producto ya existe.', 'error')
            return redirect(url_for('productos.add_tipo'))

        nuevo_tipo = TipoProducto(nombre=nombre)
        db.session.add(nuevo_tipo)
        db.session.commit()
        flash('Tipo de producto agregado exitosamente.', 'success')
        return redirect(url_for('productos.add_tipo'))

    tipos = TipoProducto.query.all()
    return render_template('add_tipo.html', tipos=tipos)

# Ruta para agregar un nuevo modelo
@productos_bp.route('/add_modelo', methods=['GET', 'POST'])
def add_modelo():
    marcas = Marca.query.all()

    if request.method == 'POST':
        marca_id = request.form['marca_id']
        nombre = request.form.get('nombre')

        if not nombre or not marca_id:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('productos.add_modelo'))

        modelo_existente = Modelo.query.filter_by(nombre=nombre, marca_id=marca_id).first()
        if modelo_existente:
            flash('Este modelo ya existe para la marca seleccionada.', 'error')
            return redirect(url_for('productos.add_modelo'))

        nuevo_modelo = Modelo(nombre=nombre, marca_id=marca_id)
        db.session.add(nuevo_modelo)
        db.session.commit()
        flash('Modelo agregado exitosamente.', 'success')
        return redirect(url_for('productos.add_modelo'))

    return render_template('add_modelo.html', marcas=marcas)

# Ruta para agregar una nueva marca
@productos_bp.route('/add_marca', methods=['GET', 'POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre de la marca es obligatorio.', 'error')
            return redirect(url_for('productos.add_marca'))

        # Verificar si la marca ya existe
        marca_existente = Marca.query.filter_by(nombre=nombre).first()
        if marca_existente:
            flash('Esta marca ya existe.', 'error')
            return redirect(url_for('productos.add_marca'))

        # Crear una nueva marca
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        flash('Marca agregada exitosamente.', 'success')
        return redirect(url_for('productos.add_marca'))

    # Obtener todas las marcas para mostrarlas en el formulario
    marcas = Marca.query.all()
    return render_template('add_marca.html', marcas=marcas)