<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import ImageUpload from "./ImageUpload.vue";

const selectedFile = ref<File | null>(null);
const isProcessing = ref(false);
const isAnalyzing = ref(false);
const resultImage = ref<string>("");
const error = ref<string>("");
const dominantColors = ref<string[]>([]);
const previewUrl = ref<string>("");

const options = reactive({
  selectedColor: "#ffffff",
  tolerance: 30,
  format: "PNG" as "PNG" | "JPEG" | "WEBP",
});

// Watch for file changes to auto-analyze colors
watch(selectedFile, async (newFile) => {
  if (newFile) {
    // Create preview URL
    previewUrl.value = window.URL.createObjectURL(newFile);
    await analyzeDominantColors();
  } else {
    dominantColors.value = [];
    if (previewUrl.value) {
      window.URL.revokeObjectURL(previewUrl.value);
      previewUrl.value = "";
    }
  }
});

const analyzeDominantColors = async () => {
  if (!selectedFile.value) return;

  isAnalyzing.value = true;
  error.value = "";

  try {
    const formData = new FormData();
    formData.append("image", selectedFile.value);

    const response = await fetch(
      `${
        import.meta.env.VITE_API_URL || "http://localhost:5000"
      }/get-dominant-colors`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    if (data.success) {
      dominantColors.value = data.dominant_colors;
      // Auto-select first dominant color
      if (data.dominant_colors.length > 0) {
        options.selectedColor = data.dominant_colors[0];
      }
    } else {
      error.value = data.error || "Color analysis failed";
    }
  } catch (err) {
    error.value =
      "Network error. Please check if the backend server is running.";
    console.error("Error:", err);
  } finally {
    isAnalyzing.value = false;
  }
};

const processImage = async () => {
  if (!selectedFile.value) {
    error.value = "Please select an image first";
    return;
  }

  isProcessing.value = true;
  error.value = "";
  resultImage.value = "";

  try {
    const formData = new FormData();
    formData.append("image", selectedFile.value);
    formData.append("color", options.selectedColor);
    formData.append("tolerance", options.tolerance.toString());
    formData.append("format", options.format);

    // Debug logging
    console.log("Sending FormData:", {
      color: options.selectedColor,
      tolerance: options.tolerance,
      format: options.format,
      imageSize: selectedFile.value?.size
    });

    const response = await fetch(
      `${
        import.meta.env.VITE_API_URL || "http://localhost:5000"
      }/remove-color-background`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    if (data.success) {
      resultImage.value = data.result;
    } else {
      error.value = data.error || "Processing failed";
    }
  } catch (err) {
    error.value =
      "Network error. Please check if the backend server is running.";
    console.error("Error:", err);
  } finally {
    isProcessing.value = false;
  }
};

const downloadResult = () => {
  if (!resultImage.value) return;

  const link = document.createElement("a");
  link.href = resultImage.value;
  link.download = `removed-color-bg.${options.format.toLowerCase()}`;
  link.click();
};

const reset = () => {
  selectedFile.value = null;
  resultImage.value = "";
  error.value = "";
  dominantColors.value = [];
  options.selectedColor = "#ffffff";
  options.tolerance = 30;
  if (previewUrl.value) {
    window.URL.revokeObjectURL(previewUrl.value);
    previewUrl.value = "";
  }
};
</script>

<template>
  <div class="bg-white rounded-xl shadow-lg p-6">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">
        Color Background Removal
      </h2>
      <p class="text-gray-600">
        Remove specific colored backgrounds by selecting the target color and
        adjusting tolerance
      </p>
    </div>

    <!-- Image Upload -->
    <div class="mb-6">
      <ImageUpload
        v-model="selectedFile"
        :disabled="isProcessing || isAnalyzing"
        @fileSelected="error = ''"
      />
    </div>

    <!-- Color Analysis Loading -->
    <div
      v-if="isAnalyzing"
      class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg"
    >
      <div class="flex items-center">
        <svg
          class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        <p class="text-blue-700">Analyzing dominant colors...</p>
      </div>
    </div>

    <!-- Dominant Colors -->
    <div v-if="dominantColors.length > 0" class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-3">
        Dominant Colors (Click to select)
      </label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="color in dominantColors"
          :key="color"
          @click="options.selectedColor = color"
          :class="[
            'w-12 h-12 rounded-lg border-2 transition-all hover:scale-110',
            options.selectedColor === color
              ? 'border-blue-500 ring-2 ring-blue-200'
              : 'border-gray-300 hover:border-gray-400',
          ]"
          :style="{ backgroundColor: color }"
          :title="color"
        />
      </div>
    </div>

    <!-- Color Selection -->
    <div class="grid md:grid-cols-2 gap-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Target Color
        </label>
        <div class="flex gap-2">
          <input
            type="color"
            v-model="options.selectedColor"
            :disabled="isProcessing"
            class="w-12 h-10 border border-gray-300 rounded cursor-pointer disabled:opacity-50"
          />
          <input
            type="text"
            v-model="options.selectedColor"
            :disabled="isProcessing"
            placeholder="#ffffff"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Tolerance ({{ options.tolerance }})
        </label>
        <input
          type="range"
          v-model.number="options.tolerance"
          :disabled="isProcessing"
          min="1"
          max="100"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
        />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Precise</span>
          <span>Loose</span>
        </div>
      </div>
    </div>

    <!-- Output Format -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Output Format
      </label>
      <select
        v-model="options.format"
        :disabled="isProcessing"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
      >
        <option value="PNG">PNG (Recommended for transparency)</option>
        <option value="JPEG">JPEG (White background)</option>
        <option value="WEBP">WEBP (Modern format)</option>
      </select>
    </div>

    <!-- Error Message -->
    <div
      v-if="error"
      class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg"
    >
      <p class="text-red-600">{{ error }}</p>
    </div>

    <!-- Process Button -->
    <div class="mb-6">
      <button
        @click="processImage"
        :disabled="!selectedFile || isProcessing || isAnalyzing"
        class="w-full bg-blue-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
      >
        <svg
          v-if="isProcessing"
          class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        {{ isProcessing ? "Processing..." : "Remove Color Background" }}
      </button>
    </div>

    <!-- Result -->
    <div v-if="resultImage" class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-800">Result</h3>

      <div class="grid md:grid-cols-2 gap-4">
        <!-- Original -->
        <div>
          <h4 class="text-sm font-medium text-gray-600 mb-2">Original</h4>
          <div class="border rounded-lg overflow-hidden bg-gray-50">
            <img
              v-if="previewUrl"
              :src="previewUrl"
              alt="Original"
              class="w-full h-48 object-contain"
            />
          </div>
        </div>

        <!-- Result -->
        <div>
          <h4 class="text-sm font-medium text-gray-600 mb-2">
            Background Removed ({{ options.selectedColor }})
          </h4>
          <div class="border rounded-lg overflow-hidden bg-gray-50 relative">
            <!-- Checkerboard pattern for transparency -->
            <div
              class="absolute inset-0"
              style="
                background-image: linear-gradient(
                    45deg,
                    #ccc 25%,
                    transparent 25%
                  ),
                  linear-gradient(-45deg, #ccc 25%, transparent 25%),
                  linear-gradient(45deg, transparent 75%, #ccc 75%),
                  linear-gradient(-45deg, transparent 75%, #ccc 75%);
                background-size: 20px 20px;
                background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
              "
            ></div>
            <img
              :src="resultImage"
              alt="Result"
              class="w-full h-48 object-contain relative z-10"
            />
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button
          @click="downloadResult"
          class="flex-1 bg-green-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-600 transition-colors"
        >
          Download Result
        </button>
        <button
          @click="reset"
          class="flex-1 bg-gray-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-gray-600 transition-colors"
        >
          Start Over
        </button>
      </div>
    </div>
  </div>
</template>
