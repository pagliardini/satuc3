const insumosMethods = {
    /**
     * Resetea el formulario de nuevo insumo
     */
    resetNewInsumoForm() {
        this.newInsumo = {
            tipo_id: '',
            marca_id: '',
            modelo_id: '',
            descripcion: '',
            inventariable: true,
            toner_id: '',
            bateria_id: '',
            url_imagen: ''
        };
    },
    
    /**
     * Crea un nuevo insumo
     */
    async createInsumo() {
        this.loading = true;
        try {
            const response = await axios.post('/api/stock/insumos', this.newInsumo);
            if (response.data.success) {
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.resetNewInsumoForm();
                await this.loadData();
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al crear insumo';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },
    
    /**
     * Muestra el modal de confirmación para eliminar un insumo
     */
    confirmDeleteInsumo(insumo) {
        this.insumoToDelete = insumo;
        if (!this.deleteConfirmModalInstance) {
            this.deleteConfirmModalInstance = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
        }
        this.deleteConfirmModalInstance.show();
    },
    
    /**
     * Elimina un insumo
     */
    async deleteInsumo() {
        if (!this.insumoToDelete) return;
        
        this.loading = true;
        try {
            const response = await axios.delete(`/api/stock/insumos/${this.insumoToDelete.id}`);
            if (response.data.success) {
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.deleteConfirmModalInstance.hide();
                this.insumoToDelete = null;
                await this.loadData();
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al eliminar insumo';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },
    
    /**
     * Muestra el modal para editar un insumo
     */
    editInsumo(insumo) {
        // Clonar el insumo para edición
        this.editingInsumo = {
            id: insumo.id,
            tipo_id: insumo.tipo.id,
            marca_id: insumo.marca.id,
            modelo_id: insumo.modelo.id,
            descripcion: insumo.descripcion || '',
            inventariable: insumo.inventariable,
            toner_id: insumo.toner ? insumo.toner.id : '',
            bateria_id: insumo.bateria ? insumo.bateria.id : '',
            url_imagen: insumo.url_imagen || ''
        };
        
        if (!this.editInsumoModalInstance) {
            this.editInsumoModalInstance = new bootstrap.Modal(document.getElementById('editInsumoModal'));
        }
        this.editInsumoModalInstance.show();
    },
    
    /**
     * Actualiza un insumo
     */
    async updateInsumo() {
        if (!this.editingInsumo) return;
        
        this.loading = true;
        try {
            const response = await axios.put(`/api/stock/insumos/${this.editingInsumo.id}`, this.editingInsumo);
            if (response.data.success) {
                this.showToast('Éxito', 'Insumo actualizado correctamente', 'bg-success text-white');
                this.editInsumoModalInstance.hide();
                this.editingInsumo = null;
                await this.loadData();
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Error al actualizar insumo';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },
    
    /**
     * Muestra el modal para crear un nuevo elemento (tipo, marca, modelo, etc.)
     */
    showCreateModal(type) {
        this.modalType = type;
        this.newItem = {
            nombre: '',
            marca_id: '',
            cantidad: ''
        };
        
        // Definir título según el tipo
        const titles = {
            'tipo': 'Nuevo Tipo de Producto',
            'marca': 'Nueva Marca',
            'modelo': 'Nuevo Modelo',
            'toner': 'Nuevo Tóner',
            'bateria': 'Nueva Batería'
        };
        
        const names = {
            'tipo': 'Tipo de Producto',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'toner': 'Tóner',
            'bateria': 'Batería'
        };
        
        this.modalTitle = titles[type];
        this.modalTypeName = names[type];
        
        if (!this.createModalInstance) {
            this.createModalInstance = new bootstrap.Modal(document.getElementById('createModal'));
        }
        this.createModalInstance.show();
    },
    
    /**
     * Crea un nuevo elemento (tipo, marca, modelo, etc.)
     */
    async createNewItem() {
        if (!this.isFormValid) return;
        
        this.loading = true;
        try {
            let response;
            
            switch (this.modalType) {
                case 'tipo':
                    response = await axios.post('/api/stock/tipos', { nombre: this.newItem.nombre });
                    break;
                case 'marca':
                    response = await axios.post('/api/stock/marcas', { nombre: this.newItem.nombre });
                    break;
                case 'modelo':
                    response = await axios.post('/api/modelos', { 
                        nombre: this.newItem.nombre,
                        marca_id: this.newItem.marca_id
                    });
                    break;
                case 'toner':
                    response = await axios.post('/api/toners_baterias', { nombre: this.newItem.nombre });
                    break;
                case 'bateria':
                    response = await axios.post('/api/baterias', { cantidad: this.newItem.cantidad });
                    break;
            }
            
            if (response.data.success) {
                // Actualizar listas y seleccionar el nuevo elemento
                await this.loadData();
                
                // Seleccionar el nuevo elemento en el formulario principal
                if (this.modalType === 'tipo') {
                    this.newInsumo.tipo_id = response.data.id;
                } else if (this.modalType === 'marca') {
                    this.newInsumo.marca_id = response.data.id;
                } else if (this.modalType === 'modelo') {
                    this.newInsumo.modelo_id = response.data.id;
                } else if (this.modalType === 'toner') {
                    this.newInsumo.toner_id = response.data.id;
                } else if (this.modalType === 'bateria') {
                    this.newInsumo.bateria_id = response.data.id;
                }
                
                this.showToast('Éxito', response.data.message, 'bg-success text-white');
                this.createModalInstance.hide();
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
        } catch (error) {
            const message = error.response?.data?.message || `Error al crear ${this.modalTypeName}`;
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    }
};