// Métodos específicos para gestión de áreas
const lugaresAreasMethods = {
    // Cargar listado de áreas
    async loadAreas() {
        this.loading = true;
        try {
            const res = await axios.get('/api/areas');
            this.areas = res.data;
        } catch (e) {
            this.showToast('Error', 'No se pudieron cargar las áreas.', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Agregar nueva área
    async addArea() {
        if (!this.newAreaNombre || !this.newAreaUnidadId) return;
        this.loading = true;
        try {
            const res = await axios.post('/api/areas', { 
                nombre: this.newAreaNombre, 
                unidad_organizativa_id: this.newAreaUnidadId 
            });
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Área agregada correctamente', 'bg-success text-white');
                this.newAreaNombre = '';
                this.newAreaUnidadId = '';
                await this.loadAreas();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al agregar área', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Iniciar edición de área
    startEditArea(area) {
        this.editAreaId = area.id;
        this.editAreaNombre = area.nombre;
        this.editAreaUnidadId = area.unidad_organizativa_id;
    },

    // Cancelar edición de área
    cancelEditArea() {
        this.editAreaId = null;
        this.editAreaNombre = '';
        this.editAreaUnidadId = '';
    },

    // Guardar edición de área
    async saveEditArea(area) {
        if (!this.editAreaNombre || !this.editAreaUnidadId) return;
        this.loading = true;
        try {
            const res = await axios.put(`/api/areas/${area.id}`, { 
                nombre: this.editAreaNombre, 
                unidad_organizativa_id: this.editAreaUnidadId 
            });
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Área actualizada', 'bg-success text-white');
                this.editAreaId = null;
                this.editAreaNombre = '';
                this.editAreaUnidadId = '';
                await this.loadAreas();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al actualizar área', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Eliminar área
    async deleteArea(area) {
        if (!confirm('¿Seguro que desea eliminar esta área?')) return;
        this.loading = true;
        try {
            const res = await axios.delete(`/api/areas/${area.id}`);
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Área eliminada', 'bg-success text-white');
                await this.loadAreas();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al eliminar área', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Marcar área como depósito
    async setDeposito(area) {
        if (!confirm('¿Seguro que desea marcar esta área como depósito?')) return;
        this.loading = true;
        try {
            const res = await axios.put(`/api/areas/${area.id}/set_deposito`);
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Área marcada como depósito', 'bg-success text-white');
                await this.loadAreas();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al marcar depósito', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    }
};