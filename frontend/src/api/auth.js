import { defineStore } from 'pinia';
import api from '@/api/axios';
import { parseJwt } from '@/utils/jwt'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  actions: {
    async login(credentials) {
      const { data } = await api.post('/auth/login', credentials)
      this.token = data.access_token
      localStorage.setItem('token', this.token)

      // 🟢 Fetch full user profile
      const profileRes = await api.get('/auth/me', {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      })

      this.user = profileRes.data
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    logout() {
      this.token = '';
      this.user = null;
      localStorage.removeItem('token');
    },
    async fetchProfile() {
      const { data } = await api.get('/auth/me');
      this.user = data;
    },
  },
});
