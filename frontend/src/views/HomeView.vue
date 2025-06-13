<script setup lang="ts">
import AIRemoval from "@/components/AIRemoval.vue";
import ColorRemoval from "@/components/ColorRemoval.vue";
import { ref } from "vue";

const activeTab = ref<"ai" | "color">("ai");

const switchTab = (tab: "ai" | "color") => {
  activeTab.value = tab;
};
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">
        Background Removal Tool
      </h1>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto">
        Remove backgrounds from your images using AI or by selecting specific
        colors
      </p>
    </div>

    <!-- Tab Navigation -->
    <div class="flex justify-center mb-8">
      <div class="bg-white rounded-lg p-1 shadow-lg border">
        <button
          @click="switchTab('ai')"
          :class="[
            'px-6 py-3 rounded-md font-medium transition-all duration-200',
            activeTab === 'ai'
              ? 'bg-blue-500 text-white shadow-md'
              : 'text-gray-600 hover:text-blue-500',
          ]"
        >
          AI Background Removal
        </button>
        <button
          @click="switchTab('color')"
          :class="[
            'px-6 py-3 rounded-md font-medium transition-all duration-200',
            activeTab === 'color'
              ? 'bg-blue-500 text-white shadow-md'
              : 'text-gray-600 hover:text-blue-500',
          ]"
        >
          Color Background Removal
        </button>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="max-w-4xl mx-auto">
      <AIRemoval v-if="activeTab === 'ai'" />
      <ColorRemoval v-if="activeTab === 'color'" />
    </div>
  </div>
</template>
