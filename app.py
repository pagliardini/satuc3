from flask import Flask, render_template
from models import db  # Importar db desde models.py
from impresoras import impresoras_bp
from insumos import insumos_bp
from ups import ups_bp

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db con la aplicación Flask
db.init_app(app)

# Registrar blueprints
app.register_blueprint(impresoras_bp)
app.register_blueprint(insumos_bp)
app.register_blueprint(ups_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True)