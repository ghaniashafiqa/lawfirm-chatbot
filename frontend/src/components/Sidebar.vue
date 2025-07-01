<template>
  <aside
    id="sidebar"
    class="w-64 h-screen sticky top-0 bg-[#1F2937] text-white flex flex-col justify-between overflow-y-auto z-30 shadow-2xl"
  >
    <!-- Logo -->
    <div class="px-6 py-6 flex flex-col items-center border-b border-white/10">
      <div
        @click="goToDashboard"
        class="cursor-pointer hover:scale-105 transition-transform duration-300"
      >
        <img
          src="@/assets/logo-lawfirm.png"
          alt="Law Firm Logo"
          class="h-12 w-auto mb-3 rounded-md shadow-md"
        />
      </div>
      <span class="text-xl font-semibold tracking-wide">
        <span class="text-yellow-400"></span>
      </span>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-5 py-6 space-y-2">
      <ul class="space-y-1">
        <li v-for="item in menuItems" :key="item.name">
          <button
            @click="item.action"
            class="group w-full flex items-center gap-3 px-4 py-2 rounded-md text-sm font-medium hover:bg-white/10 transition-all duration-200 relative"
          >
            <div class="absolute left-0 h-full w-1 bg-yellow-400 rounded-r-lg opacity-0 group-hover:opacity-100"></div>
            <component :is="item.icon" class="w-5 h-5 text-yellow-400" />
            <span class="text-white/90 group-hover:text-white">{{ item.name }}</span>
          </button>
        </li>
      </ul>
    </nav>

    <!-- User Info -->
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
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'
import {
  HomeIcon,
  DocumentMagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  UsersIcon,
  QuestionMarkCircleIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'
import { computed } from 'vue'

const router = useRouter()
const authStore = useAuthStore()

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
  { name: 'FAQ', action: () => router.push('/faq-admin'), icon: QuestionMarkCircleIcon },
  { name: 'Settings', action: () => router.push('/settings'), icon: Cog6ToothIcon }
]

function goToDashboard() {
  router.push('/dashboard')
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
/* Optional custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}
</style>
