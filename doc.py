swagger_config = {
    'openapi': '3.0.0',
    'info': {
        'title': 'SATUCC3 API',
        'version': '1.0.0',
        'description': 'API para gestión de inventario y ubicaciones.'
    },
    'servers': [
        {'url': '/api'}
    ],
    'tags': [
        {'name': 'Sedes', 'description': 'Operaciones relacionadas con las sedes'},
        {'name': 'Unidades Organizativas', 'description': 'Gestión de unidades organizativas'},
        {'name': 'Áreas', 'description': 'Gestión de áreas dentro de unidades organizativas'},
        {'name': 'Productos', 'description': 'Gestión de productos'},
        {'name': 'Marcas', 'description': 'Gestión de marcas de productos'},
        {'name': 'Modelos', 'description': 'Gestión de modelos de productos'},
    ],
    'paths': {
        '/sedes': {
            'get': {
                'tags': ['Sedes'],
                'summary': 'Obtener todas las sedes',
                'responses': {
                    '200': {
                        'description': 'Lista de sedes',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'array',
                                    'items': {'$ref': '#/components/schemas/Sede'}
                                }
                            }
                        }
                    }
                }
            },
            'post': {
                'tags': ['Sedes'],
                'summary': 'Crear una nueva sede',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/SedeInput'}
                        }
                    }
                },
                'responses': {
                    '201': {'description': 'Sede creada exitosamente'},
                    '400': {'description': 'Datos inválidos'},
                    '500': {'description': 'Error del servidor'}
                }
            }
        },
        '/sedes/{sede_id}': {
            'put': {
                'tags': ['Sedes'],
                'summary': 'Actualizar una sede existente',
                'parameters': [
                    {
                        'name': 'sede_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID de la sede a actualizar'
                    }
                ],
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/SedeInput'}
                        }
                    }
                },
                'responses': {
                    '200': {
                        'description': 'Sede actualizada correctamente',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'success': {'type': 'boolean'},
                                        'message': {'type': 'string'},
                                        'sede': {'$ref': '#/components/schemas/Sede'}
                                    }
                                }
                            }
                        }
                    },
                    '400': {'description': 'El nombre es requerido'},
                    '404': {'description': 'Sede no encontrada'},
                    '409': {'description': 'Ya existe una sede con ese nombre'},
                    '500': {'description': 'Error del servidor'}
                }
            },
            'delete': {
                'tags': ['Sedes'],
                'summary': 'Eliminar una sede',
                'parameters': [
                    {
                        'name': 'sede_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID de la sede a eliminar'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Sede eliminada correctamente',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'success': {'type': 'boolean'},
                                        'message': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    },
                    '400': {'description': 'No se puede eliminar la sede porque tiene unidades asociadas'},
                    '404': {'description': 'Sede no encontrada'},
                    '500': {'description': 'Error del servidor'}
                }
            }
        },
        '/unidades': {
            'get': {
                'tags': ['Unidades Organizativas'],
                'summary': 'Obtener todas las unidades organizativas',
                'responses': {
                    '200': {
                        'description': 'Lista de unidades organizativas',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'array',
                                    'items': {'$ref': '#/components/schemas/UnidadOrganizativa'}
                                }
                            }
                        }
                    }
                }
            },
            'post': {
                'tags': ['Unidades Organizativas'],
                'summary': 'Crear una nueva unidad organizativa',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/UnidadInput'}
                        }
                    }
                },
                'responses': {
                    '201': {
                        'description': 'Unidad creada exitosamente',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'mensaje': {'type': 'string'},
                                        'unidad': {'$ref': '#/components/schemas/UnidadOrganizativa'}
                                    }
                                }
                            }
                        }
                    },
                    '400': {'description': 'Datos inválidos'},
                    '404': {'description': 'Sede no encontrada'},
                    '409': {'description': 'La unidad ya existe en la sede'},
                }
            }
        },
        '/unidades/{unidad_id}': {
            'get': {
                'tags': ['Unidades Organizativas'],
                'summary': 'Obtener una unidad organizativa específica',
                'parameters': [
                    {
                        'name': 'unidad_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID de la unidad organizativa'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Detalles de la unidad organizativa',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/UnidadOrganizativa'}
                            }
                        }
                    },
                    '404': {'description': 'Unidad no encontrada'}
                }
            }
        },
        '/productos': {
            'get': {
                'tags': ['Productos'],
                'summary': 'Obtener todos los productos',
                'responses': {
                    '200': {
                        'description': 'Lista de productos',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'array',
                                    'items': {'$ref': '#/components/schemas/Producto'}
                                }
                            }
                        }
                    }
                }
            }
        },
        '/marcas': {
    'get': {
        'tags': ['Marcas'],
        'summary': 'Obtener todas las marcas',
        'responses': {
            '200': {
                'description': 'Lista de marcas',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {'$ref': '#/components/schemas/Marca'}
                        }
                    }
                }
            }
        }
    },
    'post': {
        'tags': ['Marcas'],
        'summary': 'Crear una nueva marca',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/MarcaInput'}
                }
            }
        },
        'responses': {
            '201': {'description': 'Marca creada correctamente'},
            '400': {'description': 'El nombre es requerido'},
            '500': {'description': 'Error del servidor'}
        }
    }
},
'/marcas/{id}': {
    'put': {
        'tags': ['Marcas'],
        'summary': 'Actualizar una marca existente',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/MarcaInput'}
                }
            }
        },
        'responses': {
            '200': {'description': 'Marca actualizada correctamente'},
            '400': {'description': 'El nombre es requerido'},
            '500': {'description': 'Error del servidor'}
        }
    },
    'delete': {
        'tags': ['Marcas'],
        'summary': 'Eliminar una marca',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            '200': {'description': 'Marca eliminada correctamente'},
            '400': {'description': 'La marca tiene productos o modelos asociados y no puede eliminarse'},
            '500': {'description': 'Error del servidor'}
        }
    }
},
'/modelos': {
    'get': {
        'tags': ['Modelos'],
        'summary': 'Obtener todos los modelos',
        'responses': {
            '200': {
                'description': 'Lista de modelos',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {'$ref': '#/components/schemas/ModeloResponse'}
                        }
                    }
                }
            }
        }
    },
    'post': {
        'tags': ['Modelos'],
        'summary': 'Crear un nuevo modelo',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/ModeloInput'}
                }
            }
        },
        'responses': {
            '201': {
                'description': 'Modelo creado correctamente',
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/ModeloCreatedResponse'}
                    }
                }
            },
            '400': {'description': 'El nombre y marca_id son requeridos'},
            '404': {'description': 'La marca especificada no existe'},
            '500': {'description': 'Error del servidor'}
        }
    }
},
'/modelos/{id}': {
    'put': {
        'tags': ['Modelos'],
        'summary': 'Actualizar un modelo existente',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID del modelo'
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/ModeloInput'}
                }
            }
        },
        'responses': {
            '200': {
                'description': 'Modelo actualizado correctamente',
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/ModeloCreatedResponse'}
                    }
                }
            },
            '400': {'description': 'El nombre y marca_id son requeridos'},
            '404': {'description': 'Modelo o marca no encontrada'},
            '500': {'description': 'Error del servidor'}
        }
    },
    'delete': {
        'tags': ['Modelos'],
        'summary': 'Eliminar un modelo',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'ID del modelo'
            }
        ],
        'responses': {
            '200': {'description': 'Modelo eliminado correctamente'},
            '400': {'description': 'No se puede eliminar el modelo porque tiene productos asociados'},
            '404': {'description': 'Modelo no encontrado'},
            '500': {'description': 'Error del servidor'}
        }
    }
}

    },
    'components': {
        'schemas': {
            'Sede': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único de la sede'},
                    'nombre': {'type': 'string', 'description': 'Nombre de la sede'}
                }
            },
            'SedeInput': {
                'type': 'object',
                'required': ['nombre'],
                'properties': {
                    'nombre': {'type': 'string', 'description': 'Nombre de la sede'}
                }
            },
            'UnidadOrganizativa': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único de la unidad'},
                    'nombre': {'type': 'string', 'description': 'Nombre de la unidad'},
                    'sede_id': {'type': 'integer', 'description': 'ID de la sede a la que pertenece'}
                }
            },
            'UnidadInput': {
                'type': 'object',
                'required': ['nombre', 'sede_id'],
                'properties': {
                    'nombre': {'type': 'string', 'description': 'Nombre de la unidad'},
                    'sede_id': {'type': 'integer', 'description': 'ID de la sede'}
                }
            },
            'Producto': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único del producto'},
                    'tipo': {'type': 'string', 'description': 'Tipo de producto'},
                    'marca': {'type': 'string', 'description': 'Marca del producto'},
                    'modelo': {'type': 'string', 'description': 'Modelo del producto'},
                    'descripcion': {'type': 'string', 'description': 'Descripción del producto'},
                    'inventariable': {'type': 'boolean', 'description': 'Si el producto es inventariable'},
                    'activo': {'type': 'boolean', 'description': 'Si el producto está activo'},
                    'fecha_creacion': {'type': 'string', 'format': 'date-time', 'description': 'Fecha de creación'}
                }
            },
            'Marca': {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer', 'description': 'ID único de la marca'},
        'nombre': {'type': 'string', 'description': 'Nombre de la marca'}
    }
            },
            'MarcaInput': {
                'type': 'object',
                'required': ['nombre'],
                'properties': {
                    'nombre': {'type': 'string', 'description': 'Nombre de la marca'}
                }
            },
            'ModeloInput': {
                'type': 'object',
                'required': ['nombre', 'marca_id'],
                'properties': {
                    'nombre': {'type': 'string', 'description': 'Nombre del modelo'},
                    'marca_id': {'type': 'integer', 'description': 'ID de la marca'}
                }
            },
            'ModeloResponse': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único del modelo'},
                    'nombre': {'type': 'string', 'description': 'Nombre del modelo'},
                    'marca_id': {'type': 'integer', 'description': 'ID de la marca'}
                }
            },
            'ModeloCreatedResponse': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'description': 'Indica si la operación fue exitosa'},
                    'message': {'type': 'string', 'description': 'Mensaje descriptivo del resultado'},
                    'modelo': {'$ref': '#/components/schemas/ModeloResponse'}
                }
            }
        }
    }
}