<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-primary">Chat History</h1>
      <p class="text-gray-600 text-sm">Review, audit, and export past chatbot conversations.</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
      <p class="mt-2 text-gray-600">Loading chat history...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
      <p class="text-red-700 font-medium">⚠️ Error loading chat history</p>
      <p class="text-red-600 text-sm mt-1">{{ error }}</p>
      <button 
        @click="fetchChatHistory"
        class="mt-3 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 transition"
      >
        Retry
      </button>
    </div>

    <!-- Main Content -->
    <div v-else class="bg-white border border-gray-200 shadow-md rounded-xl p-6">
      <!-- Top Bar -->
      <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-6 gap-4">
        <h2 class="text-lg font-semibold text-primary">Conversation Records</h2>
        <div class="flex gap-2">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search conversations..."
            class="px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:outline-primary w-full md:w-64"
          />
          <button
            @click="exportToCSV"
            class="bg-primary text-white px-4 py-2 rounded-md text-sm hover:bg-primary/90 transition flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export CSV
          </button>
        </div>
      </div>

      <!-- Table -->
      <div v-if="filteredConversations.length === 0" class="text-center text-gray-500 py-12">
        No conversations found matching your search.
      </div>

      <div v-else class="overflow-x-auto rounded-lg border border-gray-100">
        <table class="min-w-full text-sm text-left text-gray-700">
          <thead class="bg-accent text-gray-800 uppercase text-xs">
            <tr>
              <th class="px-4 py-3">Session ID</th>
              <th class="px-4 py-3">Question</th>
              <th class="px-4 py-3">Answer</th>
              <th class="px-4 py-3">Feedback</th>
              <th class="px-4 py-3">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in filteredConversations"
              :key="index"
              class="border-t border-gray-100 hover:bg-gray-50"
            >
              <td class="px-4 py-3 font-mono text-xs text-gray-500">{{ truncateText(item.session_id, 12) }}</td>
              <td class="px-4 py-3">{{ item.question }}</td>
              <td class="px-4 py-3 text-gray-600">{{ truncateText(item.answer, 100) }}</td>
              <td class="px-4 py-3">
                <span v-if="item.feedback === true" class="text-green-600">👍</span>
                <span v-else-if="item.feedback === false" class="text-red-600">👎</span>
                <span v-else class="text-gray-400 italic">—</span>
              </td>
              <td class="px-4 py-3 text-xs text-gray-500">{{ formatDate(item.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex flex-col md:flex-row justify-between items-center mt-6 gap-4">
        <div class="text-sm text-gray-600">
          Showing {{ filteredConversations.length }} of {{ conversations.length }} conversations
        </div>
        <div class="flex gap-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-4 py-1.5 border border-gray-300 rounded text-sm hover:bg-gray-100 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            @click="currentPage++"
            :disabled="currentPage * perPage >= conversations.length"
            class="px-4 py-1.5 border border-gray-300 rounded text-sm hover:bg-gray-100 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const conversations = ref([])
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const perPage = ref(10)

async function fetchChatHistory() {
  try {
    loading.value = true
    error.value = null

    const response = await fetch('https://lawfirm-chatbot-production.up.railway.app/history', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Failed to fetch history: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()
    conversations.value = data
  } catch (err) {
    error.value = err.message || 'Unable to fetch data'
  } finally {
    loading.value = false
  }
}

const filteredConversations = computed(() => {
  let results = conversations.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    results = results.filter(item =>
      item.question.toLowerCase().includes(query) ||
      item.answer.toLowerCase().includes(query) ||
      item.session_id.toLowerCase().includes(query)
    )
  }

  const start = (currentPage.value - 1) * perPage.value
  return results.slice(start, start + perPage.value)
})

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleString('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

function truncateText(text, maxLength) {
  return text.length > maxLength
    ? text.substring(0, maxLength) + '...'
    : text
}

function exportToCSV() {
  const headers = ['Session ID', 'Question', 'Answer', 'Feedback', 'Timestamp']
  const rows = conversations.value.map(item => [
    `"${item.session_id}"`,
    `"${item.question.replace(/"/g, '""')}"`,
    `"${item.answer.replace(/"/g, '""')}"`,
    item.feedback === true ? 'Positive' : item.feedback === false ? 'Negative' : '',
    `"${formatDate(item.created_at)}"`
  ])

  const csvContent = [headers.join(',')].concat(rows.map(r => r.join(','))).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `chat-history-${new Date().toISOString().slice(0, 10)}.csv`
  link.click()
}

onMounted(fetchChatHistory)
</script>

<style scoped>
.bg-neutralbg {
  background-color: #f9fafb;
}

.text-primary {
  color: #1e3a8a;
}

.bg-primary {
  background-color: #1e3a8a;
}

.hover\:bg-primary\/90:hover {
  background-color: rgba(30, 58, 138, 0.9);
}

.bg-accent {
  background-color: #f0f4f8;
}

.border-gray-100 {
  border-color: #f3f4f6;
}

table {
  border-collapse: separate;
  border-spacing: 0;
}

th {
  position: sticky;
  top: 0;
  z-index: 10;
}

tr {
  transition: background-color 0.2s ease;
}
</style>