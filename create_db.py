from app import app
from models import db

with app.app_context():
    db.create_all()
    print("Base de datos creada con éxito.")