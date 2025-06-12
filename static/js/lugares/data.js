// Variables reactivas para la aplicación de lugares
const lugaresData = {
    tab: 'sedes',
    sedes: [],
    unidades: [],
    areas: [],
    searchSede: '',
    searchUnidad: '',
    searchArea: '',
    loading: false,
    
    // Sedes
    newSedeNombre: '',
    editSedeId: null,
    editSedeNombre: '',
    
    // Unidades
    newUnidadNombre: '',
    newUnidadSedeId: '',
    editUnidadId: null,
    editUnidadNombre: '',
    editUnidadSedeId: '',
    
    // Áreas
    newAreaNombre: '',
    newAreaUnidadId: '',
    editAreaId: null,
    editAreaNombre: '',
    editAreaUnidadId: '',
    
    // Toast
    toastMessage: '',
    toastTitle: '',
    toastClass: '',
    resultToast: null
};