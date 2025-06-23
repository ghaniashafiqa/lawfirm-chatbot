<template>
  <div class="min-h-screen flex flex-col bg-[#f9f6f4]">
    <!-- Header -->
    <header class="bg-primary text-white px-6 py-4 flex items-center justify-between shadow">
      <router-link to="/" class="flex items-center gap-2 hover:underline">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
        </svg>
        <span>Kembali ke Beranda</span>
      </router-link>
      <span class="font-bold text-sm">Hukum<span class="text-yellow-300">Cerdas</span></span>
    </header>

    <!-- Chat Window -->
    <div class="max-w-4xl mx-auto flex-1 overflow-hidden">
      <ChatWindow />
    </div>
  </div>
</template>

<script setup>
import ChatWindow from '@/components/ChatWindow.vue'
</script>
