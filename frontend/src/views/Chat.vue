<template>
  <div class="w-full h-screen flex flex-col bg-gradient-to-br from-[#f9f6f4] to-white">
    <!-- Header -->
    <!-- <header class="bg-primary text-white px-6 py-4 shadow-md flex items-center justify-between">
      <router-link to="/" class="flex items-center gap-2 text-sm hover:underline">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Kembali ke Beranda
      </router-link>
      <div class="text-lg font-serif font-bold tracking-wide">
        Hukum<span class="text-yellow-300">Cerdas</span>
      </div>
    </header> -->

    <!-- Chat Container -->
    <main class="flex-1 flex items-center justify-center px-4 py-10">
      <div class="flex flex-col flex-1 w-full h-full rounded-2xl shadow-xl bg-white border border-neutral-200 animate-fade-in-up">
        <ChatWindow />
      </div>
    </main>
  </div>
</template>

<script setup>
import ChatWindow from '@/components/ChatWindow.vue'
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out both;
}
</style>
