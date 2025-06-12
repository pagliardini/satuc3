// Configuración principal de la aplicación Vue para lugares
const { createApp } = Vue;

createApp({
    data() {
        return lugaresData;
    },
    
    computed: lugaresComputed,
    
    methods: {
        ...lugaresCommonMethods,
        ...lugaresSedesMethods,
        ...lugaresUnidadesMethods,
        ...lugaresAreasMethods
    },
    
    mounted() {
        // Esperar que los interceptors estén listos
        setTimeout(() => {
            this.initializeData();
        }, 100);
    }
}).mount('#app');