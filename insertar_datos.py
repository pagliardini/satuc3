from models import db, Marca, Modelo, TipoProducto, Sede, Area, UnidadOrganizativa
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
        "Ugreen", "Western Digital"
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
    modelos = {
    "HP": [
        "LaserJet Pro", "DeskJet", "OfficeJet", "Envy", "Pavilion", "Omen", "EliteBook", "Spectre", "X360", "ProBook",
        "PageWide", "DesignJet", "Color LaserJet", "LaserJet Enterprise", "LaserJet MFP", "HP 200", "HP 400",
        "HP LaserJet M", "HP DeskJet Plus", "HP All-in-One", "HP LaserJet Pro MFP", "HP Color LaserJet Pro", "HP Smart Tank",
        "HP Neverstop", "HP LaserJet Pro M15", "HP LaserJet Pro M28", "HP OfficeJet Pro 9015", "HP OfficeJet Pro 8025",
        "HP LaserJet 100", "HP Smart Ink", "HP Tango", "HP PageWide Pro", "HP Ink Tank", "HP InkJet", "HP LaserJet Enterprise MFP",
        "HP OfficeJet 200", "HP OfficeJet 250", "HP DesignJet T730", "HP DesignJet T830", "HP DesignJet T650", "HP DesignJet T1600",
        "HP Envy Inspire", "HP EliteDesk", "HP Spectre x360 Convertible", "HP Chromebook", "HP Pavilion x360", "HP Envy x360",
        "HP Spectre Folio", "HP EliteOne", "HP TouchSmart", "HP DeskJet Ink Advantage", "HP LaserJet Pro P1102", "HP LaserJet Pro MFP M130",
        "HP PageWide Pro 477dw", "HP LaserJet Pro MFP M281fdw", "HP LaserJet Pro M255dw", "HP OfficeJet 8012",
        "HP OfficeJet 3830", "HP LaserJet Pro M404n", "HP LaserJet MFP M428fdw", "HP Tango X", "HP OfficeJet 250 All-in-One",
        "HP LaserJet 107w", "HP LaserJet MFP M479fdw", "HP LaserJet Pro M406dn"],
        "Epson": ["EcoTank", "WorkForce", "Expression"],
        "Canon": ["PIXMA", "imageCLASS", "MAXIFY"],
        "Brother": ["HL-L2350DW", "MFC-L2710DW", "DCP-T720DW"],
        "Samsung": ["ProXpress", "MultiXpress", "CLP-680"],
        "Xerox": ["VersaLink", "WorkCentre", "AltaLink"]
    }

    with app.app_context():
        for marca_nombre, modelos_lista in modelos.items():
            marca = Marca.query.filter_by(nombre=marca_nombre).first()
            if not marca:
                print(f"La marca '{marca_nombre}' no existe. No se pueden agregar modelos.")
                continue

            for modelo_nombre in modelos_lista:
                existing_modelo = Modelo.query.filter_by(nombre=modelo_nombre, marca_id=marca.id).first()
                if not existing_modelo:
                    nuevo_modelo = Modelo(nombre=modelo_nombre, marca_id=marca.id)
                    db.session.add(nuevo_modelo)
                    print(f"Modelo '{modelo_nombre}' agregado a la marca '{marca_nombre}'.")
                else:
                    print(f"El modelo '{modelo_nombre}' ya existe para la marca '{marca_nombre}'.")

        db.session.commit()

def insertar_tipos():
    tipos = ["Impresora", "UPS", "Notebook", "PC", "Insumos"]

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

if __name__ == '__main__':
    insertar_marcas()
    insertar_modelos()
    insertar_tipos()
    insertar_sedes_unidades_y_areas()
