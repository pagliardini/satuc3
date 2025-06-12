// Métodos comunes para la aplicación de lugares
const lugaresCommonMethods = {
    // Inicializar datos verificando token
    initializeData() {
        const token = localStorage.getItem('token');
        if (!token) {
            this.showToast('Error', 'No hay sesión activa. Redirigiendo...', 'bg-warning text-white');
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
            return;
        }
        
        // Si hay token, cargar datos
        this.loadSedes();
        this.loadUnidades();
        this.loadAreas();
    },

    // Mostrar toast de notificación
    showToast(title, message, headerClass = '') {
        this.toastTitle = title;
        this.toastMessage = message;
        this.toastClass = headerClass;
        if (!this.resultToast) {
            this.resultToast = new bootstrap.Toast(document.getElementById('resultToast'));
        }
        this.resultToast.show();
    },

    // Obtener nombre de sede por ID
    getSedeNombre(sede_id) {
        const sede = this.sedes.find(s => s.id === sede_id);
        return sede ? sede.nombre : '—';
    },

    // Obtener nombre de unidad por ID
    getUnidadNombre(unidad_id) {
        const unidad = this.unidades.find(u => u.id === unidad_id);
        return unidad ? unidad.nombre : '—';
    }
};