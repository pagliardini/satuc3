from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TipoProducto(db.Model):
    __tablename__ = 'tipos_producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
    modelos = db.relationship('Modelo', back_populates='marca')

class Modelo(db.Model):
    __tablename__ = 'modelos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    
    marca = db.relationship('Marca', back_populates='modelos')

class Sede(db.Model):
    __tablename__ = 'sedes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidades = db.relationship('UnidadOrganizativa', back_populates='sede', lazy=True)

class UnidadOrganizativa(db.Model):
    __tablename__ = 'unidades_organizativas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    sede_id = db.Column(db.Integer, db.ForeignKey('sedes.id'), nullable=False)
    
    sede = db.relationship('Sede', back_populates='unidades', lazy=True)
    areas = db.relationship('Area', back_populates='unidad_organizativa', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('nombre', 'sede_id', name='uq_unidad_sede'),
    )

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad_organizativa_id = db.Column(db.Integer, db.ForeignKey('unidades_organizativas.id'), nullable=False)
    es_deposito = db.Column(db.Boolean, default=False)

    unidad_organizativa = db.relationship('UnidadOrganizativa', back_populates='areas')
    stock_ubicaciones = db.relationship('StockUbicacion', backref='area', lazy=True)

    @property
    def sede(self):
        return self.unidad_organizativa.sede

    __table_args__ = (
        db.UniqueConstraint('nombre', 'unidad_organizativa_id', name='uq_area_unidad'),
    )

class StockUbicacion(db.Model):
    __tablename__ = 'stock_ubicacion'
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_producto.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelos.id'), nullable=False)
    descripcion = db.Column(db.String(255))
    inventariable = db.Column(db.Boolean, default=True)
    
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    codigo = db.Column(db.String(50), nullable=True)
    fecha_imputacion = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_movimiento = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tipo = db.relationship('TipoProducto')
    marca = db.relationship('Marca')
    modelo = db.relationship('Modelo')
    
    @property
    def nombre_completo(self):
        try:
            return f"{self.tipo.nombre} {self.marca.nombre} {self.modelo.nombre}"
        except:
            return f"Stock #{self.id}"

class MovimientoStock(db.Model):
    __tablename__ = 'movimientos_stock'
    id = db.Column(db.Integer, primary_key=True)
    stock_origen_id = db.Column(db.Integer, db.ForeignKey('stock_ubicacion.id'), nullable=True)
    stock_destino_id = db.Column(db.Integer, db.ForeignKey('stock_ubicacion.id'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    observacion = db.Column(db.String(200), nullable=True)

    stock_origen = db.relationship('StockUbicacion', foreign_keys=[stock_origen_id], lazy=True)
    stock_destino = db.relationship('StockUbicacion', foreign_keys=[stock_destino_id], lazy=True)

