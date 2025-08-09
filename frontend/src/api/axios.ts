import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  const type = localStorage.getItem('type') || 'Bearer';
  if (token) {
    config.headers.Authorization = `${type} ${token}`;
  }
  return config;
});