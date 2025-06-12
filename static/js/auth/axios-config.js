// Configuración global de axios
// Interceptor para agregar el token a todas las solicitudes
axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
            console.log('Token agregado a la petición:', token.substring(0, 20) + '...'); // Debug
        } else {
            console.log('No hay token disponible'); // Debug
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores de autenticación - MÁS SIMPLE
axios.interceptors.response.use(
    response => response,
    error => {
        // Si el servidor responde con código 401 (Unauthorized)
        if (error.response && error.response.status === 401) {
            console.log('Error 401 detectado, limpiando token...');
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);