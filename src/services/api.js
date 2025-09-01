import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Tu backend en Laravel
  withCredentials: true, // Para que funcione con Sanctum
});

export default api;