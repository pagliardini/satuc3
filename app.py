from flask import Flask, render_template
from impresoras import impresoras_bp  # Importar el blueprint
from insumos import insumos_bp
from ups import ups_bp

app = Flask(__name__)

app.register_blueprint(impresoras_bp)
app.register_blueprint(insumos_bp)
app.register_blueprint(ups_bp)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)