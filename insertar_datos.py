from models import db, Marca, Modelo, TipoProducto, Sede, Area, UnidadOrganizativa, Producto
from app import app
from sqlalchemy import text

def insertar_marcas():
    marcas = [
        "HP", "Epson", "Canon", "Brother", "Samsung", "Xerox", "Lexmark", "Ricoh",
        "Kyocera", "Pantum", "OKI", "Sharp", "Dell", "Pekoko", "Prusa", "Creality",
        "Bambu Lab", "Elegoo", "Formlabs", "Konica Minolta",
        "Asus", "Behringer", "Cromax", "Energizer", "Genius", "Gigabyte",
        "Global", "HDC", "Intelaid", "Kingston", "Lenovo", "LG", "Logitech",
        "Magnum Tech", "Microsoft", "MSI", "Netmak", "Nisuta", "Noga", "Performance",
        "Seisa", "Sennheiser", "Soundcraft", "Suono", "TP-Link", "Trust", "TRV",
        "Ugreen", "Western Digital", "Genérico", "Sin Marca", "Nvidia", "AMD",
    ]

    with app.app_context():
        for marca in marcas:
            existing_marca = Marca.query.filter_by(nombre=marca).first()
            if not existing_marca:
                nueva_marca = Marca(nombre=marca)
                db.session.add(nueva_marca)
                print(f"Marca '{marca}' insertada correctamente.")
            else:
                print(f"La marca '{marca}' ya existe.")

        db.session.commit()

def insertar_modelos():
    modelos_lista = [
        # HP Printers
        "Color Laser 150a", "Color Laser 150nw", "Color Laser MFP 178nw",
        # ...existing HP models...
        "LaserJet Pro MFP M428fdn (W1A29A)",
        
        # Epson
        "EcoTank", "WorkForce", "Expression", "SureColor", "L-Series",
        
        # Lexmark
        "B2236dw", "MB2236adw", "C3224dw", "C3326dw", "C3326adw",
        
        # Canon
        "PIXMA", "imageCLASS", "MAXIFY", "imagePROGRAF", "SELPHY",
        
        # Ricoh
        "SP C261DNW", "SP C360DNW", "SP C440DNW", "MP C307", "MP C4504",
        
        # Brother
        "HL-L2350DW", "MFC-L2710DW", "DCP-T720DW",
        
        # Samsung
        "ProXpress", "MultiXpress", "CLP-680",
        
        # Xerox
        "VersaLink", "WorkCentre", "AltaLink",
        
        # Nvidia
        "GT 710", "GT 730", "GT 1030", "GTX 750 Ti", "GTX 1050", "GTX 1050 Ti",
        "GTX 1060", "GTX 1070", "GTX 1080", "GTX 1650", "GTX 1660", "GTX 1660 Ti",
        "RTX 2060", "RTX 2070", "RTX 2080", "RTX 3060", "RTX 3070", "RTX 3080",
        "RTX 3090", "RTX 4060", "RTX 4070", "RTX 4080", "RTX 4090"
    ]

    with app.app_context():
        for modelo_nombre in modelos_lista:
            existing_modelo = Modelo.query.filter_by(nombre=modelo_nombre).first()
            if not existing_modelo:
                nuevo_modelo = Modelo(nombre=modelo_nombre)
                db.session.add(nuevo_modelo)
                print(f"Modelo '{modelo_nombre}' agregado.")
            else:
                print(f"El modelo '{modelo_nombre}' ya existe.")

        db.session.commit()

def insertar_tipos():
    tipos = [
    "Impresora", "UPS", "Notebook", "PC", "Insumos",
    "Monitor", "Teclado", "Mouse", "Combo (Mouse + Teclado)", 
    "Parlantes", "Auriculares", "Webcam", "Pad Mouse",
    "Pilas", "Baterías", "Cargador", "Fuente de PC",
    "Cartucho", "Proyector", "Pantalla de proyección",
    "Adaptador", "Extensor USB", "Cable HDMI", "Cable VGA",
    "Cable Power", "Patchcord / Cable de red", "Hub / Dock USB",
    "Puntero Láser", "Placa de Video", "Placa WiFi",
    "Memoria RAM", "Disco SSD", "Disco HDD", "Zapatilla",
    "Licencia / Software", "Herramienta / Accesorio"
]

    with app.app_context():
        for tipo_nombre in tipos:
            existing_tipo = TipoProducto.query.filter_by(nombre=tipo_nombre).first()
            if not existing_tipo:
                nuevo_tipo = TipoProducto(nombre=tipo_nombre)
                db.session.add(nuevo_tipo)
                print(f"Tipo de producto '{tipo_nombre}' insertado correctamente.")
            else:
                print(f"El tipo de producto '{tipo_nombre}' ya existe.")

        db.session.commit()

def insertar_sedes_unidades_y_areas():
    sedes_y_datos = {
        "Campus": {
            "Administración": ["Recursos Humanos", "Finanzas"],
            "Laboratorio": ["Química", "Física"],
            "Biblioteca": ["Lectura", "Archivo"],
            "Aulas": ["Aula 1", "Aula 2"]
        },
        "Trejo": {
            "Recepción": ["Atención al Cliente"],
            "Contabilidad": ["Pagos", "Cobros"],
            "Investigación": ["Proyectos", "Publicaciones"],
            "Salas de Reunión": ["Sala 1", "Sala 2"]
        },
        "Medicina": {
            "Consultorios": ["Pediatría", "Cardiología"],
            "Laboratorio Clínico": ["Hematología", "Microbiología"],
            "Farmacia": ["Medicamentos", "Control"],
            "Aulas": ["Aula 1", "Aula 2"]
        },
        "Río IV": {
            "Oficinas": ["Administración", "Soporte Técnico"],
            "Laboratorio de Física": ["Mecánica", "Óptica"],
            "Biblioteca": ["Lectura", "Archivo"],
            "Aulas": ["Aula 1", "Aula 2"]
        }
    }

    with app.app_context():
        for sede_nombre, unidades in sedes_y_datos.items():
            # Insertar sede
            sede = Sede.query.filter_by(nombre=sede_nombre).first()
            if not sede:
                sede = Sede(nombre=sede_nombre)
                db.session.add(sede)
                db.session.commit()
                print(f"Sede '{sede_nombre}' insertada correctamente.")

            for unidad_nombre, areas in unidades.items():
                # Insertar unidad organizativa
                unidad = UnidadOrganizativa.query.filter_by(nombre=unidad_nombre, sede_id=sede.id).first()
                if not unidad:
                    unidad = UnidadOrganizativa(nombre=unidad_nombre, sede_id=sede.id)
                    db.session.add(unidad)
                    db.session.commit()
                    print(f"Unidad Organizativa '{unidad_nombre}' insertada en la sede '{sede_nombre}'.")

                for area_nombre in areas:
                    # Insertar área
                    area = Area.query.filter_by(nombre=area_nombre, unidad_organizativa_id=unidad.id).first()
                    if not area:
                        area = Area(nombre=area_nombre, unidad_organizativa_id=unidad.id)
                        db.session.add(area)
                        print(f"Área '{area_nombre}' insertada en la Unidad Organizativa '{unidad_nombre}'.")
                    else:
                        print(f"El área '{area_nombre}' ya existe en la Unidad Organizativa '{unidad_nombre}'.")

        db.session.commit()

def insertar_productos():
    from random import choice, randint

    with app.app_context():
        tipos = TipoProducto.query.all()
        marcas = Marca.query.all()
        modelos = Modelo.query.all()

        if not (tipos and marcas and modelos):
            print("Faltan tipos, marcas o modelos para crear productos.")
            return

        for i in range(20):
            tipo = choice(tipos)
            marca = choice(marcas)
            modelo = choice(modelos)

            producto = Producto(
                tipo_id=tipo.id,
                marca_id=marca.id,
                modelo_id=modelo.id,
                descripcion=f"Producto de prueba {i + 1}",
                activo=True,
                inventariable=bool(randint(0, 1))
            )
            db.session.add(producto)
            print(f"Producto {i + 1} agregado: {producto.descripcion} ({marca.nombre} {modelo.nombre})")

        db.session.commit()
        print("Inserción de productos completada.")


if __name__ == '__main__':
    insertar_marcas()
    insertar_modelos()
    insertar_tipos()
    insertar_sedes_unidades_y_areas()
    insertar_productos()
