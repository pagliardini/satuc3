from flask import Blueprint, request, jsonify
from models import db, Sede, UnidadOrganizativa

sedes_bp = Blueprint('sedes_api', __name__, url_prefix='/api')


@sedes_bp.route('/sedes', methods=['GET', 'POST'])
def sedes():
    if request.method == 'POST':
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
    
    sedes = Sede.query.all()
    return jsonify([{"id": s.id, "nombre": s.nombre} for s in sedes])

@sedes_bp.route('/sedes/<int:sede_id>/unidades', methods=['GET'])
def unidades_por_sede(sede_id):
    unidades = UnidadOrganizativa.query.filter_by(sede_id=sede_id).all()
    return jsonify([{"id": u.id, "nombre": u.nombre} for u in unidades])