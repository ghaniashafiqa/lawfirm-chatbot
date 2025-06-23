<template>
  <div class="bg-white rounded-lg p-6 text-center text-gray-600 shadow">
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: 'No data available.' }
})
</script>

<style scoped>
/* optional styling */
</style>
