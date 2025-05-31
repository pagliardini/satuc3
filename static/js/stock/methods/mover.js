const moverMethods = {
    /**
     * Resetea el formulario de movimiento
     */
    resetMovimientoForm() {
        this.movimiento = {
            stock_origen_id: '',
            area_destino_id: '',
            cantidad: 1,
            responsable: '',
            observacion: ''
        };
    },
    
    /**
     * Actualiza la cantidad máxima disponible al seleccionar origen
     */
    updateCantidadMaxima() {
        if (this.movimiento.stock_origen_id) {
            const stockOrigen = this.stockItems.find(item => item.id == this.movimiento.stock_origen_id);
            if (stockOrigen) {
                this.movimiento.cantidad = stockOrigen.cantidad;
            }
        } else {
            this.movimiento.cantidad = 1;
        }
    },
    
    /**
     * Realiza el movimiento de stock
     */
    async moverStock() {
        // Validar formulario
        if (!this.movimiento.stock_origen_id || !this.movimiento.area_destino_id || !this.movimiento.cantidad) {
            this.showToast('Error', 'Origen, destino y cantidad son obligatorios', 'bg-danger text-white');
            return;
        }
        
        this.loading = true;
        try {
            const response = await axios.post('/api/stock/mover', this.movimiento);
            
            if (response.data.success) {
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.resetMovimientoForm();
                await this.loadData();
                // Cambiar a la pestaña de stock para ver el resultado
                this.tab = 'stock';
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al mover stock';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },
    
    /**
     * Mover stock desde el modal
     */
    async moveStockFromModal() {
        if (!this.stockToMove || !this.moveForm.area_destino_id) return;
        
        this.loading = true;
        try {
            const moveData = {
                stock_origen_id: this.stockToMove.id,
                area_destino_id: this.moveForm.area_destino_id,
                cantidad: this.moveForm.cantidad,
                responsable: this.moveForm.responsable,
                observacion: this.moveForm.observacion
            };
            
            const response = await axios.post('/api/stock/mover', moveData);
            if (response.data.success) {
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.moveStockModalInstance.hide();
                this.stockToMove = null;
                await this.loadData();
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al mover stock';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    }
};