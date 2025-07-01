<template>
  <div class="min-h-screen flex flex-col bg-[#f9f6f4]">
    <!-- Header -->
    <header class="bg-primary text-white px-6 py-4 flex items-center justify-between shadow-md">
      <router-link to="/" class="flex items-center gap-2 text-sm hover:underline">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
        </svg>
        Kembali
      </router-link>
      <div class="font-semibold text-lg tracking-wide">
        <span class="text-white">Hukum</span><span class="text-yellow-300 font-bold">Cerdas</span>
      </div>
    </header>

    <!-- Chat Window -->
    <div class="max-w-4xl mx-auto flex-1 w-full">
      <ChatWindow />
    </div>
  </div>
</template>

<script setup>
import ChatWindow from '@/components/ChatWindow.vue'
</script>
