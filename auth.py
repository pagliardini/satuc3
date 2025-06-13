# auth.py

import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User  # Importa tu instancia de db de tu app principal

# Configuración
SECRET_KEY = 'tu_clave_secreta_super_segura'  # En producción, usar variable de entorno

auth_bp = Blueprint('auth', __name__)

# Decoradores de autenticación
def require_auth(f):
    """
    Decorador que requiere autenticación válida (cualquier usuario autenticado)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({'error': 'Token de autorización requerido'}), 401
            
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            # Verificar que el usuario existe
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
            
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'error': 'Error de autenticación'}), 401
    
    return decorated_function

def require_role(required_role):
    """
    Decorador que requiere un rol específico
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith("Bearer "):
                    return jsonify({'error': 'Token de autorización requerido'}), 401
                
                token = auth_header.split(" ")[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                
                # Verificar que el usuario existe
                user = User.query.get(payload['user_id'])
                if not user:
                    return jsonify({'error': 'Usuario no encontrado'}), 401
                
                # Verificar el rol
                if user.role != required_role:
                    return jsonify({'error': 'Permisos insuficientes'}), 403
                
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido'}), 401
            except Exception as e:
                return jsonify({'error': 'Error de autenticación'}), 401
        
        return decorated_function
    return decorator

# --- Login y generación de token JWT ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username y password son requeridos'}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Crear token con información adicional
        payload = {
            'user_id': user.id,
            'username': user.username,  # NUEVO: Incluir username en el token
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=8)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

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

# Agregar esta función helper
def get_current_user():
    """Obtiene el usuario actual desde el token JWT"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        return User.query.get(payload['user_id'])
    except:
        return None

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint para logout (opcional, ya que JWT es stateless)
    Podrías usarlo para invalidar tokens en una blacklist si implementas esa funcionalidad
    """
    # Por ahora solo confirmamos el logout
    return jsonify({'message': 'Logout exitoso'}), 200

@auth_bp.route('/api/user/profile', methods=['GET'])
@require_auth  # Ahora debería funcionar
def get_user_profile():
    """Obtiene la información del usuario autenticado"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
