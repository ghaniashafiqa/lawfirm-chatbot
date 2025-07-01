<template>
  <div class="flex flex-col h-[75vh]">
    <!-- Greeting -->
    <div class="p-6">
      <div class="flex items-start gap-4 bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
        <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-semibold text-sm">
          HC
        </div>
        <div>
          <p class="font-semibold text-lg text-gray-800 mb-1">
            Selamat datang di <span class="text-primary">Hukum Cerdas</span> 👋
          </p>
          <p class="text-gray-600 text-sm">
            Saya dapat membantu menjawab pertanyaan hukum seputar agraria, dokumen tanah, dan lainnya.
          </p>
          <div class="flex flex-wrap gap-2 mt-4">
            <button
              v-for="example in examples"
              :key="example"
              @click="fillQuestion(example)"
              class="text-sm px-4 py-2 rounded-full border border-primary text-primary hover:bg-primary hover:text-white transition duration-200"
            >
              + {{ example }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto px-6 pb-4 space-y-6">
      <div v-for="msg in messages" :key="msg.id" class="space-y-2">
        <!-- User Message -->
        <div class="flex justify-end">
          <div class="bg-primary text-white rounded-2xl px-4 py-3 max-w-[75%] text-sm shadow">
            {{ msg.question }}
          </div>
        </div>

        <!-- Bot Message -->
        <div class="flex justify-start">
          <div class="bg-gray-100 rounded-2xl px-4 py-3 text-sm text-gray-800 max-w-[75%] shadow relative">
            {{ msg.answer }}
            <div class="flex items-center gap-2 mt-2 text-gray-500" v-if="msg.feedback !== null || !isLoading">
              <button
                @click="sendFeedbackHandler(msg.id, true)"
                :class="msg.feedback === true ? 'text-green-600' : 'hover:text-green-500'"
                title="Bermanfaat"
              >
                👍
              </button>
              <button
                @click="sendFeedbackHandler(msg.id, false)"
                :class="msg.feedback === false ? 'text-red-600' : 'hover:text-red-500'"
                title="Tidak membantu"
              >
                👎
              </button>
              <button
                @click="copyToClipboard(msg.answer)"
                class="ml-2 text-blue-500 hover:text-blue-700"
                title="Salin jawaban"
              >
                📋
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading bubble -->
      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-gray-100 rounded-2xl px-4 py-3 text-sm text-gray-500 max-w-[75%] shadow italic animate-pulse">
          Sedang mengetik<span class="dot">...</span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <form @submit.prevent="ask" class="px-6 py-4 bg-white shadow-inner flex items-center gap-3 border-t border-gray-200">
      <input
        v-model="question"
        type="text"
        placeholder="Ketik pertanyaan hukum Anda..."
        class="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:ring-2 focus:ring-primary focus:outline-none text-sm"
        :disabled="isLoading"
      />
      <button
        type="submit"
        :disabled="isLoading"
        class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center hover:bg-opacity-90 transition disabled:opacity-50"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"
             viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { sendQuestion } from '@/api/chat'
import { sendFeedback } from '@/api/feedback'

const sessionId = Date.now().toString()
const question = ref('')
const messages = ref([])
const isLoading = ref(false)

const examples = [
  'Bagaimana cara balik nama sertifikat tanah?',
  'Apa itu mafia tanah?',
  'Apa Itu Konflik Agraria?',
  'Contoh-contoh Kasus Sengketa Tanah Fenomenal di Indonesia',
]

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
