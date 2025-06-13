// Métodos de autenticación
const authMethods = {
    // Verifica si el usuario está autenticado
    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    // Obtiene el token almacenado
    getToken() {
        return localStorage.getItem('token');
    },

    // Guarda el token en localStorage
    setToken(token) {
        localStorage.setItem('token', token);
    },

    // Elimina el token (logout)
    removeToken() {
        localStorage.removeItem('token');
    },

    // Inicia sesión
    async login(credentials) {
        try {
            const response = await axios.post('/login', credentials);
            if (response.data.token) {
                this.setToken(response.data.token);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error de autenticación:', error);
            throw error;
        }
    },

    // Cierra sesión
    logout() {
        this.removeToken();
        
        // Mostrar mensaje de confirmación
        this.showLogoutMessage();
        
        // Redirigir después de un breve retraso
        setTimeout(() => {
            window.location.href = '/login';
        }, 1500);
    },

    // Mostrar mensaje de logout
    showLogoutMessage() {
        // Crear y mostrar un toast de confirmación
        const toastContainer = document.querySelector('.toast-container');
        if (toastContainer) {
            const toastHTML = `
                <div id="logoutToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header bg-success text-white">
                        <strong class="me-auto">Sesión cerrada</strong>
                        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                        Has cerrado sesión exitosamente. Redirigiendo...
                    </div>
                </div>
            `;
            
            toastContainer.insertAdjacentHTML('beforeend', toastHTML);
            const toast = new bootstrap.Toast(document.getElementById('logoutToast'));
            toast.show();
            
            // Limpiar el toast después de que se oculte
            setTimeout(() => {
                const toastElement = document.getElementById('logoutToast');
                if (toastElement) {
                    toastElement.remove();
                }
            }, 3000);
        } else {
            // Fallback si no hay container de toast
            alert('Sesión cerrada exitosamente');
        }
    },

    // Obtener información del usuario desde el servidor
    async getUserProfile() {
        try {
            const response = await axios.get('/api/user/profile');
            return response.data;
        } catch (error) {
            console.error('Error al obtener perfil de usuario:', error);
            return null;
        }
    },

    // Obtener el nombre de usuario desde el token (más rápido, sin llamada al servidor)
    getUsernameFromToken() {
        const payload = this.parseToken();
        return payload ? payload.username : null;
    },

    // Decodifica el token JWT (actualizado para incluir username)
    parseToken() {
        const token = this.getToken();
        if (!token) return null;
        
        try {
            // Dividir el token en partes (header.payload.signature)
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            // Decodificar la parte del payload
            const payload = JSON.parse(window.atob(base64));
            
            // Verificar si el token ha expirado
            if (payload.exp && payload.exp < Date.now() / 1000) {
                this.removeToken();
                return null;
            }
            
            return payload;
        } catch (e) {
            console.error('Error al parsear token:', e);
            return null;
        }
    },

    // Obtener información completa del usuario desde el token
    getUserInfo() {
        const payload = this.parseToken();
        if (!payload) return null;
        
        return {
            id: payload.user_id,
            username: payload.username,
            role: payload.role,
            exp: payload.exp
        };
    }
};

// Función para mostrar el nombre de usuario en el navbar
async function updateNavbarUsername() {
    const usernameDisplay = document.getElementById('username-display');
    const usernameHeader = document.getElementById('username-header');
    
    if (!usernameDisplay) return;
    
    try {
        // Mostrar "Cargando..." inicialmente
        usernameDisplay.textContent = 'Cargando...';
        
        // Primero intentar obtener el username del token (más rápido)
        const userInfo = authMethods.getUserInfo();
        
        if (userInfo && userInfo.username) {
            usernameDisplay.textContent = userInfo.username;
            if (usernameHeader) {
                usernameHeader.textContent = `${userInfo.username} (${userInfo.role})`;
            }
        } else {
            // Si no está en el token, hacer llamada al servidor
            const userProfile = await authMethods.getUserProfile();
            if (userProfile && userProfile.username) {
                usernameDisplay.textContent = userProfile.username;
                if (usernameHeader) {
                    usernameHeader.textContent = `${userProfile.username} (${userProfile.role})`;
                }
            } else {
                // Fallback
                usernameDisplay.textContent = 'Usuario';
                if (usernameHeader) {
                    usernameHeader.textContent = 'Usuario';
                }
            }
        }
    } catch (error) {
        console.error('Error al actualizar nombre de usuario:', error);
        usernameDisplay.textContent = 'Usuario';
        if (usernameHeader) {
            usernameHeader.textContent = 'Usuario';
        }
    }
}

// Función global para logout (para usar en onclick)
function logout() {
    authMethods.logout();
}

// Inicializar cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Verificar autenticación
    if (!authMethods.isAuthenticated() && !window.location.pathname.includes('/login')) {
        window.location.href = '/login';
        return;
    }
    
    // Actualizar el nombre de usuario en el navbar si estamos autenticados
    if (authMethods.isAuthenticated()) {
        updateNavbarUsername();
    }
});