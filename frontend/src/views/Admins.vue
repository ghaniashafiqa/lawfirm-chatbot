<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-primary">Admin Management</h1>
      <p class="text-gray-600 text-sm">Manage administrator accounts with full access to the system.</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
      <p class="mt-2 text-gray-600">Loading administrators...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
      <p class="text-red-700 font-medium">⚠️ Error loading administrators</p>
      <p class="text-red-600 text-sm mt-1">{{ error }}</p>
      <button 
        @click="fetchAdmins"
        class="mt-3 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 transition"
      >
        Retry
      </button>
    </div>

    <!-- Main Content -->
    <div v-else>
      <!-- Add Admin Button -->
      <div class="flex justify-end mb-4">
        <button
          @click="openAddModal"
          class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary/90 transition flex items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd" />
          </svg>
          Add Admin
        </button>
      </div>

      <!-- Admins Table -->
      <div class="bg-white border border-gray-200 shadow-md rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-primary">Administrators</h2>
          <div class="flex items-center">
            <span class="text-sm text-gray-600 mr-3">Total: {{ admins.length }}</span>
            <input
              v-model="searchQuery"
              placeholder="Search admins..."
              class="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-primary"
            />
          </div>
        </div>

        <div v-if="filteredAdmins.length === 0" class="text-center text-gray-500 py-10">
          No administrators found
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-700 border-t border-gray-100">
            <thead class="bg-accent text-gray-800 uppercase text-xs">
              <tr>
                <th class="px-4 py-3">Username</th>
                <th class="px-4 py-3">Email</th>
                <th class="px-4 py-3">Role</th>
                <th class="px-4 py-3">Created</th>
                <th class="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="admin in filteredAdmins"
                :key="admin.id"
                class="border-t border-gray-100 hover:bg-gray-50"
              >
                <td class="px-4 py-3 font-medium">{{ admin.username }}</td>
                <td class="px-4 py-3">{{ admin.email }}</td>
                <td class="px-4 py-3">
                  <span 
                    :class="{
                      'bg-purple-100 text-purple-800': admin.role === 'super',
                      'bg-blue-100 text-blue-800': admin.role === 'admin',
                      'bg-gray-100 text-gray-800': admin.role === 'staff'
                    }"
                    class="capitalize px-2.5 py-0.5 rounded-full text-xs"
                  >
                    {{ admin.role }}
                  </span>
                </td>
                <td class="px-4 py-3 text-xs text-gray-500">{{ formatDate(admin.created_at) }}</td>
                <td class="px-4 py-3 text-right">
                  <button 
                    @click="editAdmin(admin)"
                    class="text-blue-600 hover:text-blue-800 p-1 rounded-full hover:bg-blue-50"
                    title="Edit"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                  <button 
                    @click="confirmDelete(admin)"
                    class="text-red-600 hover:text-red-800 p-1 ml-2 rounded-full hover:bg-red-50"
                    title="Delete"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="flex justify-between items-center mt-4">
            <div class="text-sm text-gray-600">
              Showing {{ filteredAdmins.length }} of {{ admins.length }} administrators
            </div>
            <div class="flex gap-2">
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-1 border rounded text-sm disabled:opacity-50"
              >
                Previous
              </button>
              <button
                @click="currentPage++"
                :disabled="currentPage * perPage >= admins.length"
                class="px-3 py-1 border rounded text-sm disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <transition name="modal-fade">
      <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50 p-4">
        <div class="bg-white p-8 rounded-xl w-full max-w-lg shadow-xl">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-primary">{{ isEditing ? 'Edit Admin' : 'Add Admin' }}</h2>
            <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="saveAdmin" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-1">Username *</label>
              <input 
                v-model="form.username" 
                type="text" 
                required
                class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary" 
                :disabled="isEditing"
              />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Email *</label>
              <input 
                v-model="form.email" 
                type="email" 
                required
                class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary" 
              />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Role *</label>
              <select 
                v-model="form.role" 
                class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary"
              >
                <option value="super">Super Admin</option>
                <option value="admin">Admin</option>
                <option value="staff">Staff</option>
              </select>
            </div>
            <div v-if="!isEditing">
              <label class="block text-sm font-medium mb-1">Password *</label>
              <input 
                v-model="form.password" 
                type="password" 
                required
                class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary" 
              />
            </div>
            <div v-else>
              <label class="block text-sm font-medium mb-1">Password (leave blank to keep current)</label>
              <input 
                v-model="form.password" 
                type="password" 
                class="w-full border rounded px-4 py-2 focus:ring-2 focus:ring-primary" 
              />
            </div>
            <div v-if="formError" class="text-red-600 text-sm mt-2">{{ formError }}</div>
            <div class="flex justify-end gap-2 pt-4">
              <button 
                type="button" 
                @click="closeModal" 
                class="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300 transition"
              >
                Cancel
              </button>
              <button 
                type="submit" 
                :disabled="saving"
                class="bg-primary text-white px-4 py-2 rounded hover:bg-primary/90 transition flex items-center gap-2"
              >
                <svg v-if="saving" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                {{ saving ? 'Processing...' : (isEditing ? 'Update' : 'Create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Delete Confirmation Modal -->
    <transition name="modal-fade">
      <div v-if="deleteModalOpen" class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50 p-4">
        <div class="bg-white p-6 rounded-xl w-full max-w-md shadow-xl">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 class="text-xl font-serif font-bold text-primary mt-4">Confirm Deletion</h3>
            <div class="mt-2">
              <p class="text-sm text-gray-500">
                Are you sure you want to delete admin <span class="font-semibold">{{ adminToDelete?.username }}</span>?
                This action cannot be undone.
              </p>
            </div>
            <div class="mt-6 flex justify-center gap-3">
              <button 
                @click="deleteModalOpen = false" 
                class="px-4 py-2 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button 
                @click="deleteAdmin" 
                class="px-4 py-2 bg-red-600 text-white rounded-md text-sm hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const admins = ref([])
const loading = ref(true)
const error = ref(null)
const saving = ref(false)
const formError = ref('')
const searchQuery = ref('')
const isModalOpen = ref(false)
const isEditing = ref(false)
const deleteModalOpen = ref(false)
const adminToDelete = ref(null)
const currentPage = ref(1)
const perPage = ref(5)

const form = ref({
  id: null,
  username: '',
  email: '',
  role: 'staff',
  password: ''
})

// Fetch admins from backend
async function fetchAdmins() {
  try {
    loading.value = true
    error.value = null
    
    const response = await fetch('http://localhost:5000/admin', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch admins: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    admins.value = data
  } catch (err) {
    console.error('Error fetching admins:', err)
    error.value = err.message || 'Failed to load administrators'
  } finally {
    loading.value = false
  }
}

// Filter admins based on search query and pagination
const filteredAdmins = computed(() => {
  let results = admins.value
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    results = results.filter(admin => 
      admin.username.toLowerCase().includes(query) || 
      admin.email.toLowerCase().includes(query) ||
      admin.role.toLowerCase().includes(query)
    )
  }
  
  // Apply pagination
  const start = (currentPage.value - 1) * perPage.value
  return results.slice(start, start + perPage.value)
})

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function openAddModal() {
  resetForm()
  isEditing.value = false
  isModalOpen.value = true
}

function editAdmin(admin) {
  form.value = {
    id: admin.id,
    username: admin.username,
    email: admin.email,
    role: admin.role,
    password: ''
  }
  isEditing.value = true
  isModalOpen.value = true
}

function confirmDelete(admin) {
  adminToDelete.value = admin
  deleteModalOpen.value = true
}

async function saveAdmin() {
  formError.value = ''
  saving.value = true
  
  try {
    let url, method
    const payload = {
      username: form.value.username,
      email: form.value.email,
      role: form.value.role
    }
    
    // Include password if provided
    if (form.value.password) {
      payload.password = form.value.password
    }
    
    if (isEditing.value) {
      url = `http://localhost:5000/admin/${form.value.id}`
      method = 'PUT'
    } else {
      url = 'http://localhost:5000/admin'
      method = 'POST'
      // For new admin, password is required
      if (!form.value.password) {
        throw new Error('Password is required for new admin')
      }
    }
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(payload)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.msg || `Failed to ${isEditing.value ? 'update' : 'create'} admin`)
    }
    
    const result = await response.json()
    
    if (isEditing.value) {
      // Update existing admin in list
      const index = admins.value.findIndex(a => a.id === form.value.id)
      if (index !== -1) {
        admins.value[index] = { ...admins.value[index], ...payload }
      }
    } else {
      // Add new admin to list
      admins.value.push(result)
    }
    
    closeModal()
  } catch (err) {
    console.error('Error saving admin:', err)
    formError.value = err.message || 'An error occurred. Please try again.'
  } finally {
    saving.value = false
  }
}

async function deleteAdmin() {
  if (!adminToDelete.value) return
  
  try {
    const response = await fetch(`http://localhost:5000/admin/${adminToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (!response.ok) {
      throw new Error(`Failed to delete admin: ${response.status} ${response.statusText}`)
    }
    
    // Remove from local list
    admins.value = admins.value.filter(a => a.id !== adminToDelete.value.id)
    deleteModalOpen.value = false
    adminToDelete.value = null
  } catch (err) {
    console.error('Error deleting admin:', err)
    error.value = err.message || 'Failed to delete admin'
  }
}

function resetForm() {
  form.value = {
    id: null,
    username: '',
    email: '',
    role: 'staff',
    password: ''
  }
}

function closeModal() {
  isModalOpen.value = false
  resetForm()
  formError.value = ''
}

// Fetch data on component mount
onMounted(fetchAdmins)
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

table {
  border-collapse: separate;
  border-spacing: 0;
}

th {
  position: sticky;
  top: 0;
  z-index: 10;
}

tr {
  transition: background-color 0.2s ease;
}

.bg-accent {
  background-color: #f0f4f8;
}

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
</style>