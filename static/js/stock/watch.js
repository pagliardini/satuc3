const stockWatchers = {
    'newInsumo.tipo_id': function(newVal, oldVal) {
        // Si cambió el tipo, limpiar tóner y batería según corresponda
        if (newVal !== oldVal) {
            // Si no es impresora, limpiar tóner
            if (!this.isImpresoraSelected) {
                this.newInsumo.toner_id = '';
            }
            // Si no es UPS, limpiar batería
            if (!this.isUpsSelected) {
                this.newInsumo.bateria_id = '';
            }
        }
    },
    
    'newInsumo.marca_id': function(newVal, oldVal) {
        // Si cambia la marca, resetear el modelo
        if (newVal !== oldVal) {
            this.newInsumo.modelo_id = '';
        }
    },
    
    'editingInsumo.tipo_id': function(newVal, oldVal) {
        if (this.editingInsumo && newVal !== oldVal) {
            // Si no es impresora, limpiar tóner
            if (!this.isImpresoraSelectedEdit) {
                this.editingInsumo.toner_id = '';
            }
            // Si no es UPS, limpiar batería
            if (!this.isUpsSelectedEdit) {
                this.editingInsumo.bateria_id = '';
            }
        }
    },
    
    'editingInsumo.marca_id': function(newVal, oldVal) {
        // Si cambia la marca, resetear el modelo
        if (this.editingInsumo && newVal !== oldVal) {
            this.editingInsumo.modelo_id = '';
        }
    },
    
    'movimiento.stock_origen_id': function(newVal, oldVal) {
        // Actualizar cantidad disponible al cambiar el origen
        if (newVal !== oldVal) {
            this.updateCantidadMaxima();
        }
    }
};