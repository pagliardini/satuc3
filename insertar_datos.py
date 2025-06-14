from models import db, Marca, Modelo, TipoProducto, Sede, Area, UnidadOrganizativa
from app import app
from sqlalchemy import text
from models import Insumo
from models import Toner
from models import User

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
    modelos_por_marca = {
        "HP": [
            "P1102w", "p2035", "p1006", "M1132", "1212", "2055", "2600", "2014N", "1320",
            "P3005", "1022", "1020", "M1120", "P2030", "1005", "2100", "P4014", "400",
            "1606", "5200", "2410", "1018", "1505", "1015", "1025", "1160", "1200",
            "OTRA", "M127FN", "5", "1150", "5000", "M201", "M401N", "1000", "DESKJET 3545",
            "100 MFP", "M175A", "7110", "MFP M426FDW", "MF130", "M402", "M102W", "1100",
            "M203", "NEVSTOP 1000w", "M428FDW", "MFP 137FNW", "107W", "M203DW", "M402DNE", "107A",
            "Color Laser 150a", "Color Laser 150nw", "Color Laser MFP 178nw",
            "LaserJet Pro MFP M428fdn (W1A29A)"
        ],
        "Epson": [
            "EcoTank", "WorkForce", "L3250", "L575", "L3110", "L8180"
        ],
        "Lexmark": [
            "B2236dw", "MB2236adw", "C3224dw", "C3326dw", "C3326adw"
        ],
        "Canon": [
            "PIXMA", "imageCLASS", "MAXIFY", "imagePROGRAF", "SELPHY"
        ],
        "Ricoh": [
            "SP C261DNW", "SP C360DNW", "SP C440DNW", "MP C307", "MP C4504", "MC251FW", "M250FW"
        ],
        "Brother": [
            "HL-L2350DW", "MFC-L2710DW", "DCP-T720DW", "DCP-7065DN", "DCP-T220"
        ],
        "Samsung": [
            "M2070FW", "M2020W", "M2880"
        ],
        "Minolta": [
            "MINOLTA MAGIC", "bizhub C308", "bizhub C368", "bizhub 227"
        ],
        "Xerox": [
            "VersaLink", "WorkCentre", "AltaLink"
        ],
        "Evolis": [
            "Primacy", "Zenius", "Quantum", "Kiosk", "Avansia"
        ],
        "Nvidia": [
            "GT 710", "GT 730", "GT 1030", "GTX 750 Ti", "GTX 1050", "GTX 1050 Ti",
            "GTX 1060", "GTX 1070", "GTX 1080", "GTX 1650", "GTX 1660", "GTX 1660 Ti",
            "RTX 2060", "RTX 2070", "RTX 2080", "RTX 3060", "RTX 3070", "RTX 3080",
            "RTX 3090", "RTX 4060", "RTX 4070", "RTX 4080", "RTX 4090"
        ]
}

    with app.app_context():
        for marca_nombre, modelos in modelos_por_marca.items():
            # Buscar la marca en la base de datos
            marca = Marca.query.filter_by(nombre=marca_nombre).first()
            if not marca:
                print(f"Error: La marca '{marca_nombre}' no existe en la base de datos.")
                continue

            for modelo_nombre in modelos:
                existing_modelo = Modelo.query.filter_by(nombre=modelo_nombre).first()
                if not existing_modelo:
                    nuevo_modelo = Modelo(nombre=modelo_nombre, marca_id=marca.id)
                    db.session.add(nuevo_modelo)
                    print(f"Modelo '{modelo_nombre}' agregado para marca '{marca_nombre}'.")
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

def insertar_toners():
            toners = [
                "12A",
                "85A",
                "78A",
                "CF244A",
                "CF217A",
                "05A",
                "30A",
                "58A",
                "83A",
                "80A",
                "105A",
                "DRUM CE314A",
                "26A",
                "58A sin chip",
                "16A",
                "49A",
                "D111S",
                "D115",
                "17A con chip",
                "35A",
                "Tinta HP 933xl Magenta",
                "MC250H (CYAN Y NEGRO)",
                "D115L",
                "MC250H (CYAN)"
            ]

            with app.app_context():
                for nombre in toners:
                    existente = Toner.query.filter_by(nombre=nombre).first()
                    if not existente:
                        toner = Toner(nombre=nombre)
                        db.session.add(toner)
                        print(f"Toner '{nombre}' insertado correctamente.")
                    else:
                        print(f"El toner '{nombre}' ya existe.")
                db.session.commit()

def insertar_insumos():
    """
    Inserta insumos de ejemplo según el modelo Insumo definido en models.py.
    Relaciona insumos con tipo, marca y modelo existentes.
    """
    insumos = [
        # (tipo, marca, modelo, descripcion, toner_id, bateria_id, url_imagen)
        ("Impresora", "HP", "Color Laser 150a", "Impresora láser color", 1, None, None),
        ("Impresora", "Epson", "EcoTank", "Impresora tanque de tinta", None, None, None),
        ("Placa de Video", "Nvidia", "RTX 3060", "Placa de video dedicada", None, None, None),
        ("Notebook", "Lenovo", "ThinkPad", "Notebook empresarial", None, None, None),
        ("Monitor", "LG", "UltraWide", "Monitor panorámico", None, None, None),
        ("UPS", "Energizer", "Energizer 1200VA", "UPS de respaldo", None, None, None),
    ]


    with app.app_context():
        for tipo_nombre, marca_nombre, modelo_nombre, descripcion, toner_id, bateria_id, url_imagen in insumos:
            tipo = TipoProducto.query.filter_by(nombre=tipo_nombre).first()
            marca = Marca.query.filter_by(nombre=marca_nombre).first()
            modelo = Modelo.query.filter_by(nombre=modelo_nombre).first()
            if not (tipo and marca and modelo):
                print(f"Insumo omitido: {tipo_nombre}, {marca_nombre}, {modelo_nombre} (faltan datos)")
                continue

            existente = Insumo.query.filter_by(
                tipo_id=tipo.id,
                marca_id=marca.id,
                modelo_id=modelo.id,
                descripcion=descripcion
            ).first()
            if existente:
                print(f"Insumo ya existe: {descripcion} ({tipo_nombre}, {marca_nombre}, {modelo_nombre})")
                continue

            insumo = Insumo(
                tipo_id=tipo.id,
                marca_id=marca.id,
                modelo_id=modelo.id,
                descripcion=descripcion,
                toner_id=toner_id,
                bateria_id=bateria_id,
                url_imagen=url_imagen
            )
            db.session.add(insumo)
            print(f"Insumo insertado: {descripcion} ({tipo_nombre}, {marca_nombre}, {modelo_nombre})")
        db.session.commit()

def insertar_usuarios():
    """
    Inserta usuarios de ejemplo según el modelo User definido en models.py.
    """
    usuarios = [
        ("admin", "admin123", "admin"),
        ("user1", "user123", "general"),
        ("user2", "user123", "general"),
        ("user3", "user123", "general"),
    ]
    with app.app_context():
        for username, password, role in usuarios:
            existente = User.query.filter_by(username=username).first()
            if existente:
                print(f"Usuario '{username}' ya existe.")
                continue

            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            print(f"Usuario '{username}' insertado correctamente.")

        db.session.commit()
if __name__ == '__main__':
    insertar_marcas()
    insertar_modelos()
    insertar_tipos()
    insertar_sedes_unidades_y_areas()
    insertar_insumos()
    insertar_toners()
    insertar_usuarios()