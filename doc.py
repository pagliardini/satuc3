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
        {'name': 'Stock', 'description': 'Gestión de inventario y movimientos de stock'},
        {'name': 'Tipos de Productos', 'description': 'Operaciones relacionadas con los tipos de productos'}
    ],
    'paths': {
        # Sedes endpoints
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
                    '409': {'description': 'La unidad ya existe en la sede'}
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
            },
            'put': {
                'tags': ['Unidades Organizativas'],
                'summary': 'Actualizar una unidad organizativa',
                'parameters': [
                    {
                        'name': 'unidad_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID de la unidad organizativa a actualizar'
                    }
                ],
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/UnidadInput'}
                        }
                    }
                },
                'responses': {
                    '200': {
                        'description': 'Unidad actualizada correctamente',
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
                    '404': {'description': 'Unidad o sede no encontrada'},
                    '409': {'description': 'Ya existe una unidad con ese nombre en la sede especificada'}
                }
            },
            'delete': {
                'tags': ['Unidades Organizativas'],
                'summary': 'Eliminar una unidad organizativa',
                'parameters': [
                    {
                        'name': 'unidad_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID de la unidad organizativa a eliminar'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Unidad eliminada correctamente',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'mensaje': {'type': 'string'},
                                        'id': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    },
                    '404': {'description': 'Unidad no encontrada'},
                    '409': {'description': 'No se puede eliminar la unidad organizativa porque tiene dependencias'}
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
            },
            'post': {
                'tags': ['Productos'],
                'summary': 'Crear un nuevo producto',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/ProductoInput'}
                        }
                    }
                },
                'responses': {
                    '201': {
                        'description': 'Producto creado exitosamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/ProductoResponse'}
                            }
                        }
                    },
                    '400': {'description': 'Datos inválidos o faltantes'},
                    '404': {'description': 'Tipo, marca o modelo no encontrado'},
                    '500': {'description': 'Error del servidor'}
                }
            }
        },
        '/productos/{producto_id}': {
            'get': {
                'tags': ['Productos'],
                'summary': 'Obtener un producto específico',
                'parameters': [
                    {
                        'name': 'producto_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del producto'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Detalles del producto',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/Producto'}
                            }
                        }
                    },
                    '404': {'description': 'Producto no encontrado'}
                }
            },
            'put': {
                'tags': ['Productos'],
                'summary': 'Actualizar un producto',
                'parameters': [
                    {
                        'name': 'producto_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del producto a actualizar'
                    }
                ],
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/ProductoInput'}
                        }
                    }
                },
                'responses': {
                    '200': {
                        'description': 'Producto actualizado correctamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/ProductoResponse'}
                            }
                        }
                    },
                    '404': {'description': 'Producto no encontrado'},
                    '500': {'description': 'Error del servidor'}
                }
            },
            'delete': {
                'tags': ['Productos'],
                'summary': 'Eliminar un producto',
                'parameters': [
                    {
                        'name': 'producto_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del producto a eliminar'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Producto eliminado correctamente',
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
                    '404': {'description': 'Producto no encontrado'},
                    '500': {'description': 'Error del servidor'}
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
        },
        '/areas': {
            'get': {
                'tags': ['Áreas'],
                'summary': 'Obtener todas las áreas',
                'responses': {
                    '200': {
                        'description': 'Lista de áreas',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'array',
                                    'items': {'$ref': '#/components/schemas/Area'}
                                }
                            }
                        }
                    }
                }
            },
            'post': {
                'tags': ['Áreas'],
                'summary': 'Crear una nueva área',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/AreaInput'}
                        }
                    }
                },
                'responses': {
                    '201': {
                        'description': 'Área creada exitosamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/AreaResponse'}
                            }
                        }
                    },
                    '400': {'description': 'Datos inválidos'},
                    '404': {'description': 'Unidad organizativa no encontrada'},
                    '409': {'description': 'El área ya existe en la unidad organizativa'}
                }
            }
        },
        '/areas/{area_id}': {
            'get': {
                'tags': ['Áreas'],
                'summary': 'Obtener un área específica',
                'parameters': [
                    {
                        'name': 'area_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del área'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Detalles del área',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/Area'}
                            }
                        }
                    },
                    '404': {'description': 'Área no encontrada'}
                }
            },
            'put': {
                'tags': ['Áreas'],
                'summary': 'Actualizar un área',
                'parameters': [
                    {
                        'name': 'area_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del área a actualizar'
                    }
                ],
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/AreaInput'}
                        }
                    }
                },
                'responses': {
                    '200': {
                        'description': 'Área actualizada correctamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/AreaResponse'}
                            }
                        }
                    },
                    '400': {'description': 'Datos inválidos'},
                    '404': {'description': 'Área o unidad organizativa no encontrada'},
                    '409': {'description': 'Ya existe un área con ese nombre en la unidad organizativa'}
                }
            },
            'delete': {
                'tags': ['Áreas'],
                'summary': 'Eliminar un área',
                'parameters': [
                    {
                        'name': 'area_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del área a eliminar'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Área eliminada correctamente',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'mensaje': {'type': 'string'},
                                        'id': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    },
                    '404': {'description': 'Área no encontrada'},
                    '409': {'description': 'No se puede eliminar el área porque tiene dependencias'}
                }
            }
        },
        '/areas/{area_id}/set_deposito': {
            'put': {
                'tags': ['Áreas'],
                'summary': 'Marcar un área como depósito',
                'parameters': [
                    {
                        'name': 'area_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del área a marcar como depósito'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Área marcada como depósito correctamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/AreaResponse'}
                            }
                        }
                    },
                    '404': {'description': 'Área no encontrada'},
                    '500': {'description': 'Error al establecer el área como depósito'}
                }
            }
        },
        # Updated Stock endpoints
        '/stock': {
            'get': {
                'tags': ['Stock'],
                'summary': 'Obtener todo el stock',
                'description': 'Retorna una lista de todos los items en stock con detalles de producto y área',
                'responses': {
                    '200': {
                        'description': 'Lista de items en stock',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'array',
                                    'items': {'$ref': '#/components/schemas/StockItem'}
                                }
                            }
                        }
                    }
                }
            },
            'post': {
                'tags': ['Stock'],
                'summary': 'Registrar nuevo stock',
                'description': 'Registra nuevo stock considerando si el producto es inventariable o no. Permite crear un nuevo producto durante la imputación o utilizar uno existente.',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/StockInputExtendido'}
                        }
                    }
                },
                'responses': {
                    '201': {
                        'description': 'Stock registrado correctamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/StockResponseExtendido'}
                            }
                        }
                    },
                    '400': {'description': 'Datos inválidos'},
                    '404': {'description': 'Producto, área, tipo, marca o modelo no encontrado'},
                    '500': {'description': 'Error del servidor'}
                }
            }
        },
        '/stock/{stock_id}': {
            'get': {
                'tags': ['Stock'],
                'summary': 'Obtener detalles de un item de stock',
                'description': 'Retorna información detallada sobre un item específico del stock',
                'parameters': [
                    {
                        'name': 'stock_id',
                        'in': 'path',
                        'required': True,
                        'schema': {'type': 'integer'},
                        'description': 'ID del item de stock'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Detalles del item de stock',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/StockItemDetail'}
                            }
                        }
                    },
                    '404': {'description': 'Item de stock no encontrado'}
                }
            }
        },
        '/stock/movimientos': {
            'post': {
                'tags': ['Stock'],
                'summary': 'Mover stock entre áreas',
                'description': 'Traslada items de stock entre diferentes áreas. El comportamiento varía según el tipo de producto: los inventariables se mueven de uno en uno, los no inventariables permiten mover cantidades parciales.',
                'requestBody': {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/StockMoveInput'}
                        }
                    }
                },
                'responses': {
                    '200': {
                        'description': 'Stock movido correctamente',
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/StockMoveResponse'}
                            }
                        }
                    },
                    '400': {'description': 'Datos inválidos o movimiento no permitido'},
                    '404': {'description': 'Stock o área no encontrada'},
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
            },
            'Area': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único del área'},
                    'nombre': {'type': 'string', 'description': 'Nombre del área'},
                    'unidad_organizativa_id': {'type': 'integer', 'description': 'ID de la unidad organizativa'},
                    'es_deposito': {'type': 'boolean', 'description': 'Indica si el área es un depósito'}
                }
            },
            'AreaInput': {
                'type': 'object',
                'required': ['nombre', 'unidad_organizativa_id'],
                'properties': {
                    'nombre': {'type': 'string', 'description': 'Nombre del área'},
                    'unidad_organizativa_id': {'type': 'integer', 'description': 'ID de la unidad organizativa'}
                }
            },
            'AreaResponse': {
                'type': 'object',
                'properties': {
                    'mensaje': {'type': 'string', 'description': 'Mensaje de la operación'},
                    'area': {'$ref': '#/components/schemas/Area'}
                }
            },
            'ProductoInput': {
                'type': 'object',
                'required': ['tipo_id', 'marca_id', 'modelo_id'],
                'properties': {
                    'tipo_id': {'type': 'integer', 'description': 'ID del tipo de producto'},
                    'marca_id': {'type': 'integer', 'description': 'ID de la marca'},
                    'modelo_id': {'type': 'integer', 'description': 'ID del modelo'},
                    'descripcion': {'type': 'string', 'description': 'Descripción del producto'},
                    'inventariable': {'type': 'boolean', 'description': 'Si el producto es inventariable'},
                    'activo': {'type': 'boolean', 'description': 'Si el producto está activo'}
                }
            },
            'ProductoResponse': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'producto': {'$ref': '#/components/schemas/Producto'}
                }
            },
            'StockItem': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único del item de stock'},
                    'area': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'description': 'ID del área'},
                            'nombre': {'type': 'string', 'description': 'Nombre del área'}
                        }
                    },
                    'producto': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'description': 'ID del producto'},
                            'nombre': {'type': 'string', 'description': 'Nombre completo del producto'}
                        }
                    },
                    'codigo': {'type': 'string', 'description': 'Código único (solo para productos inventariables)'},
                    'cantidad': {'type': 'integer', 'description': 'Cantidad en stock (siempre 1 para productos inventariables)'},
                    'fecha_imputacion': {'type': 'string', 'format': 'date-time', 'description': 'Fecha en que se imputó inicialmente el stock'}
                }
            },
            'StockItemDetail': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID único del item de stock'},
                    'area': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'description': 'ID del área'},
                            'nombre': {'type': 'string', 'description': 'Nombre del área'}
                        }
                    },
                    'producto': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'description': 'ID del producto'},
                            'nombre': {'type': 'string', 'description': 'Nombre completo del producto'},
                            'inventariable': {'type': 'boolean', 'description': 'Indica si el producto es inventariable'}
                        }
                    },
                    'codigo': {'type': 'string', 'description': 'Código único (solo para productos inventariables)'},
                    'cantidad': {'type': 'integer', 'description': 'Cantidad en stock'},
                    'fecha_imputacion': {'type': 'string', 'format': 'date-time', 'description': 'Fecha en que se imputó inicialmente el stock'},
                    'ultimo_movimiento': {'type': 'string', 'format': 'date-time', 'description': 'Fecha del último movimiento'}
                }
            },
            'StockInput': {
                'type': 'object',
                'required': ['producto_id', 'area_id', 'cantidad'],
                'properties': {
                    'producto_id': {'type': 'integer', 'description': 'ID del producto'},
                    'area_id': {'type': 'integer', 'description': 'ID del área donde se imputará el stock'},
                    'cantidad': {'type': 'integer', 'description': 'Cantidad a registrar'}
                }
            },
            'StockInputExtendido': {
                'type': 'object',
                'required': ['area_id', 'cantidad'],
                'properties': {
                    'producto_id': {'type': 'integer', 'description': 'ID del producto existente. Requerido solo si crear_producto es false'},
                    'area_id': {'type': 'integer', 'description': 'ID del área donde se imputará el stock'},
                    'cantidad': {'type': 'integer', 'description': 'Cantidad a registrar'},
                    'crear_producto': {'type': 'boolean', 'description': 'Indica si se debe crear un nuevo producto'},
                    'tipo_id': {'type': 'integer', 'description': 'ID del tipo de producto. Requerido si crear_producto es true'},
                    'marca_id': {'type': 'integer', 'description': 'ID de la marca. Requerido si crear_producto es true'},
                    'modelo_id': {'type': 'integer', 'description': 'ID del modelo. Requerido si crear_producto es true'},
                    'descripcion': {'type': 'string', 'description': 'Descripción del producto nuevo'},
                    'inventariable': {'type': 'boolean', 'description': 'Si el producto nuevo es inventariable'},
                    'activo': {'type': 'boolean', 'description': 'Si el producto nuevo está activo'}
                }
            },
            'StockMoveInput': {
                'type': 'object',
                'required': ['stock_id', 'destino_area_id', 'cantidad'],
                'properties': {
                    'stock_id': {'type': 'integer', 'description': 'ID del item de stock a mover'},
                    'destino_area_id': {'type': 'integer', 'description': 'ID del área de destino'},
                    'cantidad': {'type': 'integer', 'description': 'Cantidad a mover (debe ser 1 para productos inventariables)'},
                    'observacion': {'type': 'string', 'description': 'Comentario opcional sobre el movimiento'}
                }
            },
            'StockResponse': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'description': 'Indica si la operación fue exitosa'},
                    'message': {'type': 'string', 'description': 'Mensaje descriptivo del resultado'},
                    'stock': {
                        'type': 'object',
                        'properties': {
                            'producto': {'type': 'string', 'description': 'Nombre del producto'},
                            'area': {'type': 'string', 'description': 'Nombre del área'},
                            'cantidad': {'type': 'integer', 'description': 'Cantidad total registrada'},
                            'codigos': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Lista de códigos generados para productos inventariables'
                            }
                        }
                    }
                }
            },
            'StockResponseExtendido': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'description': 'Indica si la operación fue exitosa'},
                    'message': {'type': 'string', 'description': 'Mensaje descriptivo del resultado'},
                    'stock': {
                        'type': 'object',
                        'properties': {
                            'producto': {'type': 'string', 'description': 'Nombre del producto'},
                            'area': {'type': 'string', 'description': 'Nombre del área'},
                            'cantidad': {'type': 'integer', 'description': 'Cantidad total registrada'},
                            'codigos': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Lista de códigos generados para productos inventariables'
                            }
                        }
                    },
                    'producto_creado': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'description': 'ID del producto creado'},
                            'tipo': {'type': 'string', 'description': 'Tipo del producto'},
                            'marca': {'type': 'string', 'description': 'Marca del producto'},
                            'modelo': {'type': 'string', 'description': 'Modelo del producto'},
                            'descripcion': {'type': 'string', 'description': 'Descripción del producto'},
                            'inventariable': {'type': 'boolean', 'description': 'Si el producto es inventariable'}
                        },
                        'description': 'Información del producto recién creado (solo si crear_producto=true)'
                    }
                }
            },
            'StockMoveResponse': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'description': 'Indica si la operación fue exitosa'},
                    'message': {'type': 'string', 'description': 'Mensaje descriptivo del resultado'},
                    'movimiento': {
                        'type': 'object',
                        'properties': {
                            'origen': {'type': 'string', 'description': 'Nombre del área de origen'},
                            'destino': {'type': 'string', 'description': 'Nombre del área de destino'},
                            'producto': {'type': 'string', 'description': 'Nombre completo del producto'},
                            'cantidad': {'type': 'integer', 'description': 'Cantidad movida'}
                        }
                    }
                }
            }
        }
    }
}