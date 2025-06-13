from flask import Blueprint, render_template, jsonify, request, send_file
from models import db, Sede, UnidadOrganizativa, Area, StockUbicacion, Insumo, TipoProducto, Marca, Modelo
from sqlalchemy import func
import pandas as pd
from fpdf import FPDF
import tempfile
import os
from datetime import datetime
from io import BytesIO

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reportes/inventario-area')
def inventario_area_view():
    """Renderiza la vista del reporte de inventario por área"""
    sedes_query = Sede.query.all()
    # Convertir objetos Sede a diccionarios serializables
    sedes = [serialize_model(sede) for sede in Sede.query.all()]
    return render_template('reportes/inventario_area.html', sedes=sedes)

@reports_bp.route('/api/reportes/inventario-area')
def inventario_area_data():
    """Devuelve los datos del reporte de inventario por área en formato JSON"""
    # Obtener parámetros de filtro
    sede_id = request.args.get('sede_id', type=int)
    unidad_id = request.args.get('unidad_id', type=int)
    area_id = request.args.get('area_id', type=int)
    
    # Construir la consulta base con las relaciones adicionales y CORREGIR los campos de join
    query = db.session.query(
        StockUbicacion,
        Insumo,
        TipoProducto,
        Marca,
        Modelo,
        Area,
        UnidadOrganizativa,
        Sede
    ).join(
        Insumo, StockUbicacion.insumo_id == Insumo.id
    ).join(
        TipoProducto, Insumo.tipo_id == TipoProducto.id  # Corregido: tipo_id en lugar de tipo_producto_id
    ).join(
        Marca, Insumo.marca_id == Marca.id, isouter=True
    ).join(
        Modelo, Insumo.modelo_id == Modelo.id, isouter=True
    ).join(
        Area, StockUbicacion.area_id == Area.id
    ).join(
        UnidadOrganizativa, Area.unidad_organizativa_id == UnidadOrganizativa.id
    ).join(
        Sede, UnidadOrganizativa.sede_id == Sede.id
    ).filter(
        StockUbicacion.cantidad > 0  # Solo mostrar stock positivo
    )
    
    # Aplicar filtros si están presentes
    if sede_id:
        query = query.filter(Sede.id == sede_id)
    if unidad_id:
        query = query.filter(UnidadOrganizativa.id == unidad_id)
    if area_id:
        query = query.filter(Area.id == area_id)
    
    # Ejecutar la consulta
    results = query.all()
    
    # Formatear los resultados con los valores adicionales
    inventario = []
    for stock, insumo, tipo, marca, modelo, area, unidad, sede in results:
        inventario.append({
            'stock_id': stock.id,
            'insumo_id': insumo.id,
            'insumo_nombre': insumo.nombre_completo,
            # Agregar los campos desglosados
            'tipo_id': tipo.id,
            'tipo_nombre': tipo.nombre,
            'marca_id': marca.id if marca else None,
            'marca_nombre': marca.nombre if marca else "Sin marca",
            'modelo_id': modelo.id if modelo else None,
            'modelo_nombre': modelo.nombre if modelo else "Sin modelo",
            'cantidad': stock.cantidad,
            'codigo': stock.codigo if insumo.inventariable else "No inventariable",
            'estado': stock.estado,
            'area_id': area.id,
            'area_nombre': area.nombre,
            'unidad_id': unidad.id,
            'unidad_nombre': unidad.nombre,
            'sede_id': sede.id,
            'sede_nombre': sede.nombre,
            'es_deposito': area.es_deposito,
            'fecha_imputacion': stock.fecha_imputacion.strftime('%d/%m/%Y'),
            'ultimo_movimiento': stock.ultimo_movimiento.strftime('%d/%m/%Y')
        })
    
    return jsonify(inventario)

@reports_bp.route('/api/reportes/unidades-por-sede/<int:sede_id>')
def unidades_por_unidad(sede_id):
    """Devuelve las unidades organizativas de una sede específica"""
    unidades = UnidadOrganizativa.query.filter_by(sede_id=sede_id).all()
    # Ya está devolviendo una lista de diccionarios, así que es correcto
    return jsonify([{'id': u.id, 'nombre': u.nombre} for u in unidades])

@reports_bp.route('/api/reportes/areas-por-unidad/<int:unidad_id>')
def areas_por_unidad(unidad_id):
    """Devuelve las áreas de una unidad organizativa específica"""
    areas = Area.query.filter_by(unidad_organizativa_id=unidad_id).all()
    return jsonify([{'id': a.id, 'nombre': a.nombre, 'es_deposito': a.es_deposito} for a in areas])

@reports_bp.route('/api/reportes/exportar-inventario-area')
def exportar_inventario_area():
    """Exporta el reporte de inventario por área en el formato solicitado"""
    formato = request.args.get('formato', 'excel')
    
    # Obtener los mismos datos que en la API
    sede_id = request.args.get('sede_id', type=int)
    unidad_id = request.args.get('unidad_id', type=int)
    area_id = request.args.get('area_id', type=int)
    
    # Construir la consulta con las relaciones adicionales
    query = db.session.query(
        StockUbicacion,
        Insumo,
        TipoProducto,
        Marca,
        Modelo,
        Area,
        UnidadOrganizativa,
        Sede
    ).join(
        Insumo, StockUbicacion.insumo_id == Insumo.id
    ).join(
        TipoProducto, Insumo.tipo_id == TipoProducto.id  # Corregido: tipo_id en lugar de tipo_producto_id
    ).join(
        Marca, Insumo.marca_id == Marca.id, isouter=True
    ).join(
        Modelo, Insumo.modelo_id == Modelo.id, isouter=True
    ).join(
        Area, StockUbicacion.area_id == Area.id
    ).join(
        UnidadOrganizativa, Area.unidad_organizativa_id == UnidadOrganizativa.id
    ).join(
        Sede, UnidadOrganizativa.sede_id == Sede.id
    ).filter(
        StockUbicacion.cantidad > 0
    )
    
    # Aplicar filtros
    if sede_id:
        query = query.filter(Sede.id == sede_id)
    if unidad_id:
        query = query.filter(UnidadOrganizativa.id == unidad_id)
    if area_id:
        query = query.filter(Area.id == area_id)
    
    # Ejecutar consulta
    results = query.all()
    
    # Preparar los datos para exportar con los campos desglosados
    data = []
    for stock, insumo, tipo, marca, modelo, area, unidad, sede in results:
        data.append({
            'Sede': sede.nombre,
            'Unidad Organizativa': unidad.nombre,
            'Área': area.nombre,
            'Es Depósito': 'Sí' if area.es_deposito else 'No',
            'Tipo': tipo.nombre,
            'Marca': marca.nombre if marca else "Sin marca",
            'Modelo': modelo.nombre if modelo else "Sin modelo",
            'Producto': insumo.nombre_completo,
            'Código': stock.codigo if insumo.inventariable else "No inventariable",
            'Cantidad': stock.cantidad,
            'Estado': stock.estado,
            'Fecha Imputación': stock.fecha_imputacion.strftime('%d/%m/%Y'),
            'Último Movimiento': stock.ultimo_movimiento.strftime('%d/%m/%Y')
        })
    
    # Crear DataFrame de pandas
    df = pd.DataFrame(data)
    
    # Generar título del archivo
    titulo = "Inventario"
    if area_id:
        area = Area.query.get(area_id)
        titulo += f" - {area.nombre}"
    elif unidad_id:
        unidad = UnidadOrganizativa.query.get(unidad_id)
        titulo += f" - {unidad.nombre}"
    elif sede_id:
        sede = Sede.query.get(sede_id)
        titulo += f" - {sede.nombre}"
    
    fecha_actual = datetime.now().strftime('%d%m%Y_%H%M%S')
    
    if formato == 'excel':
        # Exportar a Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Inventario', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Inventario']
            
            # Formato para el encabezado
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#0047AB',  # Azul UCC
                'font_color': 'white',
                'border': 1
            })
            
            # Aplicar formato al encabezado
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, len(str(value)) + 5)
            
        output.seek(0)
        return send_file(
            output, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{titulo}_{fecha_actual}.xlsx'
        )
    
    elif formato == 'pdf':
        # Crear una instancia de FPDF
        class PDF(FPDF):
            def header(self):
                # Logo (si existe)
                try:
                    logo_path = os.path.join(os.path.dirname(__file__), 'static', 'img', 'ucc_logo.png')
                    if os.path.exists(logo_path):
                        self.image(logo_path, 10, 8, 33)
                except:
                    pass
                    
                # Fuente y color para el título
                self.set_font('Arial', 'B', 16)
                self.set_text_color(0, 71, 171)  # Azul UCC (RGB)
                
                # Título del reporte
                self.cell(0, 10, titulo, 0, 1, 'C')
                
                # Fecha de generación
                self.set_font('Arial', 'I', 10)
                self.set_text_color(100, 100, 100)
                self.cell(0, 10, f'Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C')
                
                # Línea de separación
                self.ln(5)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(5)
            
            def footer(self):
                # Posición a 1.5 cm del final
                self.set_y(-15)
                # Fuente y color
                self.set_font('Arial', 'I', 8)
                self.set_text_color(128, 128, 128)
                # Número de página
                self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')
        
        # Crear el PDF
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Configurar la tabla
        pdf.set_font('Arial', 'B', 10)
        
        # Colores para el encabezado de la tabla
        pdf.set_fill_color(0, 71, 171)  # Azul UCC
        pdf.set_text_color(255, 255, 255)  # Texto blanco
        
        # Columnas y anchos
        columns = list(df.columns)
        col_widths = [30, 30, 25, 15, 35, 20, 15, 20, 20, 20]
        if len(col_widths) < len(columns):
            # Si faltan anchos, usar un valor predeterminado para el resto
            col_widths += [20] * (len(columns) - len(col_widths))
        
        # Encabezados de la tabla
        for i, column in enumerate(columns):
            pdf.cell(col_widths[i], 10, column, 1, 0, 'C', True)
        pdf.ln()
        
        # Datos de la tabla
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(0, 0, 0)  # Texto negro
        
        # Alternar colores de fondo para filas
        alt_color = False
        
        for _, row in df.iterrows():
            if alt_color:
                pdf.set_fill_color(240, 240, 240)  # Gris claro
            else:
                pdf.set_fill_color(255, 255, 255)  # Blanco
            
            alt_color = not alt_color
            
            # Verificar si necesitamos una nueva página por la altura
            height_needed = 6  # altura estimada de la fila
            if pdf.get_y() + height_needed > pdf.page_break_trigger:
                pdf.add_page()
                
                # Volver a imprimir los encabezados
                pdf.set_font('Arial', 'B', 10)
                pdf.set_fill_color(0, 71, 171)
                pdf.set_text_color(255, 255, 255)
                
                for i, column in enumerate(columns):
                    pdf.cell(col_widths[i], 10, column, 1, 0, 'C', True)
                pdf.ln()
                
                pdf.set_font('Arial', '', 8)
                pdf.set_text_color(0, 0, 0)
            
            # Imprimir los datos de la fila
            for i, column in enumerate(columns):
                value = str(row[column])
                # Truncar texto si es muy largo
                if len(value) > 28:
                    value = value[:25] + '...'
                pdf.cell(col_widths[i], 6, value, 1, 0, 'L', True)
            pdf.ln()
        
        # Guardar el PDF en memoria
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        
        return send_file(
            pdf_output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{titulo}_{fecha_actual}.pdf'
        )
    
    else:
        return jsonify({'error': 'Formato no soportado'}), 400

def serialize_model(model, exclude=None):
    """Serializa un modelo SQLAlchemy a un diccionario"""
    if exclude is None:
        exclude = []
    
    result = {}
    for key in model.__table__.columns.keys():
        if key not in exclude:
            result[key] = getattr(model, key)
    return result