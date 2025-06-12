// Métodos específicos para gestión de sedes
const lugaresSedesMethods = {
    // Cargar listado de sedes
    async loadSedes() {
        this.loading = true;
        try {
            const res = await axios.get('/api/sedes');
            this.sedes = res.data;
        } catch (e) {
            // NO manejes 401 aquí, déjalo al interceptor
            if (e.response && e.response.status !== 401) {
                this.showToast('Error', 'No se pudieron cargar las sedes.', 'bg-danger text-white');
            }
            // Si es 401, el interceptor se encargará de redirigir
        } finally {
            this.loading = false;
        }
    },

    // Agregar nueva sede
    async addSede() {
        if (!this.newSedeNombre) return;
        this.loading = true;
        try {
            const res = await axios.post('/api/sedes', { nombre: this.newSedeNombre });
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Sede agregada correctamente', 'bg-success text-white');
                this.newSedeNombre = '';
                await this.loadSedes();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al agregar sede', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Iniciar edición de sede
    startEditSede(sede) {
        this.editSedeId = sede.id;
        this.editSedeNombre = sede.nombre;
    },

    // Cancelar edición de sede
    cancelEditSede() {
        this.editSedeId = null;
        this.editSedeNombre = '';
    },

    // Guardar edición de sede
    async saveEditSede(sede) {
        if (!this.editSedeNombre) return;
        this.loading = true;
        try {
            const res = await axios.put(`/api/sedes/${sede.id}`, { nombre: this.editSedeNombre });
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Sede actualizada', 'bg-success text-white');
                this.editSedeId = null;
                this.editSedeNombre = '';
                await this.loadSedes();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al actualizar sede', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },

    // Eliminar sede
    async deleteSede(sede) {
        if (!confirm('¿Seguro que desea eliminar esta sede?')) return;
        this.loading = true;
        try {
            const res = await axios.delete(`/api/sedes/${sede.id}`);
            if (res.data.mensaje || res.data.success) {
                this.showToast('Éxito', 'Sede eliminada', 'bg-success text-white');
                await this.loadSedes();
                await this.loadUnidades();
            } else {
                this.showToast('Error', res.data.error || res.data.message, 'bg-danger text-white');
            }
        } catch (e) {
            this.showToast('Error', e.response?.data?.error || e.response?.data?.message || 'Error al eliminar sede', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    }
};