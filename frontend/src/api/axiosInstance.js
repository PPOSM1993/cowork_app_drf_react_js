import axios from 'axios';

const API_KEY = '<TU_API_KEY_AQUI>';  // Mejor si la cargas desde una variable de entorno

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'X-API-KEY': API_KEY,
    },
});

// Interceptor para agregar token automáticamente
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default axiosInstance;
