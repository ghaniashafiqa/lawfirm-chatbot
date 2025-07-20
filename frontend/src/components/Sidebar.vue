<template>
  <div>
    <!-- Mobile Toggle Button -->
    <button
      class="md:hidden fixed top-4 left-4 z-40 bg-gray-800 text-white p-2 rounded-md"
      @click="isSidebarOpen = !isSidebarOpen"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-0 left-0 w-64 h-screen z-30 bg-[#1F2937] text-white shadow-2xl flex flex-col justify-between transition-transform duration-300',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'md:translate-x-0 md:relative md:flex'
      ]"
    >
      <!-- Top Section: Logo -->
      <div class="px-6 py-6 flex flex-col items-center border-b border-white/10">
        <div @click="goToDashboard" class="cursor-pointer hover:scale-105 transition-transform duration-300">
          <img src="@/assets/logo-lawfirm.png" alt="Logo" class="h-12 w-auto mb-3 rounded-md shadow-md" />
        </div>
        <span class="text-xl font-semibold tracking-wide text-yellow-400"></span>
      </div>

      <!-- Middle Section: Navigation -->
      <nav class="flex-1 px-5 py-4 overflow-y-auto">
        <ul class="space-y-1">
          <li v-for="item in menuItems" :key="item.name">
            <button
              @click="handleMenuClick(item.action)"
              class="group w-full flex items-center gap-3 px-4 py-2 rounded-md text-sm font-medium hover:bg-white/10 transition-all duration-200 relative"
            >
              <div class="absolute left-0 h-full w-1 bg-yellow-400 rounded-r-lg opacity-0 group-hover:opacity-100"></div>
              <component :is="item.icon" class="w-5 h-5 text-yellow-400" />
              <span class="text-white/90 group-hover:text-white">{{ item.name }}</span>
            </button>
          </li>
        </ul>
      </nav>

      <!-- Bottom Section: User Info & Logout -->
      <div class="p-4 border-t border-white/10">
        <div class="flex items-center mb-4">
          <div class="relative">
            <div class="w-10 h-10 rounded-full bg-yellow-400 text-primary flex items-center justify-center font-bold shadow-inner">
              {{ userInitials }}
            </div>
            <span class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-[#1F2937]"></span>
          </div>
          <div class="ml-3">
            <p class="text-sm font-semibold text-white">{{ authStore.user?.username || 'Admin' }}</p>
            <p class="text-xs text-white/60">{{ authStore.user?.role || 'Super Admin' }}</p>
          </div>
        </div>
        <button
          @click="confirmLogout"
          class="w-full bg-red-500 hover:bg-red-600 text-white text-sm font-medium px-4 py-2 rounded-md transition"
        >
          Logout
        </button>
      </div>
    </aside>

    <!-- Backdrop for mobile -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black bg-opacity-40 z-20 md:hidden"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Swal from 'sweetalert2'
import {
  HomeIcon,
  DocumentMagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  UsersIcon,
  QuestionMarkCircleIcon,
  Cog6ToothIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const isSidebarOpen = ref(false)

const userInitials = computed(() => {
  const name = authStore.user?.username || ''
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .slice(0, 2)
})

const menuItems = [
  { name: 'Dashboard', action: () => router.push('/dashboard'), icon: HomeIcon },
  { name: 'Knowledge Base', action: () => router.push('/knowledge-base'), icon: DocumentMagnifyingGlassIcon },
  { name: 'Chat History', action: () => router.push('/chat-history'), icon: ChatBubbleLeftRightIcon },
  { name: 'Admins', action: () => router.push('/admin'), icon: UsersIcon },
  { name: 'FAQs', action: () => router.push('/faq-admin'), icon: QuestionMarkCircleIcon },
  { name: 'Opening Prompts', action: () => router.push('/bot-greetings'), icon: SparklesIcon },
  { name: 'Settings', action: () => router.push('/settings'), icon: Cog6ToothIcon }
]

function goToDashboard() {
  router.push('/dashboard')
}

function handleMenuClick(action) {
  action()
  isSidebarOpen.value = false
}

function confirmLogout() {
  Swal.fire({
    title: 'Logout?',
    text: 'You will be redirected to the login page.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, logout',
    cancelButtonText: 'Cancel'
  }).then(result => {
    if (result.isConfirmed) {
      authStore.logout()
      router.push('/login')
    }
  })
}
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}
</style>
