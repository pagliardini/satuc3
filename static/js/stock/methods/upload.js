const uploadMethods = {
    /**
     * Maneja la selección de imágenes
     */
    onImageSelected(event) {
        const file = event.target.files[0];
        if (file) {
            this.selectedImage = file;
        }
    },
    
    /**
     * Sube una imagen al servidor
     */
    async uploadImage() {
        if (!this.selectedImage) return;
        
        this.uploading = true;
        try {
            const formData = new FormData();
            formData.append('file', this.selectedImage);
            
            // Determinar categoría basada en el tipo seleccionado
            let categoria = 'otros';
            if (this.newInsumo.tipo_id) {
                const tipo = this.tiposProducto.find(t => t.id == this.newInsumo.tipo_id);
                if (tipo && tipo.nombre.toLowerCase().includes('impresora')) {
                    categoria = 'impresoras';
                } else if (tipo && tipo.nombre.toLowerCase().includes('ups')) {
                    categoria = 'ups';
                }
            }
            
            formData.append('categoria', categoria);
            
            const response = await axios.post('/api/upload/imagen', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            if (response.data.success) {
                this.newInsumo.url_imagen = response.data.url;
                this.selectedImage = null;
                this.$refs.imageFile.value = '';
                this.showToast('Éxito', 'Imagen subida correctamente', 'bg-success text-white');
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
            
        } catch (error) {
            const message = error.response?.data?.message || 'Error al subir imagen';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.uploading = false;
        }
    },
    
    /**
     * Elimina una imagen del insumo
     */
    async removeImage() {
        if (this.newInsumo.url_imagen) {
            try {
                // Extraer filename de la URL
                const filename = this.newInsumo.url_imagen.split('/').pop();
                await axios.delete(`/api/upload/imagen/${filename}`);
                this.newInsumo.url_imagen = '';
                this.showToast('Éxito', 'Imagen eliminada', 'bg-success text-white');
            } catch (error) {
                console.error('Error al eliminar imagen:', error);
            }
        }
    },
    
    /**
     * Maneja la selección de imágenes para edición
     */
    onEditImageSelected(event) {
        const file = event.target.files[0];
        if (file) {
            this.selectedEditImage = file;
        }
    },
    
    /**
     * Sube una imagen al servidor para un insumo en edición
     */
    async uploadEditImage() {
        if (!this.selectedEditImage) return;
        
        this.uploadingEdit = true;
        try {
            const formData = new FormData();
            formData.append('file', this.selectedEditImage);
            
            // Determinar categoría basada en el tipo seleccionado
            let categoria = 'otros';
            if (this.editingInsumo.tipo_id) {
                const tipo = this.tiposProducto.find(t => t.id == this.editingInsumo.tipo_id);
                if (tipo && tipo.nombre.toLowerCase().includes('impresora')) {
                    categoria = 'impresoras';
                } else if (tipo && tipo.nombre.toLowerCase().includes('ups')) {
                    categoria = 'ups';
                }
            }
            
            formData.append('categoria', categoria);
            
            const response = await axios.post('/api/upload/imagen', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            if (response.data.success) {
                this.editingInsumo.url_imagen = response.data.url;
                this.selectedEditImage = null;
                this.$refs.editImageFile.value = '';
                this.showToast('Éxito', 'Imagen subida correctamente', 'bg-success text-white');
            } else {
                this.showToast('Error', response.data.message, 'bg-danger text-white');
            }
            
        } catch (error) {
            const message = error.response?.data?.message || 'Error al subir imagen';
            this.showToast('Error', message, 'bg-danger text-white');
        } finally {
            this.uploadingEdit = false;
        }
    },
    
    /**
     * Elimina una imagen del insumo en edición
     */
    async removeEditImage() {
        if (this.editingInsumo.url_imagen) {
            try {
                const filename = this.editingInsumo.url_imagen.split('/').pop();
                await axios.delete(`/api/upload/imagen/${filename}`);
                this.editingInsumo.url_imagen = '';
                this.showToast('Éxito', 'Imagen eliminada', 'bg-success text-white');
            } catch (error) {
                console.error('Error al eliminar imagen:', error);
            }
        }
    }
};