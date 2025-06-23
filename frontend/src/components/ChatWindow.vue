<template>
  <div class="flex flex-col h-[75vh]">
    <!-- Greeting -->
    <div class="p-6">
      <div class="flex items-start gap-4 bg-[#fff9f7] border border-accent/30 rounded-xl p-5 shadow-sm">
        <div class="w-10 h-10 rounded-full bg-accent text-white flex items-center justify-center font-bold">
          HC
        </div>
        <div>
          <p class="font-bold text-lg text-neutral-800 mb-1">Halo, selamat datang di <span class="text-accent">Hukum Cerdas</span>!</p>
          <p class="text-gray-700 text-sm leading-relaxed">
            Chatbot ini dapat membantu Anda memahami prosedur hukum, sengketa tanah, atau dokumen penting lainnya.
          </p>
          <div class="flex flex-wrap gap-2 mt-4">
            <button v-for="example in examples" :key="example" @click="fillQuestion(example)"
              class="text-sm px-4 py-2 border border-accent text-accent rounded-full hover:bg-accent hover:text-white transition">
              + {{ example }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto px-6 space-y-4">
      <div v-for="msg in messages" :key="msg.id" class="space-y-2">
        <!-- User -->
        <div class="text-right">
          <div class="inline-block bg-primary text-white rounded-xl px-4 py-3 text-sm max-w-xs text-left shadow">
            {{ msg.question }}
          </div>
        </div>
        <!-- Bot -->
        <div class="text-left">
          <div class="inline-block bg-accentSoft rounded-xl px-4 py-3 text-sm text-gray-800 max-w-xs shadow">
            {{ msg.answer }}
          </div>
        </div>
      </div>
    </div>

    <!-- Sticky Input -->
    <form @submit.prevent="ask" class="px-6 py-4 bg-white shadow-inner flex items-center gap-3">
      <input
        v-model="question"
        type="text"
        placeholder="Ketik pertanyaan hukum Anda..."
        class="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:ring-2 focus:ring-accent focus:outline-none text-sm"
      />
      <button
        type="submit"
        class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center hover:bg-opacity-90 transition"
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
import { ref } from 'vue'
import { sendQuestion } from '@/api/chat'

const sessionId = Date.now().toString()
const question = ref('')
const messages = ref([])

const examples = [
  'Bagaimana cara balik nama sertifikat tanah?',
  'Apa itu mafia tanah?',
  'Apa perbedaan AJB dan SHM?',
  'Langkah hukum jika tanah diserobot?',
]

function fillQuestion(q) {
  question.value = q
  ask()
}

async function ask() {
  const q = question.value.trim()
  if (!q) return
  question.value = ''
  try {
    const { data } = await sendQuestion(sessionId, q)
    messages.value.push({
      id: messages.value.length,
      question: q,
      answer: data.answer || '[Tidak ada jawaban]',
    })
  } catch {
    messages.value.push({
      id: messages.value.length,
      question: q,
      answer: '⚠️ Maaf, terjadi kesalahan. Silakan coba lagi.',
    })
  }
}
</script>

<style scoped>
/* scrollbar tweak (optional) */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}
</style>
