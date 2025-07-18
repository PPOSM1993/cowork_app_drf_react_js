import axios from 'axios';

const API_KEY = 'c7b6156d-e86d-4cab-a2a0-fa918faa1eae';  // Mejor si la cargas desde una variable de entorno

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
