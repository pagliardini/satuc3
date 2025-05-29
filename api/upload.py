from flask import Blueprint, request, jsonify, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

upload_bp = Blueprint('upload_api', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload/imagen', methods=['POST'])
def upload_imagen():
    """Subir imagen para insumo"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No se envió ningún archivo'}), 400
    
    file = request.files['file']
    categoria = request.form.get('categoria', 'otros')  # impresoras, ups, otros
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generar nombre único para el archivo
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            
            # Crear ruta de la carpeta según categoría
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'insumos', categoria)
            os.makedirs(upload_folder, exist_ok=True)
            
            # Guardar archivo
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # URL para acceder al archivo
            file_url = f"/uploads/insumos/{categoria}/{unique_filename}"
            
            return jsonify({
                'success': True,
                'message': 'Imagen subida correctamente',
                'url': file_url,
                'filename': unique_filename
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al subir archivo: {str(e)}'}), 500
    
    return jsonify({'success': False, 'message': 'Tipo de archivo no permitido'}), 400

@upload_bp.route('/upload/imagen/<filename>', methods=['DELETE'])
def delete_imagen(filename):
    """Eliminar imagen"""
    try:
        # Buscar el archivo en todas las subcarpetas
        for categoria in ['impresoras', 'ups', 'otros']:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'insumos', categoria, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return jsonify({'success': True, 'message': 'Imagen eliminada correctamente'}), 200
        
        return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al eliminar archivo: {str(e)}'}), 500