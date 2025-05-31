const stockComputed = {
    filteredStock() {
        if (!this.searchStock) return this.stockItems;
        const searchLower = this.searchStock.toLowerCase();
        return this.stockItems.filter(item => 
            item.insumo.nombre_completo.toLowerCase().includes(searchLower) ||
            item.area.nombre.toLowerCase().includes(searchLower) ||
            (item.codigo && item.codigo.toLowerCase().includes(searchLower))
        );
    },
    
    filteredInsumos() {
        if (!this.searchInsumos) return this.insumos;
        const searchLower = this.searchInsumos.toLowerCase();
        return this.insumos.filter(insumo => 
            insumo.nombre_completo.toLowerCase().includes(searchLower) ||
            insumo.tipo.nombre.toLowerCase().includes(searchLower) ||
            insumo.marca.nombre.toLowerCase().includes(searchLower) ||
            insumo.modelo.nombre.toLowerCase().includes(searchLower)
        );
    },
    
    modelosFiltered() {
        if (!this.newInsumo.marca_id) return [];
        return this.modelos.filter(modelo => modelo.marca_id == this.newInsumo.marca_id);
    },
    
    // Propiedad computada para validar el formulario del modal
    isFormValid() {
        if (this.modalType === 'tipo' || this.modalType === 'marca' || this.modalType === 'toner') {
            return this.newItem.nombre && this.newItem.nombre.trim() !== '';
        }
        if (this.modalType === 'modelo') {
            return this.newItem.nombre && this.newItem.nombre.trim() !== '' && this.newItem.marca_id;
        }
        if (this.modalType === 'bateria') {
            return this.newItem.cantidad && this.newItem.cantidad > 0;
        }
        return false;
    },
    
    // Propiedades computadas para las vistas filtradas de stock
    filteredStockImpresoras() {
        let stockImpresoras = this.stockItems.filter(item => {
            return item.insumo.tipo && item.insumo.tipo.toLowerCase().includes('impresora');
        });
        
        if (!this.searchStock) return stockImpresoras;
        const searchLower = this.searchStock.toLowerCase();
        return stockImpresoras.filter(item => 
            item.insumo.nombre_completo.toLowerCase().includes(searchLower) ||
            item.area.nombre.toLowerCase().includes(searchLower) ||
            (item.codigo && item.codigo.toLowerCase().includes(searchLower)) ||
            (item.insumo.toner && item.insumo.toner.toLowerCase().includes(searchLower))
        );
    },
    
    filteredStockUps() {
        // Similar a filteredStockImpresoras pero para UPS
    },
    
    // Propiedades computadas para habilitar/deshabilitar campos según selección
    isImpresoraSelected() {
        if (!this.newInsumo.tipo_id) return false;
        const tipoSeleccionado = this.tiposProducto.find(t => t.id == this.newInsumo.tipo_id);
        return tipoSeleccionado && tipoSeleccionado.nombre.toLowerCase().includes('impresora');
    },
    
    isUpsSelected() {
        if (!this.newInsumo.tipo_id) return false;
        const tipoSeleccionado = this.tiposProducto.find(t => t.id == this.newInsumo.tipo_id);
        return tipoSeleccionado && tipoSeleccionado.nombre.toLowerCase().includes('ups');
    },
    
    isEditingImpresoraSelected() {
        return this.editingInsumo && this.tiposProducto.find(t => 
            t.id === this.editingInsumo.tipo_id)?.nombre.toLowerCase().includes('impresora');
    },
    
    isEditingUpsSelected() {
        return this.editingInsumo && this.tiposProducto.find(t => 
            t.id === this.editingInsumo.tipo_id)?.nombre.toLowerCase().includes('ups');
    }
};