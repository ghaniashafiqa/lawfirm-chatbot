// frontend/src/store/auth.js
import { defineStore } from 'pinia'
import api from '@/api/axios'
import { parseJwt } from '@/utils/jwt'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  actions: {
    async login({ username, password }) {
      const { data } = await api.post('/auth/login', { username, password })
      this.token = data.access_token
      localStorage.setItem('token', this.token)
      this.user = parseJwt(this.token)
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
    },
    async fetchProfile() {
      const { data } = await api.get('/auth/me')
      this.user = data
    }
  }
})
