from flask import Flask, render_template
from models import db
from productos import productos_bp
from lugares import lugares_bp
from mtm import mtm_bp  # Importar el nuevo blueprint

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db con la aplicación Flask
db.init_app(app)

# Registrar blueprints
app.register_blueprint(productos_bp)
app.register_blueprint(lugares_bp)
app.register_blueprint(mtm_bp)  # Registrar el blueprint de mtm

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)