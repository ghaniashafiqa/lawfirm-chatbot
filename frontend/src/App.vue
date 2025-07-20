<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar (only for admin pages) -->
    <Sidebar v-if="showSidebar" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col bg-gray-100">
      <!-- Sticky Navbar -->
      <Navbar v-if="showNavbar" class="sticky top-0 z-50 shadow bg-white" />

      <!-- Scrollable Content Area -->
      <div class="flex-1 overflow-y-auto p-4">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'

const route = useRoute()

// Only show Navbar on landing page
const showNavbar = computed(() => route.path === '/')

// Only show Sidebar on admin pages
const showSidebar = computed(() =>
  ['/dashboard', '/knowledge-base', '/chat-history', '/admin', '/faq-admin', '/bot-greetings', '/settings'].includes(route.path)
)
</script>
