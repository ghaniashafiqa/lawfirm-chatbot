<template>
  <div class="p-8 min-h-screen bg-neutralbg">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-primary">Account Settings</h1>
      <p class="text-gray-600 text-sm mt-2">Manage your profile information and security settings</p>
    </div>

    <!-- Main Content -->
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Navigation -->
      <div class="lg:w-1/4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sticky top-8">
          <h3 class="font-medium text-gray-800 mb-3">Settings</h3>
          <ul class="space-y-1">
            <li v-for="tab in tabs" :key="tab.id"
                @click="activeTab = tab.id"
                class="px-3 py-2 rounded-md cursor-pointer transition"
                :class="activeTab === tab.id
                  ? 'bg-primary/10 text-primary font-medium'
                  : 'hover:bg-gray-100 text-gray-600'">
              <div class="flex items-center gap-2">
                <component :is="tab.icon" class="h-4 w-4" />
                {{ tab.label }}
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Content Area -->
      <div class="lg:w-3/4">
        <!-- Profile Settings -->
        <div v-if="activeTab === 'profile'" class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
          <div class="border-b border-gray-100 px-6 py-4">
            <h2 class="text-lg font-semibold text-gray-800">Profile Information</h2>
            <p class="text-sm text-gray-500 mt-1">Update your account's profile information</p>
          </div>

          <div class="p-6">
            <form @submit.prevent="updateProfile" class="space-y-6 max-w-2xl">
              <div class="flex items-center gap-6 mb-6">
                <div class="relative">
                  <div class="bg-gray-200 border-2 border-dashed rounded-xl w-20 h-20 flex items-center justify-center">
                    <span class="text-2xl font-bold text-gray-400">{{ initials }}</span>
                  </div>
                  <button type="button" class="absolute -bottom-2 -right-2 bg-white rounded-full p-1.5 shadow-md border border-gray-200" title="Change profile photo">
                    <PencilIcon class="h-4 w-4 text-gray-600" />
                  </button>
                </div>
                <div>
                  <h3 class="font-medium">Profile Photo</h3>
                  <p class="text-sm text-gray-500 mt-1">JPG or PNG no larger than 5MB</p>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">First Name</label>
                  <input v-model="profileForm.firstName" class="input-field" />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Last Name</label>
                  <input v-model="profileForm.lastName" class="input-field" />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
                <input v-model="profileForm.email" type="email" class="input-field" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Username</label>
                <input v-model="profileForm.username" class="input-field" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Role</label>
                <input v-model="profileForm.role" class="input-field bg-gray-50 text-gray-600 cursor-not-allowed" disabled />
              </div>

              <div class="flex justify-end pt-4">
                <button type="submit" class="submit-btn" :disabled="saving">
                  <ArrowPathIcon v-if="saving" class="h-4 w-4 animate-spin" />
                  {{ saving ? 'Saving...' : 'Update Profile' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Password Settings -->
        <div v-if="activeTab === 'password'" class="settings-section">
          <div class="section-header">
            <h2>Password Settings</h2>
            <p>Update your account password for security</p>
          </div>

          <div class="p-6">
            <form @submit.prevent="updatePassword" class="space-y-6 max-w-2xl">
              <div>
                <label class="label">Current Password</label>
                <input v-model="passwordForm.currentPassword" type="password" class="input-field" required />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="label">New Password</label>
                  <input v-model="passwordForm.newPassword" type="password" class="input-field" required />
                </div>

                <div>
                  <label class="label">Confirm Password</label>
                  <input v-model="passwordForm.confirmPassword" type="password" class="input-field" required />
                </div>
              </div>

              <div v-if="passwordError" class="bg-red-50 rounded-lg p-4 border border-red-100">
                <p class="text-red-700 text-sm">{{ passwordError }}</p>
              </div>

              <div class="flex justify-end pt-4">
                <button type="submit" class="submit-btn" :disabled="saving">
                  <ArrowPathIcon v-if="saving" class="h-4 w-4 animate-spin" />
                  {{ saving ? 'Updating...' : 'Change Password' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Security Settings -->
        <div v-if="activeTab === 'security'" class="settings-section">
          <div class="section-header">
            <h2>Security Settings</h2>
            <p>Manage your account's security settings</p>
          </div>

          <div class="p-6">
            <div class="max-w-2xl space-y-6">
              <div class="flex items-start justify-between border-b border-gray-100 pb-6">
                <div>
                  <h3 class="font-medium text-gray-800">Two-Factor Authentication</h3>
                  <p class="text-sm text-gray-500 mt-1">Add an extra layer of security to your account</p>
                </div>
                <button @click="toggle2FA" class="text-sm bg-gray-100 hover:bg-gray-200 px-4 py-1.5 rounded-lg transition">
                  {{ twoFactorEnabled ? 'Disable' : 'Enable' }}
                </button>
              </div>

              <div>
                <h3 class="font-medium text-gray-800 mb-3">Active Sessions</h3>
                <div class="border border-gray-200 rounded-lg overflow-hidden">
                  <div v-for="session in sessions" :key="session.id" class="border-b border-gray-100 last:border-0">
                    <div class="flex items-center justify-between p-4">
                      <div class="flex items-center gap-3">
                        <div class="bg-gray-100 p-2 rounded-lg">
                          <ComputerDesktopIcon class="h-5 w-5 text-gray-500" />
                        </div>
                        <div>
                          <p class="font-medium">{{ session.device }}</p>
                          <p class="text-sm text-gray-500 flex items-center gap-1 mt-1">
                            <span>{{ session.location }}</span>
                            <span class="text-gray-400">•</span>
                            <span>{{ session.ip }}</span>
                          </p>
                        </div>
                      </div>
                      <div class="text-right">
                        <p class="text-sm text-gray-500">{{ formatDate(session.lastActive) }}</p>
                        <button v-if="!session.current" @click="logOutSession(session.id)" class="text-red-600 text-sm hover:text-red-800 mt-2">
                          Log out
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import api from '@/api/axios'
import {
  UserCircleIcon,
  LockClosedIcon,
  ShieldCheckIcon,
  PencilIcon,
  ComputerDesktopIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const activeTab = ref('profile')
const saving = ref(false)
const passwordError = ref('')
const twoFactorEnabled = ref(false)
const auth = useAuthStore()

const userId = ref(null)

const tabs = ref([
  { id: 'profile', label: 'Profile', icon: UserCircleIcon },
  { id: 'password', label: 'Password', icon: LockClosedIcon },
  { id: 'security', label: 'Security', icon: ShieldCheckIcon },
])

const profileForm = ref({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  role: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const sessions = ref([])

const initials = computed(() => {
  const first = profileForm.value.firstName?.charAt(0) || ''
  const last = profileForm.value.lastName?.charAt(0) || ''
  return `${first}${last}`
})

function formatDate(dateString) {
  return new Date(dateString).toLocaleString('id-ID')
}

async function fetchProfile() {
  try {
    await auth.fetchProfile()
    const user = auth.user
    userId.value = user.id
    profileForm.value = {
      firstName: user.first_name || '',
      lastName: user.last_name || '',
      username: user.username || '',
      email: user.email || '',
      role: user.role || ''
    }

    const sessionRes = await api.get('/auth/sessions')
    sessions.value = sessionRes.data
  } catch (err) {
    console.error('❌ Failed to fetch profile:', err)
  }
}

async function updateProfile() {
  saving.value = true
  try {
    await api.put(`/users/${userId.value}`, {
      first_name: profileForm.value.firstName,
      last_name: profileForm.value.lastName,
      username: profileForm.value.username,
      email: profileForm.value.email
    })
    alert('✅ Profile updated successfully!')
  } catch (error) {
    console.error('❌ Error updating profile:', error)
    alert('Failed to update profile. Please try again.')
  } finally {
    saving.value = false
  }
}

async function updatePassword() {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = 'New password and confirmation do not match'
    return
  }
  if (passwordForm.value.newPassword.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
    return
  }
  saving.value = true
  passwordError.value = ''
  try {
    await api.post('/auth/change-password', {
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword
    })
    alert('✅ Password updated successfully!')
    passwordForm.value = { currentPassword: '', newPassword: '', confirmPassword: '' }
  } catch (error) {
    console.error('❌ Error updating password:', error)
    passwordError.value = error?.response?.data?.message || 'Failed to update password.'
  } finally {
    saving.value = false
  }
}

async function toggle2FA() {
  try {
    if (twoFactorEnabled.value) {
      await api.post('/auth/2fa/disable')
    } else {
      await api.post('/auth/2fa/enable')
    }
    twoFactorEnabled.value = !twoFactorEnabled.value
  } catch (err) {
    console.error('❌ Failed to toggle 2FA:', err)
  }
}

async function logOutSession(sessionId) {
  try {
    await api.post('/auth/logout-session', { session_id: sessionId })
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
  } catch (err) {
    console.error('❌ Failed to log out session:', err)
  }
}

onMounted(() => {
  fetchProfile()
})
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
input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.2);
}
.input-field {
  @apply w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent;
}
.submit-btn {
  @apply bg-primary text-white px-6 py-2.5 rounded-lg hover:bg-primary/90 transition font-medium flex items-center gap-2;
}
.settings-section {
  @apply bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden;
}
.section-header {
  @apply border-b border-gray-100 px-6 py-4;
}
.section-header h2 {
  @apply text-lg font-semibold text-gray-800;
}
.section-header p {
  @apply text-sm text-gray-500 mt-1;
}
.label {
  @apply block text-sm font-medium text-gray-700 mb-1.5;
}
</style>
