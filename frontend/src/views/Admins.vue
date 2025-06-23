<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-serif font-bold text-primary drop-shadow-sm">Admin Management</h1>
      <p class="text-gray-600 text-sm">Manage administrator accounts with full access to the system.</p>
    </div>

    <!-- Add Admin Button -->
    <div class="flex justify-end mb-4">
      <button
        @click="isModalOpen = true"
        class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary/90 transition"
      >
        + Add Admin
      </button>
    </div>

    <!-- Admins Table -->
    <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6">
      <table class="w-full text-sm text-left text-gray-700">
        <thead class="bg-accent text-gray-800 uppercase text-xs">
          <tr>
            <th class="px-4 py-3">Name</th>
            <th class="px-4 py-3">Email</th>
            <th class="px-4 py-3">Role</th>
            <th class="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(admin, index) in admins"
            :key="index"
            class="border-t border-gray-100 hover:bg-gray-50"
          >
            <td class="px-4 py-3 font-medium">{{ admin.name }}</td>
            <td class="px-4 py-3">{{ admin.email }}</td>
            <td class="px-4 py-3 capitalize">{{ admin.role }}</td>
            <td class="px-4 py-3 text-right">
              <button @click="editAdmin(index)" class="text-blue-600 text-xs mr-3 hover:underline">Edit</button>
              <button @click="deleteAdmin(index)" class="text-red-600 text-xs hover:underline">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="admins.length === 0" class="text-center text-gray-500 py-10">
        No admins registered yet.
      </div>
    </div>

    <!-- Modal -->
    <transition name="modal-fade">
      <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50">
        <div class="bg-white p-8 rounded-xl w-full max-w-lg shadow-xl">
          <h2 class="text-xl font-bold text-primary mb-4">{{ isEditing ? 'Edit Admin' : 'Add Admin' }}</h2>
          <form @submit.prevent="saveAdmin" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-1">Name</label>
              <input v-model="form.name" type="text" class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Email</label>
              <input v-model="form.email" type="email" class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Role</label>
              <select v-model="form.role" class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary">
                <option value="super">Super Admin</option>
                <option value="staff">Staff</option>
              </select>
            </div>
            <div class="flex justify-end gap-2 pt-4">
              <button type="button" @click="closeModal" class="bg-gray-200 px-4 py-2 rounded">Cancel</button>
              <button type="submit" class="bg-primary text-white px-4 py-2 rounded hover:bg-primary/90">
                {{ isEditing ? 'Update' : 'Create' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const admins = ref([
  { name: 'Nadia Rahmawati', email: 'nadia@saplaw.co.id', role: 'super' },
  { name: 'Ali Firmansyah', email: 'ali@saplaw.co.id', role: 'staff' }
])

const isModalOpen = ref(false)
const isEditing = ref(false)
const editIndex = ref(null)
const form = ref({ name: '', email: '', role: 'staff' })

function saveAdmin() {
  if (isEditing.value && editIndex.value !== null) {
    admins.value[editIndex.value] = { ...form.value }
  } else {
    admins.value.push({ ...form.value })
  }
  closeModal()
}

function editAdmin(index) {
  form.value = { ...admins.value[index] }
  editIndex.value = index
  isEditing.value = true
  isModalOpen.value = true
}

function deleteAdmin(index) {
  admins.value.splice(index, 1)
}

function closeModal() {
  form.value = { name: '', email: '', role: 'staff' }
  editIndex.value = null
  isEditing.value = false
  isModalOpen.value = false
}
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
</style>
