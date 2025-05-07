swagger_config = {
    'openapi': '3.0.0',
    'info': {
        'title': 'SATUCC3 API',
        'version': '1.0.0',
        'description': 'Documentación de la API de SATUCC3.'
    },
    'servers': [
        {'url': '/api'}  # URL base de tu API (relativa)
    ],
    'tags': [
        {'name': 'Sedes', 'description': 'Operaciones relacionadas con las sedes.'},
        {'name': 'Unidades Organizativas', 'description': 'Operaciones relacionadas con las unidades organizativas.'}
    ],
    'paths': {
        '/sedes': {
            'get': {
                'tags': ['Sedes'],
                'summary': 'Obtener todas las sedes o crear una nueva sede.',
                'responses': {
                    '200': {'description': 'Lista de todas las sedes.'},
                    '201': {'description': 'Sede creada exitosamente.'},
                    '500': {'description': 'Error interno del servidor.'}
                }
            },
            'post': {
                'tags': ['Sedes'],
                'summary': 'Crear una nueva sede.',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'nombre': {'type': 'string', 'description': 'Nombre de la nueva sede.'}
                                },
                                'required': ['nombre']
                            }
                        }
                    }
                },
                'responses': {
                    '201': {'description': 'Sede creada exitosamente.'},
                    '400': {'description': 'Datos de entrada inválidos.'},
                    '500': {'description': 'Error interno del servidor.'}
                }
            }
        },
        '/sedes/{sede_id}/unidades': {
            'get': {
                'tags': ['Unidades Organizativas'],
                'summary': 'Obtener las unidades organizativas de una sede específica.',
                'parameters': [
                    {
                        'in': 'path',
                        'name': 'sede_id',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID de la sede.'
                    }
                ],
                'responses': {
                    '200': {'description': 'Lista de unidades organizativas.'},
                    '404': {'description': 'Sede no encontrada.'},
                    '500': {'description': 'Error interno del servidor.'}
                }
            }
        }
        # ... añade aquí la documentación para tus otros endpoints ...
    },
    'components': {  # Puedes definir esquemas reutilizables aquí
        'schemas': {
            'Sede': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único de la sede.'},
                    'nombre': {'type': 'string', 'description': 'Nombre de la sede.'}
                }
            }
            # ... define otros esquemas como NewSede, UnidadOrganizativa, ErrorResponse, etc. ...
        }
    }
}