<template>
  <div :class="['rounded-2xl p-5 shadow-md border border-gray-100', bg]">
    <div class="flex items-center justify-between mb-2">
      <p class="text-xs text-gray-600 uppercase tracking-wide">{{ title }}</p>
      <span class="text-xl">{{ icon }}</span>
    </div>
    <h2 class="text-3xl font-extrabold text-gray-800">{{ value }}</h2>
    <p class="text-sm text-gray-500">{{ subtitle }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
  icon: String,
  bg: String,
})
</script>
