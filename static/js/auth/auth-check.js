document.addEventListener('DOMContentLoaded', function() {
    console.log('Ejecutando auth-check...');
    
    // Solo verificar token y mostrar usuario, NO hacer redirecciones
    const token = localStorage.getItem('token');
    console.log('Token encontrado:', !!token);
    
    // Si hay un token y no estamos en login, mostrar el nombre de usuario
    if (token && !window.location.pathname.includes('/login')) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const payload = JSON.parse(window.atob(base64));
            
            console.log('Payload del token:', payload);
            
            // Verificar si el token ha expirado
            const currentTime = Date.now() / 1000;
            if (payload.exp && payload.exp < currentTime) {
                console.log('Token expirado, limpiando...');
                localStorage.removeItem('token');
                return; // NO redirigir aquí, dejar que lo haga el interceptor
            }
            
            // Mostrar el nombre de usuario en el navbar
            const usernameDisplay = document.getElementById('username-display');
            if (usernameDisplay) {
                // Ahora que agregaste username al JWT, debería estar disponible
                const username = payload.username || `Usuario ${payload.user_id}`;
                usernameDisplay.textContent = username;
                console.log('Username mostrado:', username);
            } else {
                console.warn('Elemento username-display no encontrado');
            }
        } catch (e) {
            console.error('Error al procesar el token:', e);
            localStorage.removeItem('token');
        }
    }
});