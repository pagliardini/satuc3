#DESDE AQUI SE GESTIONAN MARCAS, TIPOS Y MODELOS DE PRODUCTOS
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, TipoProducto, Marca, Modelo

mtm_bp = Blueprint('mtm', __name__, url_prefix='/mtm')

# Ruta para agregar un nuevo tipo de producto
@mtm_bp.route('/add_tipo', methods=['GET', 'POST'])
def add_tipo():
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre del tipo es obligatorio.', 'error')
            return redirect(url_for('mtm.add_tipo'))

        tipo_existente = TipoProducto.query.filter_by(nombre=nombre).first()
        if tipo_existente:
            flash('Este tipo de producto ya existe.', 'error')
            return redirect(url_for('mtm.add_tipo'))

        nuevo_tipo = TipoProducto(nombre=nombre)
        db.session.add(nuevo_tipo)
        db.session.commit()
        flash('Tipo de producto agregado exitosamente.', 'success')
        return redirect(url_for('mtm.add_tipo'))

    tipos = TipoProducto.query.all()
    return render_template('add_tipo.html', tipos=tipos)

# Ruta para agregar una nueva marca
@mtm_bp.route('/add_marca', methods=['GET', 'POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre de la marca es obligatorio.', 'error')
            return redirect(url_for('mtm.add_marca'))

        marca_existente = Marca.query.filter_by(nombre=nombre).first()
        if marca_existente:
            flash('Esta marca ya existe.', 'error')
            return redirect(url_for('mtm.add_marca'))

        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        flash('Marca agregada exitosamente.', 'success')
        return redirect(url_for('mtm.add_marca'))

    marcas = Marca.query.all()
    return render_template('add_marca.html', marcas=marcas)

# Ruta para agregar un nuevo modelo
@mtm_bp.route('/add_modelo', methods=['GET', 'POST'])
def add_modelo():
    marcas = Marca.query.all()

    if request.method == 'POST':
        marca_id = request.form['marca_id']
        nombre = request.form.get('nombre')

        if not nombre or not marca_id:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('mtm.add_modelo'))

        modelo_existente = Modelo.query.filter_by(nombre=nombre, marca_id=marca_id).first()
        if modelo_existente:
            flash('Este modelo ya existe para la marca seleccionada.', 'error')
            return redirect(url_for('mtm.add_modelo'))

        nuevo_modelo = Modelo(nombre=nombre, marca_id=marca_id)
        db.session.add(nuevo_modelo)
        db.session.commit()
        flash('Modelo agregado exitosamente.', 'success')
        return redirect(url_for('mtm.add_modelo'))

    return render_template('add_modelo.html', marcas=marcas)