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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const faqs = ref([])
const activeIndex = ref(null)

function toggle(index) {
  activeIndex.value = activeIndex.value === index ? null : index
}

onMounted(async () => {
  try {
    const res = await axios.get('https://lawfirm-chatbot-production.up.railway.app/faq')
    faqs.value = res.data
  } catch (error) {
    console.error('Failed to fetch FAQs:', error)
  }
})
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
