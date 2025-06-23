// src/components/ChartCard.vue
<template>
  <div :class="['p-4 rounded-lg shadow', bgColor]">
    <p class="text-sm text-gray-500">{{ title }}</p>
    <p class="text-2xl font-bold">{{ value }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], default: () => '' },
  color: { type: String, default: 'blue' }
})

const bgColor = computed(() => {
  const map = {
    blue: 'bg-white',
    red: 'bg-red-50',
    green: 'bg-green-50'
  }
  return map[props.color] || 'bg-white'
})
</script>

<style scoped>
/* optional custom styling */
</style>