<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-serif font-bold text-primary drop-shadow-sm">Knowledge Base</h1>
      <p class="text-gray-600 text-sm">Manage legal document entries used for chatbot responses.</p>
    </div>

    <!-- Upload Box -->
    <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6 mb-10">
      <h2 class="text-lg font-semibold text-primary mb-4">Upload New Legal Document</h2>
      <form @submit.prevent="handleUpload" class="space-y-4">
        <input type="file" @change="handleFileChange" class="w-full border rounded px-4 py-2 text-sm" />
        <textarea v-model="description" placeholder="Enter document description" rows="3"
          class="w-full border rounded px-4 py-2 text-sm focus:ring-2 focus:ring-primary focus:outline-none"></textarea>
        <button
          type="submit"
          class="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary/90 transition font-medium"
        >
          Upload
        </button>
      </form>
    </div>

    <!-- List of Documents -->
    <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-primary">Uploaded Documents</h2>
        <span class="text-sm text-gray-500">{{ documents.length }} total</span>
      </div>
      <div v-if="documents.length === 0" class="text-gray-500 text-center py-10">
        No documents uploaded yet.
      </div>
      <div v-else class="divide-y divide-gray-100">
        <div
          v-for="(doc, index) in documents"
          :key="index"
          class="py-4 flex justify-between items-center"
        >
          <div>
            <p class="font-medium text-gray-800">{{ doc.name }}</p>
            <p class="text-sm text-gray-500">{{ doc.description }}</p>
          </div>
          <button
            @click="removeDocument(index)"
            class="text-sm text-red-600 hover:text-red-800"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const documents = ref([])
const file = ref(null)
const description = ref('')

function handleFileChange(event) {
  file.value = event.target.files[0]
}

function handleUpload() {
  if (!file.value) return
  documents.value.push({
    name: file.value.name,
    description: description.value || 'No description provided',
  })
  file.value = null
  description.value = ''
}

function removeDocument(index) {
  documents.value.splice(index, 1)
}
</script>
