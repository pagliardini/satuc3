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
    inventariable = db.Column(db.Boolean, default=True)  # Si es por unidad física con sticker
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Sede(db.Model):
    __tablename__ = 'sedes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    areas = db.relationship('Area', backref='sede', lazy=True)

class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    sede_id = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)

class StockUbicacion(db.Model):
    __tablename__ = 'stock_ubicacion'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    sede_id = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)

    producto = db.relationship('Producto', backref='stock_ubicaciones', lazy=True)
    sede = db.relationship('Sede', lazy=True)
    area = db.relationship('Area', lazy=True)

class MovimientoStock(db.Model):
    __tablename__ = 'movimientos_stock'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    origen_sede_id = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=True)
    origen_area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=True)
    destino_sede_id = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=True)
    destino_area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    observacion = db.Column(db.String(200), nullable=True)

    producto = db.relationship('Producto', lazy=True)
    origen_sede = db.relationship('Sede', foreign_keys=[origen_sede_id], lazy=True)
    origen_area = db.relationship('Area', foreign_keys=[origen_area_id], lazy=True)
    destino_sede = db.relationship('Sede', foreign_keys=[destino_sede_id], lazy=True)
    destino_area = db.relationship('Area', foreign_keys=[destino_area_id], lazy=True)
