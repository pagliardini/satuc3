const imputarMethods = {
    /**
     * Resetea el formulario de imputación
     */
    resetImputacionForm() {
        this.imputacion = {
            insumo_id: '',
            area_id: '',
            cantidad: 1,
            codigo: '',
            responsable: '',
            observacion: ''
        };
    },
    
    /**
     * Realiza la imputación de stock
     */
    async imputarStock() {
        // Validar formulario
        if (!this.imputacion.insumo_id || !this.imputacion.area_id || !this.imputacion.cantidad) {
            this.showToast('Error', 'Insumo, área y cantidad son obligatorios', 'bg-danger text-white');
            return;
        }
        
        // Validar código para insumos inventariables
        const insumo = this.insumos.find(i => i.id == this.imputacion.insumo_id);
        if (insumo && insumo.inventariable && !this.imputacion.codigo) {
            this.showToast('Error', 'El código es obligatorio para insumos inventariables', 'bg-danger text-white');
            return;
        }
        
        this.loading = true;
        try {
            const response = await axios.post('/api/stock/imputar', this.imputacion);
            
            if (response.data.success) {
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.resetImputacionForm();
                await this.loadData();
                // Cambiar a la pestaña de stock para ver el resultado
                this.tab = 'stock';
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al imputar stock';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    }
};