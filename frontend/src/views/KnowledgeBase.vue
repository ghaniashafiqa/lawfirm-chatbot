<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-primary">Knowledge Base</h1>
      <p class="text-gray-600 text-sm">Manage legal document entries used for chatbot responses.</p>
    </div>

    <!-- Upload Section -->
    <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6 mb-10">
      <h2 class="text-lg font-semibold text-primary mb-4">Upload New Legal Document</h2>
      <form @submit.prevent="handleUpload" class="grid gap-4">
        <input
          type="file"
          @change="handleFileChange"
          class="w-full border border-gray-300 rounded px-4 py-2 text-sm focus:outline-primary"
        />
        <textarea
          v-model="description"
          placeholder="Enter document description"
          rows="3"
          class="w-full border border-gray-300 rounded px-4 py-2 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
        ></textarea>
        <button
          type="submit"
          class="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary/90 transition font-medium w-fit"
        >
          Upload
        </button>
      </form>
    </div>

    <!-- Uploaded Documents Table -->
    <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6">
      <!-- Header with search -->
      <div class="mb-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <h2 class="text-lg font-semibold text-primary">Uploaded Knowledges</h2>
        <div class="flex items-center gap-2">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search documents..."
            class="px-3 py-2 border border-gray-300 rounded text-sm w-64 focus:outline-primary"
          />
          <span class="text-sm text-gray-500 hidden sm:inline">
            Showing {{ startIndex + 1 }}–{{ Math.min(startIndex + perPage, documents.length) }}
            of {{ documents.length }} {{ isSearching ? 'search results' : 'documents' }}
          </span>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-10">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
        <p class="mt-2 text-gray-600">Loading documents...</p>
      </div>

      <!-- No documents -->
      <div v-else-if="documents.length === 0" class="text-center text-gray-500 py-12">
        No documents uploaded yet.
      </div>

      <!-- Document Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full table-auto text-sm text-left">
          <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
            <tr>
              <th class="px-4 py-2">#</th>
              <th class="px-4 py-2">Filename</th>
              <th class="px-4 py-2">Description</th>
              <th class="px-4 py-2">Preview</th>
              <th class="px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="(doc, index) in paginatedDocs" :key="index" class="hover:bg-gray-50">
              <td class="px-4 py-2">{{ startIndex + index + 1 }}</td>
              <td class="px-4 py-2 font-medium text-gray-800">{{ doc.name }}</td>
              <td class="px-4 py-2 text-gray-600">{{ doc.description }}</td>
              <td class="px-4 py-2 text-gray-500 max-w-sm whitespace-pre-line truncate">
                {{ doc.text.slice(0, 200) }}...
              </td>
              <td class="px-4 py-2">
                <button @click="removeDocument(index)" class="text-sm text-red-600 hover:text-red-800">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="!loading" class="flex flex-col md:flex-row justify-between items-center mt-6 gap-4">
        <div class="text-sm text-gray-600">
          Showing {{ startIndex + 1 }}–{{ Math.min(startIndex + perPage, documents.length) }} of {{ documents.length }} documents
        </div>
        <div class="flex gap-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-4 py-1.5 border border-gray-300 rounded text-sm hover:bg-gray-100 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            @click="currentPage++"
            :disabled="currentPage >= totalPages"
            class="px-4 py-1.5 border border-gray-300 rounded text-sm hover:bg-gray-100 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const documents = ref([])
const file = ref(null)
const description = ref('')
const currentPage = ref(1)
const perPage = 10
const searchQuery = ref('')
const isSearching = ref(false)
const loading = ref(false)

const paginatedDocs = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return documents.value.slice(start, start + perPage)
})
const totalPages = computed(() => Math.ceil(documents.value.length / perPage))
const startIndex = computed(() => (currentPage.value - 1) * perPage)

function handleFileChange(event) {
  file.value = event.target.files[0]
}

async function handleUpload() {
  if (!file.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('description', description.value)

  try {
    const res = await axios.post('https://lawfirm-chatbot-production.up.railway.app/kb/upload', formData)
    console.log(res.data)

    await fetchDocuments()
    file.value = null
    description.value = ''
  } catch (err) {
    console.error(err)
    alert(err.response?.data?.error || "Upload failed")
  }
}

async function fetchDocuments() {
  loading.value = true
  try {
    const res = await axios.get("https://lawfirm-chatbot-production.up.railway.app/kb/get-data")
    documents.value = res.data.map((d) => ({
      name: d.payload?.source || "Unknown",
      description: d.payload?.description || "No description",
      text: d.payload?.text || "",
    }))
    if (currentPage.value > totalPages.value) {
      currentPage.value = totalPages.value || 1
    }
  } catch (err) {
    console.error("Failed to fetch data:", err)
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  if (!searchQuery.value) {
    await fetchDocuments()
    return
  }

  isSearching.value = true
  loading.value = true
  try {
    const res = await axios.get(`https://lawfirm-chatbot-production.up.railway.app/kb/search-data?q=${encodeURIComponent(searchQuery.value)}`)
    documents.value = res.data.map((d) => ({
      name: d.payload?.source || "Unknown",
      description: d.payload?.description || "No description",
      text: d.payload?.text || "",
    }))
    currentPage.value = 1
  } catch (err) {
    console.error("Failed to search data:", err)
  } finally {
    isSearching.value = false
    loading.value = false
  }
}

function removeDocument(index) {
  const globalIndex = startIndex.value + index
  documents.value.splice(globalIndex, 1)

  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value || 1
  }
  // Optionally send delete request
}

onMounted(fetchDocuments)
</script>

<style scoped>
.bg-neutralbg {
  background-color: #f9fafb;
}
.text-primary {
  color: #1e3a8a;
}
.bg-primary {
  background-color: #1e3a8a;
}
.hover\:bg-primary\/90:hover {
  background-color: rgba(30, 58, 138, 0.9);
}

@media (max-width: 640px) {
  .flex.justify-end {
    justify-content: center;
  }
}
</style>
