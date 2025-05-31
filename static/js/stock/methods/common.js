const commonMethods = {
    async loadData() {
        this.loading = true;
        try {
            // Cargar datos en paralelo
            const [stockRes, insumosRes, areasRes, tiposRes, marcasRes, modelosRes, tonersRes, bateriasRes] = await Promise.all([
                axios.get('/api/stock'),
                axios.get('/api/stock/insumos'),
                axios.get('/api/stock/areas'),
                axios.get('/api/stock/tipos'),
                axios.get('/api/stock/marcas'),
                axios.get('/api/stock/modelos'),
                axios.get('/api/stock/toners'),
                axios.get('/api/stock/baterias')
            ]);
            
            this.stockItems = stockRes.data;
            this.insumos = insumosRes.data;
            this.areas = areasRes.data;
            this.tiposProducto = tiposRes.data;
            this.marcas = marcasRes.data;
            this.modelos = modelosRes.data;
            this.toners = tonersRes.data;
            this.baterias = bateriasRes.data;
            
        } catch (error) {
            console.error('Error cargando datos:', error);
            this.showToast('Error', 'No se pudieron cargar los datos', 'bg-danger text-white');
        } finally {
            this.loading = false;
        }
    },
    
    getEstadoBadgeClass(estado) {
        const classes = {
            'disponible': 'bg-success',
            'asignado': 'bg-primary',
            'en_reparacion': 'bg-warning',
            'baja': 'bg-danger'
        };
        return classes[estado] || 'bg-secondary';
    },
    
    formatDate(dateString) {
        if (!dateString) return '—';
        return new Date(dateString).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    showToast(title, message, headerClass = '') {
        this.toastTitle = title;
        this.toastMessage = message;
        this.toastClass = headerClass;
        if (!this.resultToast) {
            this.resultToast = new bootstrap.Toast(document.getElementById('resultToast'));
        }
        this.resultToast.show();
    }
};