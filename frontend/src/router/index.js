// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// Public Views
import Landing from '@/views/Landing.vue'
import Login from '@/views/Login.vue'

// Admin Views
import Dashboard from '@/views/Dashboard.vue'
import KnowledgeBase from '@/views/KnowledgeBase.vue'
import ChatHistory from '@/views/ChatHistory.vue'
import Admins from '@/views/Admins.vue'
import FAQAdmin from '@/views/FAQAdmin.vue'
import Settings from '@/views/Settings.vue'

// Chat View (Public)
import Chat from '@/views/Chat.vue'

const routes = [
  { path: '/', name: 'Landing', component: Landing },
  { path: '/login', name: 'Login', component: Login },

  // Protected Routes
  { path: '/dashboard',    name: 'Dashboard',     component: Dashboard,      meta: { requiresAuth: true } },
  { path: '/knowledge-base', name: 'KnowledgeBase', component: KnowledgeBase, meta: { requiresAuth: true } },
  { path: '/chat-history', name: 'ChatHistory',   component: ChatHistory,    meta: { requiresAuth: true } },
  { path: '/admin',        name: 'Admins',        component: Admins,         meta: { requiresAuth: true } },
  { path: '/faq-admin',    name: 'FAQAdmin',      component: FAQAdmin,       meta: { requiresAuth: true } },
  { path: '/settings',     name: 'Settings',      component: Settings,       meta: { requiresAuth: true } },

  // Chatbot (public)
  { path: '/chat',         name: 'Chat',          component: Chat }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    return next({ name: 'Login' })
  }
  next()
})

export default router