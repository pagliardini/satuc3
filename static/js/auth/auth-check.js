document.addEventListener('DOMContentLoaded', function() {
    // Verificar si el usuario está autenticado
    const token = localStorage.getItem('token');
    
    // Si estamos en la página de login y hay un token, redirigir al index
    if (window.location.pathname.includes('/login') && token) {
        window.location.href = '/';
        return;
    }
    
    // Si no estamos en login y no hay token, redirigir a login
    if (!window.location.pathname.includes('/login') && !token) {
        window.location.href = '/login';
        return;
    }
    
    // Si hay un token y no estamos en login, mostrar el nombre de usuario
    if (token && !window.location.pathname.includes('/login')) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const payload = JSON.parse(window.atob(base64));
            
            // Verificar si el token ha expirado
            const currentTime = Date.now() / 1000;
            if (payload.exp && payload.exp < currentTime) {
                localStorage.removeItem('token');
                window.location.href = '/login';
                return;
            }
            
            // Mostrar el nombre de usuario en el navbar
            const usernameDisplay = document.getElementById('username-display');
            if (usernameDisplay && payload.user_id) {
                usernameDisplay.textContent = payload.username || 'Usuario';
            }
        } catch (e) {
            console.error('Error al procesar el token:', e);
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
    }
});