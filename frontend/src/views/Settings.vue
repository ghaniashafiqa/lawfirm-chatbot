<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-serif font-bold text-primary">Settings</h1>
      <p class="text-gray-600 text-sm">Manage your profile information and change your password.</p>
    </div>

    <!-- Settings Form -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-md p-8 max-w-2xl">
      <form @submit.prevent="updateSettings" class="space-y-6">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input
            v-model="form.username"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
          />
        </div>

        <!-- Role (readonly) -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
          <input
            v-model="form.role"
            class="w-full px-4 py-2 border border-gray-200 bg-gray-100 rounded-md text-gray-600 cursor-not-allowed"
            disabled
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Leave blank to keep current"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
          />
        </div>

        <!-- Submit Button -->
        <div class="flex justify-end">
          <button
            type="submit"
            class="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary/90 transition font-medium"
          >
            Save Changes
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const form = ref({
  username: '',
  email: '',
  role: '',
  password: ''
})

const userId = ref(null)

async function fetchProfile() {
  const { data } = await api.get('/auth/me')
  form.value.username = data.username
  form.value.email    = data.email
  form.value.role     = data.role
  userId.value        = data.id
}

async function updateSettings() {
  const payload = {
    username: form.value.username,
    email:    form.value.email,
  }
  if (form.value.password) payload.password = form.value.password

  await api.put(`/admin/${userId.value}`, payload)
  alert('✅ Settings updated successfully!')
}

onMounted(fetchProfile)
</script>
