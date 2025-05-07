# Documentación API de Unidades Organizativas

## Descripción General
API para gestionar unidades organizativas dentro del sistema. Permite listar, crear y obtener detalles de unidades organizativas.

## Endpoints

### Listar Unidades
**GET** `/api/unidades`

Retorna todas las unidades organizativas del sistema.

#### Respuesta
```json
[
    {
        "id": 1,
        "nombre": "Administración",
        "sede_id": 1
    }
]
```

### Obtener Unidad Específica
**GET** `/api/unidades/<unidad_id>`

Retorna los detalles de una unidad organizativa específica.

#### Parámetros URL
- `unidad_id`: ID de la unidad organizativa (entero)

#### Respuesta
```json
{
    "id": 1,
    "nombre": "Administración",
    "sede_id": 1
}
```

#### Códigos de respuesta
- `200`: Éxito
- `404`: Unidad no encontrada

### Crear Nueva Unidad
**POST** `/api/add_unidad`

Crea una nueva unidad organizativa.

#### Cuerpo de la Petición
Acepta tanto JSON como form-data:
```json
{
    "nombre": "Nueva Unidad",
    "sede_id": 1
}
```

#### Parámetros
- `nombre`: Nombre de la unidad (string, requerido)
- `sede_id`: ID de la sede (integer, requerido)

#### Respuesta Exitosa (201 Created)
```json
{
    "mensaje": "Unidad organizativa agregada exitosamente.",
    "id": 1
}
```

#### Códigos de Error
- `400`: Campos requeridos faltantes
- `404`: Sede no encontrada
- `409`: Unidad ya existe en la sede

## Notas de Implementación
- La API soporta tanto respuestas JSON como redirecciones web
- Incluye validación de datos y manejo de errores
- Verifica la existencia de la sede antes de crear una unidad
- Previene duplicados en la misma sede

## Uso de ejemplo
```bash
# Listar todas las unidades
curl -X GET http://localhost:5000/api/unidades

# Obtener una unidad específica
curl -X GET http://localhost:5000/api/unidades/1

# Crear una nueva unidad
curl -X POST http://localhost:5000/api/add_unidad \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Nueva Unidad","sede_id":1}'
```