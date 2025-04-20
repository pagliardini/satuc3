#DESDE AQUI SE GESTIONAN MARCAS, TIPOS Y MODELOS DE PRODUCTOS
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, TipoProducto, Marca, Modelo

mtm_bp = Blueprint('mtm', __name__, url_prefix='/mtm')

@mtm_bp.route('/', methods=['GET', 'POST'])
def mtm_index():
    marcas = Marca.query.all()
    tipos = TipoProducto.query.all()
    modelos = Modelo.query.all()
    return render_template('mtm.html', marcas=marcas, tipos=tipos, modelos=modelos)

# Ruta para agregar un nuevo tipo de producto
@mtm_bp.route('/add_tipo', methods=['POST'])
def add_tipo():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        nombre = data.get('nombre')

    if not nombre:
        msg = 'El nombre del tipo es obligatorio.'
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    if TipoProducto.query.filter_by(nombre=nombre).first():
        msg = 'El tipo de producto ya existe.'
        if request.is_json:
            return jsonify({'error': msg}), 409
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    nuevo_tipo = TipoProducto(nombre=nombre)
    db.session.add(nuevo_tipo)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Tipo agregado exitosamente.', 'id': nuevo_tipo.id}), 201

    flash('Tipo agregado exitosamente.', 'success')
    return redirect(url_for('mtm.mtm_index'))

# Ruta para agregar una nueva marca
@mtm_bp.route('/add_marca', methods=['POST'])
def add_marca():
    data = request.get_json() if request.is_json else request.form
    nombre = data.get('nombre')

    if not nombre:
        msg = 'El nombre de la marca es obligatorio.'
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    if Marca.query.filter_by(nombre=nombre).first():
        msg = 'Esta marca ya existe.'
        if request.is_json:
            return jsonify({'error': msg}), 409
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    nueva_marca = Marca(nombre=nombre)
    db.session.add(nueva_marca)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Marca agregada exitosamente.', 'id': nueva_marca.id}), 201

    flash('Marca agregada exitosamente.', 'success')
    return redirect(url_for('mtm.mtm_index'))

# Ruta para agregar un nuevo modelo
@mtm_bp.route('/add_modelo', methods=['POST'])
def add_modelo():
    data = request.get_json() if request.is_json else request.form
    nombre = data.get('nombre')
    marca_id = data.get('marca_id')

    if not nombre or not marca_id:
        msg = 'Todos los campos son obligatorios.'
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    if not Marca.query.get(marca_id):
        msg = 'Marca no válida.'
        if request.is_json:
            return jsonify({'error': msg}), 404
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    modelo_existente = Modelo.query.filter_by(nombre=nombre, marca_id=marca_id).first()
    if modelo_existente:
        msg = 'Este modelo ya existe para la marca seleccionada.'
        if request.is_json:
            return jsonify({'error': msg}), 409
        flash(msg, 'error')
        return redirect(url_for('mtm.mtm_index'))

    nuevo_modelo = Modelo(nombre=nombre, marca_id=marca_id)
    db.session.add(nuevo_modelo)
    db.session.commit()

    if request.is_json:
        return jsonify({'mensaje': 'Modelo agregado exitosamente.', 'id': nuevo_modelo.id}), 201

    flash('Modelo agregado exitosamente.', 'success')
    return redirect(url_for('mtm.mtm_index'))


