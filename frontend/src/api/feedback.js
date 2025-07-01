import axios from 'axios'
import { useAuthStore } from '@/store/auth'

// const BASE_URL = 'http://localhost:5000'

const BASE_URL = 'https://lawfirm-chatbot-production.up.railway.app'

export async function sendFeedback(chatId, isPositive) {
  const authStore = useAuthStore()
  return axios.post(`${BASE_URL}/history/${chatId}/feedback`, {
    is_positive: isPositive
  }, {
    headers: {
      Authorization: `Bearer ${authStore.token}`
    }
  })
}
