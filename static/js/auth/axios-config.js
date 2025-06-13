document.addEventListener('DOMContentLoaded', function() {
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

    // Interceptor para manejar errores de autenticación
    axios.interceptors.response.use(
        response => response,
        error => {
            // Si el servidor responde con código 401 (Unauthorized) o 403 (Forbidden)
            if (error.response && (error.response.status === 401 || error.response.status === 403)) {
                console.log('Error 401 o 403 detectado, limpiando token...');
                localStorage.removeItem('token');
                
                // Mostrar mensaje
                const toast = document.getElementById('authErrorToast');
                if (toast) {
                    const toastInstance = new bootstrap.Toast(toast);
                    toastInstance.show();
                } else {
                    console.warn('No se encontró el toast de error de autenticación');
                }
                
                // Redirigir después de un breve retraso
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            }
            return Promise.reject(error);
        }
    );
});