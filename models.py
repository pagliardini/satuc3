from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Impresora(db.Model):
    __tablename__ = 'impresoras'

    id = db.Column(db.Integer, primary_key=True)
    marcaimpresora_id = db.Column(db.Integer, db.ForeignKey('marcas_impresoras.id'), nullable=False)
    modeloimpresora_id = db.Column(db.Integer, db.ForeignKey('modelos_impresoras.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class MarcaImpresora(db.Model):
    __tablename__ = 'marcas_impresoras'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    impresoras = db.relationship('Impresora', backref='marca', lazy=True)
    modelos = db.relationship('ModeloImpresora', backref='marca', lazy=True)

class ModeloImpresora(db.Model):
    __tablename__ = 'modelos_impresoras'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas_impresoras.id'), nullable=False)
    impresoras = db.relationship('Impresora', backref='modelo', lazy=True)