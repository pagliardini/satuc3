from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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

class Insumo(db.Model):
    __tablename__ = 'insumos'
    id = db.Column(db.Integer, primary_key=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_producto.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelos.id'), nullable=False)
    descripcion = db.Column(db.String(255))  # Aumentar tamaño
    inventariable = db.Column(db.Boolean, default=True)
    activo = db.Column(db.Boolean, default=True)
    toner_id = db.Column(db.Integer, db.ForeignKey('toners.id'), nullable=True)
    bateria_id = db.Column(db.Integer, db.ForeignKey('baterias.id'), nullable=True)
    url_imagen = db.Column(db.String(255), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    tipo = db.relationship('TipoProducto', backref='insumos')
    marca = db.relationship('Marca', backref='insumos')
    modelo = db.relationship('Modelo', backref='insumos')
    toner = db.relationship('Toner', backref='insumos', lazy=True)
    bateria = db.relationship('Bateria', backref='insumos', lazy=True)
    stock_ubicaciones = db.relationship('StockUbicacion', backref='insumo', lazy=True)

    @property
    def nombre_completo(self):
        """Propiedad calculada que concatena tipo, marca, modelo y descripción."""
        try:
            tipo = self.tipo.nombre if self.tipo else "Sin Tipo"
            marca = self.marca.nombre if self.marca else "Sin Marca"
            modelo = self.modelo.nombre if self.modelo else "Sin Modelo"
            descripcion = f" - {self.descripcion}" if self.descripcion else ""
            return f"{tipo} {marca} {modelo}{descripcion}"
        except:
            return f"Insumo #{self.id}"

class StockUbicacion(db.Model):
    __tablename__ = 'stock_ubicacion'
    id = db.Column(db.Integer, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    codigo = db.Column(db.String(50), nullable=True)  # Solo para inventariables
    fecha_imputacion = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_movimiento = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = db.Column(db.String(20), default='disponible')  # disponible, asignado, en_reparacion, baja
    
    # NUEVO: Agregar referencia al usuario que realizó la imputación
    usuario_imputacion_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    usuario_ultimo_movimiento_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relaciones
    usuario_imputacion = db.relationship('User', foreign_keys=[usuario_imputacion_id], backref='imputaciones_realizadas')
    usuario_ultimo_movimiento = db.relationship('User', foreign_keys=[usuario_ultimo_movimiento_id], backref='movimientos_realizados')

    # Constraints existentes
    __table_args__ = (
        db.Index('idx_insumo_area', 'insumo_id', 'area_id'),
        db.Index('idx_codigo', 'codigo'),
    )

class MovimientoStock(db.Model):
    __tablename__ = 'movimientos_stock'
    id = db.Column(db.Integer, primary_key=True)
    stock_origen_id = db.Column(db.Integer, db.ForeignKey('stock_ubicacion.id'), nullable=True)
    stock_destino_id = db.Column(db.Integer, db.ForeignKey('stock_ubicacion.id'), nullable=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    observacion = db.Column(db.String(200), nullable=True)
    responsable = db.Column(db.String(100), nullable=True)  # Mantener por compatibilidad
    tipo_movimiento = db.Column(db.String(20), default='movimiento')  # movimiento, baja, imputacion
    
    # NUEVO: Agregar referencia al usuario que realizó el movimiento
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relaciones
    stock_origen = db.relationship('StockUbicacion', foreign_keys=[stock_origen_id], lazy=True)
    stock_destino = db.relationship('StockUbicacion', foreign_keys=[stock_destino_id], lazy=True)
    insumo = db.relationship('Insumo', backref='movimientos')
    usuario = db.relationship('User', backref='movimientos_usuario')

class Toner(db.Model):
    __tablename__ = 'toners'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(8), nullable=False)

class Bateria(db.Model):
    __tablename__ = 'baterias'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' o 'general'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)