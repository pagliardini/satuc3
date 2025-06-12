// Propiedades computadas para la aplicación de lugares
const lugaresComputed = {
    filteredSedes() {
        if (!this.searchSede) return this.sedes;
        const searchLower = this.searchSede.toLowerCase();
        return this.sedes.filter(s => s.nombre.toLowerCase().includes(searchLower));
    },
    
    filteredUnidades() {
        if (!this.searchUnidad) return this.unidades;
        const searchLower = this.searchUnidad.toLowerCase();
        return this.unidades.filter(u => u.nombre.toLowerCase().includes(searchLower));
    },
    
    filteredAreas() {
        if (!this.searchArea) return this.areas;
        const searchLower = this.searchArea.toLowerCase();
        return this.areas.filter(a => a.nombre.toLowerCase().includes(searchLower));
    }
};