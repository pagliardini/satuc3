from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TipoProducto(db.Model):
    __tablename__ = 'tipos_productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    productos = db.relationship('Producto', backref='tipo', lazy=True)

class Marca(db.Model):
    __tablename__ = 'marcas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    modelos = db.relationship('Modelo', backref='marca', lazy=True)
    productos = db.relationship('Producto', backref='marca', lazy=True)

class Modelo(db.Model):
    __tablename__ = 'modelos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    productos = db.relationship('Producto', backref='modelo', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_productos.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelos.id'), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    cantidad = db.Column(db.Integer, default=0)  # Agregar el campo cantidad con valor por defecto 0
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
