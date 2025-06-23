<template>
  <div class="flex min-h-screen">
    <!-- Sidebar (only for admin pages) -->
    <Sidebar v-if="showSidebar" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <Navbar v-if="showNavbar" />
      <router-view />
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
  ['/dashboard', '/knowledge-base', '/chat-history', '/admin', '/faq-admin', '/settings'].includes(route.path)
)
</script>
