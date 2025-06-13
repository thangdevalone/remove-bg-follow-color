<script setup lang="ts">
import { ref, defineEmits, defineProps } from 'vue'

interface Props {
  modelValue?: File | null
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  disabled: false
})

const emit = defineEmits<{
  'update:modelValue': [file: File | null]
  'fileSelected': [file: File]
}>()

const isDragging = ref(false)
const fileInput = ref<HTMLInputElement>()
const previewUrl = ref<string>('')

const handleFileSelect = (file: File) => {
  if (!file.type.startsWith('image/')) {
    alert('Please select an image file')
    return
  }

  emit('update:modelValue', file)
  emit('fileSelected', file)
  
  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const onFileInputChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    handleFileSelect(file)
  }
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = false
  
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    handleFileSelect(files[0])
  }
}

const onDragOver = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = true
}

const onDragLeave = () => {
  isDragging.value = false
}

const triggerFileInput = () => {
  if (!props.disabled) {
    fileInput.value?.click()
  }
}

const clearImage = () => {
  emit('update:modelValue', null)
  previewUrl.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<template>
  <div class="space-y-4">
    <!-- Upload Area -->
    <div
      v-if="!previewUrl"
      @click="triggerFileInput"
      @drop="onDrop"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      :class="[
        'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
        isDragging
          ? 'border-blue-400 bg-blue-50'
          : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50',
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      ]"
    >
      <div class="space-y-4">
        <div class="flex justify-center">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
          </svg>
        </div>
        <div>
          <p class="text-lg font-medium text-gray-700">
            Drop your image here or click to browse
          </p>
          <p class="text-sm text-gray-500 mt-1">
            PNG, JPG, WEBP up to 10MB
          </p>
        </div>
      </div>
    </div>

    <!-- Preview -->
    <div v-if="previewUrl" class="relative">
      <div class="border rounded-lg overflow-hidden bg-white shadow-lg">
        <img 
          :src="previewUrl" 
          alt="Preview" 
          class="w-full max-h-96 object-contain"
        />
      </div>
      <button
        @click="clearImage"
        class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      @change="onFileInputChange"
      class="hidden"
      :disabled="disabled"
    />
  </div>
</template> 