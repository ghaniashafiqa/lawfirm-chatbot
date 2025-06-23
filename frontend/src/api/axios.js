import axios from 'axios';
import { useAuthStore } from '@/store/auth';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

api.interceptors.request.use(cfg => {
  const store = useAuthStore();
  if (store.token) cfg.headers.Authorization = `Bearer ${store.token}`;
  return cfg;
});

export default api;
