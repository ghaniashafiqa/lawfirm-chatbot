<template>
  <header class="fixed w-full z-50 bg-white shadow-sm animate-slideDown">
    <nav class="max-w-7xl mx-auto px-4 py-4 md:py-5 flex justify-between items-center">
      <!-- Logo -->
      <div class="flex items-center space-x-3">
        <img src="@/assets/logo-lawfirm.png" alt="Logo" class="h-9 w-72" />
      </div>

      <!-- Desktop Nav -->
      <ul class="hidden md:flex items-center space-x-6 text-sm font-medium text-gray-700">
        <li><a href="#home" class="hover:text-primary transition-colors duration-300 ease-in-out">Home</a></li>
        <li><a href="#about" class="hover:text-primary transition">Tentang Kami</a></li>
        <li><a href="#partners" class="hover:text-primary transition">Mitra</a></li>
        <li><a href="#features" class="hover:text-primary transition">Fitur</a></li>
        <li><a href="#faq" class="hover:text-primary transition">FAQ</a></li>
        <li><a href="#contact" class="hover:text-primary transition">Kontak</a></li>
      </ul>

      <!-- CTA Button -->
      <div class="hidden md:flex">
        <router-link to="/chat">
          <button class="ml-4 px-5 py-2 bg-primary text-white font-medium rounded-md hover:bg-opacity-90 hover:scale-[1.02] transition-transform duration-300">
            💬 Chat Sekarang
          </button>
        </router-link>
      </div>

      <!-- Mobile Hamburger -->
      <button @click="toggleMenu" class="md:hidden focus:outline-none">
        <svg class="w-7 h-7 text-primary" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round"
                :d="menuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'" />
        </svg>
      </button>
    </nav>

    <!-- Mobile Dropdown -->
    <transition name="fade">
      <div v-if="menuOpen" class="md:hidden bg-white border-t px-4 pt-2 pb-3 shadow">
        <ul class="space-y-3 pt-4 text-sm font-medium text-gray-700">
          <li><a @click="closeMenu" href="#home">Home</a></li>
          <li><a @click="closeMenu" href="#about">Tentang Kami</a></li>
          <li><a @click="closeMenu" href="#partners">Mitra</a></li>
          <li><a @click="closeMenu" href="#features">Fitur</a></li>
          <li><a @click="closeMenu" href="#faq">FAQ</a></li>
          <li><a @click="closeMenu" href="#contact">Kontak</a></li>
          <li class="pt-2">
            <router-link to="/chat">
              <button class="w-full px-4 py-2 bg-primary text-white rounded-md hover:bg-opacity-90 transition">
                💬 Chat Now
              </button>
            </router-link>
          </li>
        </ul>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes slideDown {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideDown {
  animation: slideDown 0.4s ease-out;
}

</style>
