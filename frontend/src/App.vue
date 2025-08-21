<script setup>
import { ref } from "vue";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

const news = ref("");
const resultValeur = ref("");
const resultClass = ref("");
const typemodel = ref("naive_bayes");
const modelName = ref("");
const probability = ref(0);
const isLoading = ref(false);
const errorMessage = ref("");
const showExplanation = ref(false);

const modelExplanations = {
  naive_bayes: {
    title: "Naive Bayes",
    description: "A probabilistic classifier that calculates the likelihood of fake vs real news based on word patterns and statistical independence.",
    strength: "Fast and effective with limited data"
  },
  logistic_regression: {
    title: "Logistic Regression",
    description: "A linear statistical model that creates a decision boundary to classify news articles using feature relationships.",
    strength: "Interpretable and reliable results"
  },
  random_forest: {
    title: "Random Forest",
    description: "An ensemble method combining multiple decision trees, where each tree votes on the final classification.",
    strength: "High accuracy with complex patterns"
  }
};

async function checkNews() {
  if (!news.value.trim()) {
    errorMessage.value = "Please enter the news text.";
    return;
  }

  const newsJson = { article: news.value, model: typemodel.value };

  console.log(newsJson); // Afficher le JSON dans la console

  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await axios.post(`${API_URL}/predict`, newsJson);
    resultValeur.value = response.data.prediction;
    modelName.value = response.data.model;
    const probabilities = response.data.probabilities;
    if (resultValeur.value === "Fake news") {
      resultClass.value = "fakeNews";
      probability.value = probabilities.fake;
    } else {
      resultClass.value = "trueNews";
      probability.value = probabilities.true;
    }
    console.log(resultValeur.value);
    console.log(response.data.model);
    console.log(probability.value);
  } catch (error) {
    console.error(error);
    if (error.response) {
      errorMessage.value = `Server error: ${error.response.data.error || "Unknown error"}`;
    } else if (error.request) {
      errorMessage.value =
        "Cannot connect to server. Please check if the API is running.";
    } else {
      errorMessage.value = "An error occurred while making the request.";
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 sm:py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8 sm:mb-12">
        <div class="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-blue-100 rounded-full mb-4 sm:mb-6">
          <svg class="w-8 h-8 sm:w-10 sm:h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 class="text-2xl sm:text-3xl lg:text-4xl font-semibold text-gray-900 mb-2 sm:mb-3">
          Fake News Detector
        </h1>
        <p class="text-sm sm:text-base text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Advanced machine learning models to analyze and verify news article authenticity
        </p>
      </div>

      <!-- Main Card -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8 mb-6 sm:mb-8 backdrop-blur-sm">
        <div class="space-y-6 sm:space-y-8">
          <!-- Model Selection -->
          <div>
            <label for="model" class="block text-sm font-semibold text-gray-800 mb-4">
              Choose Analysis Model
            </label>
            <div class="relative">
              <select
                id="model"
                v-model="typemodel"
                class="w-full px-4 py-4 text-base border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 appearance-none bg-white cursor-pointer hover:border-gray-300"
              >
                <option value="naive_bayes">Naive Bayes</option>
                <option value="logistic_regression">Logistic Regression</option>
                <option value="random_forest">Random Forest</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center px-4 pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Model Info Toggle -->
          <div class="flex justify-center">
            <button
              @click="showExplanation = !showExplanation"
              class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-all duration-200"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'rotate-180': showExplanation }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              {{ showExplanation ? 'Hide model details' : 'Learn about this model' }}
            </button>
          </div>

          <!-- Model Explanation -->
          <div v-if="showExplanation" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200 transform transition-all duration-300">
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-lg font-semibold text-gray-900 mb-3">
                  {{ modelExplanations[typemodel].title }}
                </h3>
                <p class="text-gray-700 mb-4 leading-relaxed">
                  {{ modelExplanations[typemodel].description }}
                </p>
                <div class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  {{ modelExplanations[typemodel].strength }}
                </div>
              </div>
            </div>
          </div>

          <!-- News Input -->
          <div>
            <label for="newsText" class="block text-sm font-semibold text-gray-800 mb-4">
              News Article Text
            </label>
            <div class="relative">
              <textarea
                id="newsText"
                v-model="news"
                placeholder="Paste the news article text here for analysis..."
                class="w-full px-4 py-4 border-2 border-gray-200 rounded-xl h-32 sm:h-40 resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 placeholder-gray-400 text-base leading-relaxed hover:border-gray-300"
              ></textarea>
              <div class="absolute bottom-3 right-3 text-xs text-gray-400">
                {{ news.length }} characters
              </div>
            </div>
          </div>

          <!-- Analyze Button -->
          <div class="flex justify-center pt-2">
            <button
              @click="checkNews"
              class="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:ring-blue-200 transition-all duration-200 font-semibold text-base disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl min-w-[200px]"
              :disabled="isLoading || !news.trim()"
            >
              <span v-if="isLoading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
              <span v-else class="flex items-center justify-center">
                <svg class="w-5 h-5 mr-2 group-hover:rotate-12 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Analyze Article
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 rounded-r-xl p-4 sm:p-6 mb-6 sm:mb-8 transform transition-all duration-300">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          <div class="ml-3 flex-1">
            <h3 class="text-sm font-semibold text-red-800 mb-1">Analysis Error</h3>
            <p class="text-sm text-red-700 leading-relaxed">{{ errorMessage }}</p>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-if="resultValeur" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8 transform transition-all duration-500 animate-fade-in">
        <div class="text-center">
          <div class="mb-6 sm:mb-8">
            <div v-if="resultClass === 'fakeNews'" class="inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 bg-red-100 rounded-full mb-4 sm:mb-6 animate-pulse-once">
              <svg class="w-10 h-10 sm:w-12 sm:h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 19c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div v-else class="inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 bg-green-100 rounded-full mb-4 sm:mb-6 animate-pulse-once">
              <svg class="w-10 h-10 sm:w-12 sm:h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          
          <h2 class="text-xl sm:text-2xl font-semibold text-gray-900 mb-6 sm:mb-8">Analysis Complete</h2>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
            <div class="bg-gray-50 rounded-xl p-4 sm:p-6">
              <div class="text-sm font-medium text-gray-600 mb-2">Classification</div>
              <div class="text-xl sm:text-2xl font-bold" :class="resultClass">
                {{ resultValeur }}
              </div>
            </div>
            
            <div class="bg-gray-50 rounded-xl p-4 sm:p-6">
              <div class="text-sm font-medium text-gray-600 mb-2">Confidence Level</div>
              <div class="text-xl sm:text-2xl font-bold" :class="resultClass">
                {{ (probability * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
          
          <!-- Confidence Bar -->
          <div class="mb-6">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Low Confidence</span>
              <span>High Confidence</span>
            </div>
            <div class="bg-gray-200 rounded-full h-3 overflow-hidden shadow-inner">
              <div 
                class="h-full transition-all duration-1000 rounded-full relative"
                :class="resultClass === 'fakeNews' ? 'bg-gradient-to-r from-red-400 to-red-600' : 'bg-gradient-to-r from-green-400 to-green-600'"
                :style="{ width: (probability * 100) + '%' }"
              >
                <div class="absolute inset-0 bg-white opacity-20 rounded-full animate-shimmer"></div>
              </div>
            </div>
          </div>
          
          <div class="text-sm text-gray-500 bg-gray-50 rounded-lg py-2 px-4 inline-block">
            <span class="font-medium">Model used:</span> {{ modelExplanations[typemodel].title }}
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <div class="mt-6 sm:mt-8">
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 sm:p-6">
          <div class="flex items-start space-x-3">
            <div class="flex-shrink-0">
              <svg class="w-5 h-5 text-amber-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-sm text-amber-800 leading-relaxed">
              <strong class="font-semibold">Important:</strong> This tool provides automated analysis and should not be the sole basis for determining news authenticity. Always cross-reference with multiple reliable sources and use critical thinking.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fakeNews {
  color: #dc2626;
}

.trueNews {
  color: #059669;
}

/* Custom animations */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse-once {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}

.animate-pulse-once {
  animation: pulse-once 0.6s ease-in-out;
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

/* Smooth transitions */
* {
  transition: all 0.2s ease;
}

/* Enhanced focus states */
select:focus,
textarea:focus,
button:focus {
  outline: none;
}

/* Hover effects */
.group:hover .group-hover\:rotate-12 {
  transform: rotate(12deg);
}

/* Custom scrollbar for textarea */
textarea::-webkit-scrollbar {
  width: 8px;
}

textarea::-webkit-scrollbar-track {
  background: #f8fafc;
  border-radius: 4px;
}

textarea::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #cbd5e1, #94a3b8);
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #94a3b8, #64748b);
}

/* Mobile touch improvements */
@media (max-width: 640px) {
  button {
    min-height: 48px;
  }
  
  select {
    min-height: 48px;
  }
  
  textarea {
    min-height: 120px;
  }
}

/* Subtle glass effect */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
