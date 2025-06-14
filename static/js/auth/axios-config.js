// Configuración global de axios - SIN DOMContentLoaded
console.log('Configurando interceptors de axios...');

// Interceptor para agregar el token a todas las solicitudes
axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
            console.log('Token agregado a la petición:', token.substring(0, 20) + '...');
        } else {
            console.log('No hay token disponible');
        }
        return config;
    },
    error => {
        console.error('Error en interceptor de request:', error);
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores de autenticación
axios.interceptors.response.use(
    response => {
        console.log('Respuesta exitosa:', response.status);
        return response;
    },
    error => {
        console.error('Error en respuesta:', error.response?.status, error.response?.data);
        
        // Si el servidor responde con código 401 (Unauthorized)
        if (error.response && error.response.status === 401) {
            console.log('Error 401 detectado, limpiando token y redirigiendo...');
            localStorage.removeItem('token');
            
            // Solo redirigir si no estamos ya en login
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        
        return Promise.reject(error);
    }
);

console.log('Interceptors configurados correctamente');