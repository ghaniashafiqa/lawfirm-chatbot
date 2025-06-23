<template>
  <div class="min-h-screen bg-neutralbg flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white shadow-xl rounded-xl p-8">
      <!-- Title -->
      <h2 class="text-3xl font-serif font-bold text-center text-primary mb-6">Admin Login</h2>
      <p class="text-center text-sm text-gray-500 mb-8">
        Access the lawfirm dashboard using your admin credentials.
      </p>

      <!-- Form -->
      <form @submit.prevent="onSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Enter your password"
            class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-primary text-white py-3 rounded-md font-semibold hover:bg-primary/90 transition"
        >
          🔐 Login
        </button>
      </form>

      <!-- Footer -->
      <p class="text-xs text-center text-gray-400 mt-6">
        &copy; 2025 HukumCerdas — For authorized personnel only.
      </p>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const auth = useAuthStore();
const router = useRouter();

async function onSubmit() {
  try {
    await auth.login({ username: username.value, password: password.value });
    router.push('/dashboard');
  } catch {
    alert('Login failed');
  }
}
</script>
