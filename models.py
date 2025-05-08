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
    productos = db.relationship('Producto', backref='marca', lazy=True)

class Modelo(db.Model):
    __tablename__ = 'modelos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    productos = db.relationship('Producto', backref='modelo', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_productos.id', name='fk_producto_tipo'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id', name='fk_producto_marca'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelos.id', name='fk_producto_modelo'), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    inventariable = db.Column(db.Boolean, default=True)  # Si es por unidad física con sticker
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def nombre_completo(self):
        """Propiedad calculada que concatena marca, modelo y descripción."""
        tipo = self.tipo.nombre if self.tipo else "Sin Tipo" 
        marca = self.marca.nombre if self.marca else "Sin Marca"
        modelo = self.modelo.nombre if self.modelo else "Sin Modelo"
        descripcion = f" - {self.descripcion}" if self.descripcion else ""
        return f"{tipo} {marca} {modelo}{descripcion}"

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
    
    # Fix the relationship to match Sede's back_populates
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
    es_deposito = db.Column(db.Boolean, default=False)  # Nueva columna para identificar depósitos

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
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    producto_nombre = db.Column(db.String(200), nullable=False)  # Nombre del producto (marca, modelo, etc.)
    codigo = db.Column(db.String(50), nullable=False)  # Código único para identificar el producto en la ubicación

    __table_args__ = (
        db.UniqueConstraint('area_id', 'codigo', name='uq_area_codigo'),  # Restricción única por área y código
    )

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

    @property
    def producto(self):
        """Propiedad útil para acceder al producto relacionado desde cualquiera de los stock involucrados"""
        return self.stock_origen.producto if self.stock_origen else self.stock_destino.producto

