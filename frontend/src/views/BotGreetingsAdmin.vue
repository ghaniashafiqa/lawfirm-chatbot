<template>
  <div class="p-6 md:p-8 min-h-screen bg-neutral-100">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-2xl md:text-3xl font-bold text-blue-900">Opening Prompts Management</h1>
      <p class="text-gray-500 mt-1">Add, edit, and manage example questions shown by the chatbot.</p>
    </div>

    <!-- Add Prompt Form -->
    <div class="bg-white border rounded-2xl shadow-sm p-6 mb-10">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-blue-800">Add New Prompt</h2>
      </div>
      <form @submit.prevent="addGreeting" class="flex flex-col sm:flex-row gap-4">
        <input
          v-model="newGreeting"
          type="text"
          placeholder="Enter new prompt"
          class="flex-1 border rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="bg-blue-700 text-white text-sm px-6 py-2 rounded-md hover:bg-blue-800 transition"
        >
          Add
        </button>
      </form>
    </div>

    <!-- Prompt List -->
    <div class="bg-white border rounded-2xl shadow-sm p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-blue-800">Current Prompts</h2>
        <span v-if="greetings.length" class="text-sm text-gray-500">{{ greetings.length }} total</span>
      </div>

      <!-- Empty State -->
      <div v-if="greetings.length === 0" class="text-center text-gray-500 py-12">
        No prompts have been added yet.
      </div>

      <!-- Prompt List -->
      <div v-else class="divide-y divide-gray-200">
        <div
          v-for="g in greetings"
          :key="g.id"
          class="py-4 flex flex-col md:flex-row md:justify-between md:items-center gap-2 group hover:bg-gray-50 px-2 rounded-md transition"
        >
          <input
            v-model="g.text"
            class="flex-1 text-sm border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div class="flex gap-3 text-sm shrink-0 mt-2 md:mt-0 self-end md:self-center">
            <button
              @click="updateGreeting(g)"
              class="text-blue-600 hover:underline hover:text-blue-800"
            >
              Save
            </button>
            <button
              @click="confirmDelete(g.id)"
              class="text-red-600 hover:underline hover:text-red-800"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'

const greetings = ref([])
const newGreeting = ref('')

async function fetchGreetings() {
  try {
    const res = await axios.get('https://lawfirm-chatbot-production.up.railway.app/bot-greetings')
    greetings.value = res.data
  } catch (err) {
    console.error('Failed to load prompts', err)
  }
}

async function addGreeting() {
  const text = newGreeting.value.trim()
  if (!text) {
    Swal.fire('Missing input', 'Please enter a prompt first.', 'warning')
    return
  }

  try {
    const token = localStorage.getItem('token')
    await axios.post('https://lawfirm-chatbot-production.up.railway.app/bot-greetings', { text }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    newGreeting.value = ''
    fetchGreetings()
    Swal.fire('Added', 'Prompt has been added.', 'success')
  } catch (err) {
    Swal.fire('Error', 'Failed to add prompt.', 'error')
  }
}

async function updateGreeting(g) {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`https://lawfirm-chatbot-production.up.railway.app/bot-greetings/${g.id}`, {
      text: g.text
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchGreetings()
    Swal.fire('Updated', 'Prompt has been updated.', 'success')
  } catch (err) {
    Swal.fire('Error', 'Failed to update prompt.', 'error')
  }
}

function confirmDelete(id) {
  Swal.fire({
    title: 'Delete this prompt?',
    text: 'This action cannot be undone.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e3342f',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'Yes, delete it'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`https://lawfirm-chatbot-production.up.railway.app/bot-greetings/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        fetchGreetings()
        Swal.fire('Deleted!', 'Prompt has been removed.', 'success')
      } catch (err) {
        Swal.fire('Error', 'Failed to delete prompt.', 'error')
      }
    }
  })
}

onMounted(fetchGreetings)
</script>

<style scoped>
.bg-neutral-100 {
  background-color: #f9fafb;
}
</style>
