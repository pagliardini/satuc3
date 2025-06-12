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
        window.location.href = '/login';
    },

    // Decodifica el token JWT (para obtener datos como el rol)
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

    // Obtener el rol del usuario desde el token
    getUserRole() {
        const payload = this.parseToken();
        return payload ? payload.role : null;
    }
};