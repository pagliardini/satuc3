# auth.py

import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, g
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User  # Importa tu instancia de db de tu app principal

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = "satucc3-super-secreto"  # Reemplazalo por algo más seguro en producción

# --- Modelo de Usuario (si no lo tenés en otro archivo) ---
# Si ya tenés esto, no lo dupliques



# --- Login y generación de token JWT ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=8)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token})


# --- Decorador para proteger rutas según rol ---
def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({'error': 'Token requerido'}), 401
            try:
                token = auth_header.split(" ")[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                g.user_id = payload['user_id']
                g.user_role = payload['role']
                if payload['role'] not in allowed_roles:
                    return jsonify({'error': 'No autorizado'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido'}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator


# --- Ruta para crear usuario de prueba (solo para desarrollo) ---
@auth_bp.route('/crear_usuario_test', methods=['POST'])
def crear_usuario_test():
    data = request.json
    if not all(k in data for k in ('username', 'password', 'role')):
        return jsonify({'error': 'Faltan datos'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Usuario ya existe'}), 400

    user = User(username=data['username'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuario creado'}), 201
