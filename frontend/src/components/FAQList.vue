<template>
  <div class="space-y-4">
    <div
      v-for="(faq, index) in faqs"
      :key="index"
      class="bg-white border border-gray-200 rounded-xl shadow-sm transition hover:shadow-md"
    >
      <button
        @click="toggle(index)"
        class="w-full px-6 py-5 flex justify-between items-center text-left"
      >
        <h3 class="text-lg font-semibold text-primary">
          {{ faq.question }}
        </h3>
        <svg
          :class="[
            'w-5 h-5 text-accent transform transition-transform duration-200',
            activeIndex === index ? 'rotate-180' : 'rotate-0'
          ]"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      <transition name="fade">
        <div v-show="activeIndex === index" class="px-6 pb-5 text-gray-700 text-base leading-relaxed">
          {{ faq.answer }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeIndex = ref(null)

function toggle(index) {
  activeIndex.value = activeIndex.value === index ? null : index
}

const faqs = [
  {
    question: 'Apakah chatbot ini bisa menggantikan pengacara?',
    answer:
      'Tidak. Chatbot ini hanya memberikan informasi dari dokumen hukum terpercaya. Untuk tindakan hukum atau konsultasi lanjutan, silakan hubungi pengacara profesional seperti tim dari SAP Lawfirm.',
  },
  {
    question: 'Apa itu RAG (Retrieval-Augmented Generation)?',
    answer:
      'RAG adalah pendekatan AI yang mencari informasi dari dokumen eksternal dan menggunakannya untuk menjawab pertanyaan. Chatbot ini menggunakan RAG dengan OpenAI atau DeepSeek, bukan model yang di-finetune.',
  },
  {
    question: 'Apakah jawaban chatbot ini legal dan akurat?',
    answer:
      'Jawaban bersumber dari dokumen hukum resmi yang disediakan oleh SAP Lawfirm. Namun, chatbot tidak menjamin keakuratan 100% dan tidak dapat digunakan sebagai dasar keputusan hukum final.',
  },
  {
    question: 'Apa saja topik yang bisa ditanyakan?',
    answer:
      'Topik seperti sengketa tanah, mafia tanah, dokumen kepemilikan, proses balik nama, hingga pencegahan penipuan tanah. Pertanyaan akan dijawab berdasarkan isi dokumen hukum terkait.',
  },
  {
    question: 'Bagaimana cara menghubungi pengacara jika butuh bantuan lanjutan?',
    answer:
      'Anda dapat menghubungi SAP Lawfirm melalui website resmi di https://saplawfirm.com atau melalui halaman kontak kami.',
  },
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
