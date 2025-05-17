from flask import Flask, render_template, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
#from productos import productos_bp
from api.stock import stock_bp  
from api.sedes import sedes_bp
from api.areas import areas_bp
from api.unidades import unidades_bp
from api.tipos import tipos_bp
from api.marcas import marcas_bp
from api.modelos import modelos_bp


from doc import swagger_config
import os


app = Flask(__name__)
CORS(app)


### Swagger UI Configuration ###
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SATUCC3 API"
    }
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(stock_bp)
app.register_blueprint(sedes_bp)
app.register_blueprint(areas_bp)
app.register_blueprint(unidades_bp)
app.register_blueprint(marcas_bp) 
app.register_blueprint(modelos_bp)
app.register_blueprint(tipos_bp)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock')
def stock():
    return render_template('/stock/index.html')

@app.route(API_URL)
def serve_swagger():
    return jsonify(swagger_config)

if __name__ == '__main__':
    with app.app_context():
        print("Base de datos en uso:", os.path.abspath('database.db'))

        db.create_all()
    app.run(debug=True)