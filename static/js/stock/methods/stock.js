const stockMethods = {
    /**
     * Obtiene la clase CSS para el badge de estado
     */
    getEstadoBadgeClass(estado) {
        const classes = {
            'disponible': 'bg-success',
            'asignado': 'bg-primary',
            'en_reparacion': 'bg-warning',
            'baja': 'bg-danger'
        };
        return classes[estado] || 'bg-secondary';
    },
    
    /**
     * Muestra el modal para mover stock
     */
    showMoveStockModal(stockItem) {
        this.stockToMove = stockItem;
        this.areaSearch = '';
        this.filteredAreas = [];
        this.moveForm = {
            area_destino_id: '',
            cantidad: stockItem.cantidad,
            responsable: '',
            observacion: ''
        };
        
        if (!this.moveStockModalInstance) {
            this.moveStockModalInstance = new bootstrap.Modal(document.getElementById('moveStockModal'));
        }
        this.moveStockModalInstance.show();
    },
    
    /**
     * Filtra áreas al escribir en el campo de búsqueda
     */
    filterAreas() {
        if (!this.areaSearch.trim()) {
            this.filteredAreas = [];
            this.moveForm.area_destino_id = '';
            return;
        }
        
        const searchLower = this.areaSearch.toLowerCase();
        this.filteredAreas = this.areas.filter(area => 
            area.nombre.toLowerCase().includes(searchLower) && 
            area.id !== this.stockToMove.area.id // Excluir el área actual
        ).slice(0, 5); // Limitar a 5 resultados
    },
    
    /**
     * Selecciona un área de la lista filtrada
     */
    selectArea(area) {
        this.areaSearch = area.nombre;
        this.moveForm.area_destino_id = area.id;
        this.filteredAreas = [];
    },
    
    /**
     * Muestra el modal para dar de baja stock
     */
    showBajaStockModal(stockItem) {
        this.stockToBaja = stockItem;
        this.bajaForm = {
            motivo: '',
            responsable: '',
            observacion: ''
        };
        
        if (!this.bajaStockModalInstance) {
            this.bajaStockModalInstance = new bootstrap.Modal(document.getElementById('bajaStockModal'));
        }
        this.bajaStockModalInstance.show();
    },
    
    /**
     * Dar de baja un stock
     */
    async darDeBajaStock() {
        if (!this.stockToBaja || !this.bajaForm.motivo) return;
        
        this.loading = true;
        try {
            const bajaData = {
                stock_id: this.stockToBaja.id,
                motivo: this.bajaForm.motivo,
                responsable: this.bajaForm.responsable,
                observacion: this.bajaForm.observacion
            };
            
            const response = await axios.post('/api/stock/baja', bajaData);
            if (response.data.success) {
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.bajaStockModalInstance.hide();
                this.stockToBaja = null;
                await this.loadData();
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al dar de baja stock';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },
    
    /**
     * Manejo de error en carga de imágenes
     */
    onImageError(event) {
        event.target.style.display = 'none';
        const placeholder = event.target.nextElementSibling;
        if (placeholder) {
            placeholder.style.display = 'flex';
        }
    }
};