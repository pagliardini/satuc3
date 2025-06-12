from flask import Blueprint, request, jsonify, g
from models import db, Sede, UnidadOrganizativa
from sqlalchemy.exc import IntegrityError
from auth import require_role

sedes_bp = Blueprint('sedes_api', __name__, url_prefix='/api')


@sedes_bp.route('/sedes', methods=['GET', 'POST'])
@require_role(['admin', 'user'])  # permite que ambos accedan, luego filtramos
def sedes():
    if request.method == 'POST':
        if g.user_role != 'admin':
            return jsonify({"success": False, "message": "No autorizado"}), 403

        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"success": False, "message": "El nombre es requerido"})
        
        try:
            sede = Sede(nombre=nombre)
            db.session.add(sede)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Sede creada correctamente",
                "sede": {"id": sede.id, "nombre": sede.nombre}
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
    
    # GET: permitido para admin y user
    sedes = Sede.query.all()
    return jsonify([{"id": s.id, "nombre": s.nombre} for s in sedes])

@sedes_bp.route('/sedes/<int:sede_id>/unidades', methods=['GET'])
def unidades_por_sede(sede_id):
    unidades = UnidadOrganizativa.query.filter_by(sede_id=sede_id).all()
    return jsonify([{"id": u.id, "nombre": u.nombre} for u in unidades])

@sedes_bp.route('/sedes/<int:sede_id>', methods=['PUT', 'DELETE'])
def sede_operations(sede_id):
    sede = Sede.query.get_or_404(sede_id)
    
    if request.method == 'DELETE':
        try:
            # Verificar si la sede tiene unidades asociadas
            if sede.unidades:
                return jsonify({
                    "success": False,
                    "message": "No se puede eliminar la sede porque tiene unidades asociadas"
                }), 400
                
            db.session.delete(sede)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Sede eliminada correctamente"
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Error al eliminar la sede: {str(e)}"
            }), 500
    
    # PUT method
    data = request.get_json()
    nombre = data.get('nombre')
    
    if not nombre:
        return jsonify({
            "success": False,
            "message": "El nombre es requerido"
        }), 400
    
    try:
        sede.nombre = nombre
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Sede actualizada correctamente",
            "sede": {
                "id": sede.id,
                "nombre": sede.nombre
            }
        })
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Ya existe una sede con ese nombre"
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error al actualizar la sede: {str(e)}"
        }), 500