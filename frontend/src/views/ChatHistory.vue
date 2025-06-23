<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-serif font-bold text-primary drop-shadow-sm">Chat History</h1>
      <p class="text-gray-600 text-sm">Review and manage past chatbot conversations for insights and audit.</p>
    </div>

    <!-- Table Section -->
    <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-primary">Conversations</h2>
        <button
          @click="exportToCSV"
          class="bg-primary text-white px-4 py-2 rounded-md text-sm hover:bg-primary/90 transition"
        >
          ⬇️ Export CSV
        </button>
      </div>

      <div v-if="conversations.length === 0" class="text-center text-gray-500 py-10">
        No chat history available yet.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm text-left text-gray-700 border-t border-gray-100">
          <thead class="bg-accent text-gray-800 uppercase text-xs">
            <tr>
              <th class="px-4 py-3">User ID</th>
              <th class="px-4 py-3">Question</th>
              <th class="px-4 py-3">Answer</th>
              <th class="px-4 py-3">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in conversations"
              :key="index"
              class="border-t border-gray-100 hover:bg-gray-50"
            >
              <td class="px-4 py-3 font-medium">{{ item.userId }}</td>
              <td class="px-4 py-3">{{ item.question }}</td>
              <td class="px-4 py-3 text-gray-600">{{ item.answer }}</td>
              <td class="px-4 py-3 text-xs text-gray-500">{{ formatDate(item.timestamp) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const conversations = ref([
  {
    userId: 'USR-001',
    question: 'Apa perbedaan AJB dan SHM?',
    answer: 'AJB adalah Akta Jual Beli, sedangkan SHM adalah Sertifikat Hak Milik.',
    timestamp: '2025-06-19T14:35:00',
  },
  {
    userId: 'USR-002',
    question: 'Bagaimana cara balik nama sertifikat tanah?',
    answer: 'Balik nama dilakukan melalui BPN dengan syarat AJB, KTP, dan bukti pajak.',
    timestamp: '2025-06-19T15:00:00',
  },
])

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleString('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

function exportToCSV() {
  const csv = conversations.value.map(c =>
    `"${c.userId}","${c.question}","${c.answer}","${formatDate(c.timestamp)}"`
  )
  csv.unshift('"User ID","Question","Answer","Timestamp"')
  const blob = new Blob([csv.join('\n')], { type: 'text/csv' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'chat-history.csv'
  link.click()
}
</script>
