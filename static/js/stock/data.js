function getStockData() {
    return {
        tab: 'stock',
        stockItems: [],
        insumos: [],
        areas: [],
        tiposProducto: [],
        marcas: [],
        modelos: [],
        toners: [],
        baterias: [],
        
        searchStock: '',
        searchInsumos: '',
        loading: false,
        
        newInsumo: {
            tipo_id: '',
            marca_id: '',
            modelo_id: '',
            descripcion: '',
            inventariable: true,
            toner_id: '',
            bateria_id: '',
            url_imagen: ''
        },
        
        imputacion: {
            insumo_id: '',
            area_id: '',
            cantidad: 1,
            responsable: '',
            observacion: ''
        },
        
        movimiento: {
            stock_origen_id: '',
            area_destino_id: '',
            cantidad: 1,
            responsable: '',
            observacion: ''
        },
        
        toastMessage: '',
        toastTitle: '',
        toastClass: '',
        resultToast: null,
        
        // Propiedades para el modal
        modalType: '',
        modalTitle: '',
        modalTypeName: '',
        newItem: {
            nombre: '',
            marca_id: '',
            cantidad: ''
        },
        createModalInstance: null,
        
        // Propiedad para filtrar stock
        stockFilter: 'todos',
        
        // Propiedades para la carga de imágenes
        selectedImage: null,
        uploading: false,
        
        // Propiedades para mover stock
        stockToMove: null,
        moveStockModalInstance: null,
        areaSearch: '',
        filteredAreas: [],
        moveForm: {
            area_destino_id: '',
            cantidad: 1,
            responsable: '',
            observacion: ''
        },
        
        // Propiedades para dar de baja
        stockToBaja: null,
        bajaStockModalInstance: null,
        bajaForm: {
            motivo: '',
            responsable: '',
            observacion: ''
        },
        
        // Propiedad para insumo a eliminar
        insumoToDelete: null,
        deleteConfirmModalInstance: null
    };
}