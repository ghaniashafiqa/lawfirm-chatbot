<template>
  <div class="p-6 md:p-8 min-h-screen bg-neutral-100">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl md:text-3xl font-bold text-blue-900">FAQ Management</h1>
      <p class="text-gray-500 mt-1">Manage frequently asked questions used by the chatbot.</p>
    </div>

    <!-- Form Section -->
    <div class="bg-white border rounded-2xl shadow-sm p-6 mb-10">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-blue-800">
          {{ form.id ? 'Update FAQ' : 'Add New FAQ' }}
        </h2>
        <span v-if="form.id" @click="resetForm" class="text-sm text-blue-500 hover:underline cursor-pointer">
          Cancel Edit
        </span>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <input
          v-model="form.question"
          type="text"
          placeholder="Enter FAQ question"
          class="w-full border rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          v-model="form.answer"
          rows="4"
          placeholder="Enter answer"
          class="w-full border rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
        <button
          type="submit"
          class="bg-blue-700 text-white text-sm px-6 py-2 rounded-md hover:bg-blue-800 transition"
        >
          {{ form.id ? 'Update FAQ' : 'Add FAQ' }}
        </button>
      </form>
    </div>

    <!-- FAQ List Section -->
    <div class="bg-white border rounded-2xl shadow-sm p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-blue-800">Current FAQs</h2>
        <span v-if="faqs.length" class="text-sm text-gray-500">{{ faqs.length }} total</span>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-10 text-gray-500">
        <div class="animate-spin inline-block h-8 w-8 border-4 border-blue-300 border-t-transparent rounded-full"></div>
        <p class="mt-2">Loading FAQs...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="faqs.length === 0" class="text-center text-gray-500 py-12">
        No FAQs have been added yet.
      </div>

      <!-- FAQ List -->
      <div v-else class="divide-y divide-gray-200">
        <div
          v-for="faq in paginatedFaqs"
          :key="faq.id"
          class="py-4 flex flex-col md:flex-row md:justify-between md:items-center gap-2 group hover:bg-gray-50 px-2 rounded-md transition"
        >
          <div>
            <h3 class="text-base font-medium text-gray-800">{{ faq.question }}</h3>
            <p class="text-sm text-gray-600 mt-1 whitespace-pre-line">{{ faq.answer }}</p>
          </div>
          <div class="flex gap-3 text-sm shrink-0 mt-2 md:mt-0 self-end md:self-center">
            <button
              @click="editFAQ(faq)"
              class="text-blue-600 hover:underline hover:text-blue-800"
            >
              Edit
            </button>
            <button
              @click="confirmDelete(faq.id)"
              class="text-red-600 hover:underline hover:text-red-800"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center mt-6">
        <button
          class="px-3 py-1 mx-1 rounded-md text-sm border border-gray-300 hover:bg-gray-100"
          :class="{ 'bg-blue-100 text-blue-800 font-semibold': currentPage === page }"
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'

const faqs = ref([])
const loading = ref(false)
const form = ref({ id: null, question: '', answer: '' })

// Pagination
const currentPage = ref(1)
const pageSize = 5

const totalPages = computed(() => Math.ceil(faqs.value.length / pageSize))
const paginatedFaqs = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return faqs.value.slice(start, start + pageSize)
})

async function fetchFAQs() {
  loading.value = true
  try {
    const res = await axios.get('https://lawfirm-chatbot-production.up.railway.app/faq')
    faqs.value = res.data
  } catch (e) {
    console.error('Error fetching FAQs:', e)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  const trimmedQuestion = form.value.question.trim()
  const trimmedAnswer = form.value.answer.trim()

  if (!trimmedQuestion || !trimmedAnswer) {
    Swal.fire('Incomplete', 'Please enter both a question and an answer.', 'warning')
    return
  }

  try {
    const token = localStorage.getItem('token')
    const headers = { Authorization: `Bearer ${token}` }

    if (form.value.id) {
      await axios.put(`https://lawfirm-chatbot-production.up.railway.app/faq/${form.value.id}`, {
        question: trimmedQuestion,
        answer: trimmedAnswer
      }, { headers })
      Swal.fire('Updated', 'FAQ updated successfully.', 'success')
    } else {
      await axios.post(`https://lawfirm-chatbot-production.up.railway.app/faq`, {
        question: trimmedQuestion,
        answer: trimmedAnswer
      }, { headers })
      Swal.fire('Added', 'FAQ added successfully.', 'success')
    }

    resetForm()
    fetchFAQs()
  } catch (err) {
    Swal.fire('Error', 'Failed to save FAQ.', 'error')
  }
}

function editFAQ(faq) {
  form.value = { ...faq }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function resetForm() {
  form.value = { id: null, question: '', answer: '' }
}

function confirmDelete(id) {
  Swal.fire({
    title: 'Delete FAQ?',
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
        await axios.delete(`https://lawfirm-chatbot-production.up.railway.app/faq/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        fetchFAQs()
        Swal.fire('Deleted!', 'FAQ has been deleted.', 'success')
      } catch (err) {
        Swal.fire('Error', 'Failed to delete FAQ.', 'error')
      }
    }
  })
}

onMounted(fetchFAQs)
</script>

<style scoped>
.bg-neutral-100 {
  background-color: #f9fafb;
}
</style>
