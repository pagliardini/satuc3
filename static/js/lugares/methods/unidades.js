// Métodos específicos para gestión de unidades organizativas
const lugaresUnidadesMethods = {
    // Cargar listado de unidades
    async loadUnidades() {
        this.loading = true;
        try {
            const res = await axios.get('/api/unidades');
            this.unidades = res.data;
        } catch (e) {
            this.showToast('Error', 'No se pudieron cargar las unidades.', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Agregar nueva unidad
    async addUnidad() {
        if (!this.newUnidadNombre || !this.newUnidadSedeId) return;
        this.loading = true;
        try {
            const res = await axios.post('/api/unidades', { 
                nombre: this.newUnidadNombre, 
                sede_id: this.newUnidadSedeId 
            });
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Unidad agregada correctamente', 'bg-success text-white');
                this.newUnidadNombre = '';
                this.newUnidadSedeId = '';
                await this.loadUnidades();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al agregar unidad', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Iniciar edición de unidad
    startEditUnidad(unidad) {
        this.editUnidadId = unidad.id;
        this.editUnidadNombre = unidad.nombre;
        this.editUnidadSedeId = unidad.sede_id;
    },

    // Cancelar edición de unidad
    cancelEditUnidad() {
        this.editUnidadId = null;
        this.editUnidadNombre = '';
        this.editUnidadSedeId = '';
    },

    // Guardar edición de unidad
    async saveEditUnidad(unidad) {
        if (!this.editUnidadNombre || !this.editUnidadSedeId) return;
        this.loading = true;
        try {
            const res = await axios.put(`/api/unidades/${unidad.id}`, { 
                nombre: this.editUnidadNombre, 
                sede_id: this.editUnidadSedeId 
            });
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Unidad actualizada', 'bg-success text-white');
                this.editUnidadId = null;
                this.editUnidadNombre = '';
                this.editUnidadSedeId = '';
                await this.loadUnidades();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al actualizar unidad', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Eliminar unidad
    async deleteUnidad(unidad) {
        if (!confirm('¿Seguro que desea eliminar esta unidad?')) return;
        this.loading = true;
        try {
            const res = await axios.delete(`/api/unidades/${unidad.id}`);
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Unidad eliminada', 'bg-success text-white');
                await this.loadUnidades();
                await this.loadAreas();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al eliminar unidad', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    }
};