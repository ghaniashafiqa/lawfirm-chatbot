<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { sendQuestion } from '@/api/chat'
import { sendFeedback } from '@/api/feedback'

const sessionId = Date.now().toString()
const question = ref('')
const messages = ref([])
const isLoading = ref(false)
const greetings = ref([])
const greetingsLoading = ref(true)

onMounted(fetchGreetings)

async function fetchGreetings() {
  greetingsLoading.value = true
  try {
    const { data } = await axios.get('https://lawfirm-chatbot-production.up.railway.app/bot-greetings')
    greetings.value = data
  } catch (err) {
    console.error('Failed to fetch greetings:', err)
  } finally {
    greetingsLoading.value = false
  }
}

function fillQuestion(q) {
  question.value = q
  ask()
}

async function ask() {
  const q = question.value.trim()
  if (!q) return
  question.value = ''
  isLoading.value = true

  await nextTick(() => {
    const el = document.querySelector('.overflow-y-auto')
    if (el) el.scrollTop = el.scrollHeight
  })

  try {
    const { data } = await sendQuestion(sessionId, q)
    messages.value.push({
      id: data.chat_id,
      question: q,
      answer: data.answer || '[Tidak ada jawaban]',
      feedback: null
    })
  } catch {
    messages.value.push({
      id: Date.now(),
      question: q,
      answer: '⚠️ Maaf, terjadi kesalahan. Silakan coba lagi.',
      feedback: null
    })
  } finally {
    isLoading.value = false
    await nextTick(() => {
      const el = document.querySelector('.overflow-y-auto')
      if (el) el.scrollTop = el.scrollHeight
    })
  }
}

async function sendFeedbackHandler(chatId, isPositive) {
  try {
    await sendFeedback(chatId, isPositive)
    const index = messages.value.findIndex(m => m.id === chatId)
    if (index !== -1) messages.value[index].feedback = isPositive
  } catch (err) {
    alert('❌ Gagal mengirim feedback')
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('✅ Jawaban disalin ke clipboard')
  }, () => {
    alert('❌ Gagal menyalin')
  })
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Top Section -->
    <div class="p-6 border-b border-gray-200 bg-neutral-50">
      <div class="flex items-center gap-4">
        <!-- Back Button -->
        <router-link
          to="/"
          class="flex items-center gap-2 text-primary hover:underline text-sm"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"
            viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Kembali
        </router-link>

        <!-- Avatar -->
        <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold">
          HC
        </div>

        <!-- Welcome -->
        <div>
          <h1 class="text-lg font-semibold text-gray-800">
            Selamat datang di <span class="text-primary">Hukum Cerdas</span> 👋
          </h1>
          <p class="text-sm text-gray-600 mt-1">
            Ajukan pertanyaan hukum pertanahan, sertifikasi tanah, dan lainnya.
          </p>
          <div class="flex flex-wrap gap-2 mt-4">
            <template v-if="greetingsLoading">
              <p class="text-sm text-gray-400 italic">Memuat contoh pertanyaan...</p>
            </template>
            <template v-else-if="greetings.length === 0">
              <p class="text-sm text-gray-400 italic">Belum ada contoh pertanyaan</p>
            </template>
            <template v-else>
              <button
                v-for="greeting in greetings"
                :key="greeting.id"
                @click="fillQuestion(greeting.text)"
                class="text-sm px-4 py-1.5 rounded-full border border-primary text-primary hover:bg-primary hover:text-white transition"
              >
                + {{ greeting.text }}
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Body -->
    <div class="flex-1 overflow-y-auto px-6 py-4 space-y-6 bg-white">
      <div v-for="msg in messages" :key="msg.id" class="space-y-2">
        <!-- User Message -->
        <div class="flex justify-end">
          <div class="bg-primary text-white rounded-2xl px-4 py-3 max-w-[75%] text-sm shadow">
            {{ msg.question }}
          </div>
        </div>

        <!-- Bot Response -->
        <div class="flex justify-start">
          <div class="bg-gray-50 rounded-2xl px-4 py-3 text-sm text-gray-800 max-w-[75%] shadow relative border border-gray-200">
            {{ msg.answer }}
            <div class="flex items-center gap-3 mt-2 text-gray-500 text-xs" v-if="msg.feedback !== null || !isLoading">
              <button
                @click="sendFeedbackHandler(msg.id, true)"
                :class="msg.feedback === true ? 'text-green-600' : 'hover:text-green-500'"
                title="Bermanfaat"
              >👍</button>
              <button
                @click="sendFeedbackHandler(msg.id, false)"
                :class="msg.feedback === false ? 'text-red-600' : 'hover:text-red-500'"
                title="Tidak membantu"
              >👎</button>
              <button
                @click="copyToClipboard(msg.answer)"
                class="ml-2 text-blue-500 hover:text-blue-700"
                title="Salin jawaban"
              >📋</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Typing State -->
      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-gray-100 rounded-2xl px-4 py-3 text-sm text-gray-500 max-w-[75%] shadow italic animate-pulse">
          Mengetik jawaban...
        </div>
      </div>
    </div>

    <!-- Chat Input -->
    <form @submit.prevent="ask" class="flex items-center gap-3 border-t border-gray-200 px-6 py-4 bg-neutral-50">
      <input
        v-model="question"
        type="text"
        placeholder="Tanyakan sesuatu..."
        class="flex-1 px-4 py-3 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        :disabled="isLoading"
      />
      <button
        type="submit"
        :disabled="isLoading"
        class="w-10 h-10 flex items-center justify-center rounded-full bg-primary text-white hover:bg-opacity-90 disabled:opacity-50 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"
          viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </button>
    </form>
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}
.dot::after {
  content: "...";
  animation: dots 1.5s steps(3, end) infinite;
}
@keyframes dots {
  0%, 20% {
    content: "";
  }
  40% {
    content: ".";
  }
  60% {
    content: "..";
  }
  80%, 100% {
    content: "...";
  }
}
</style>
