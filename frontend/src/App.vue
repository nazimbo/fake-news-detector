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
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-3xl font-light text-gray-900 mb-2">
          Fake News Detector
        </h1>
        <p class="text-gray-600">Machine learning-powered text analysis</p>
      </div>

      <!-- Main Card -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
        <div class="space-y-8">
          <!-- Model Selection -->
          <div>
            <label for="model" class="block text-sm font-medium text-gray-700 mb-3">
              Analysis Model
            </label>
            <select
              id="model"
              v-model="typemodel"
              class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            >
              <option value="naive_bayes">Naive Bayes</option>
              <option value="logistic_regression">Logistic Regression</option>
              <option value="random_forest">Random Forest</option>
            </select>
          </div>

          <!-- Model Info Toggle -->
          <div class="flex justify-center">
            <button
              @click="showExplanation = !showExplanation"
              class="text-sm text-blue-600 hover:text-blue-800 transition-colors underline"
            >
              {{ showExplanation ? 'Hide' : 'Learn about' }} this model
            </button>
          </div>

          <!-- Model Explanation -->
          <div v-if="showExplanation" class="bg-gray-50 rounded-lg p-6 border-l-4 border-blue-500">
            <h3 class="font-medium text-gray-900 mb-3">
              {{ modelExplanations[typemodel].title }}
            </h3>
            <p class="text-gray-700 mb-4 leading-relaxed">
              {{ modelExplanations[typemodel].description }}
            </p>
            <div class="text-sm text-gray-600">
              <strong>Key advantage:</strong> {{ modelExplanations[typemodel].strength }}
            </div>
          </div>

          <!-- News Input -->
          <div>
            <label for="newsText" class="block text-sm font-medium text-gray-700 mb-3">
              News Article Text
            </label>
            <textarea
              id="newsText"
              v-model="news"
              placeholder="Paste the news article text here for analysis..."
              class="w-full px-4 py-3 border border-gray-300 rounded-md h-40 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            ></textarea>
          </div>

          <!-- Analyze Button -->
          <div class="flex justify-center">
            <button
              @click="checkNews"
              class="px-8 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
              <span v-else>Analyze Article</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
        <div class="flex items-center">
          <div class="text-red-400 mr-3">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <p class="text-red-800">{{ errorMessage }}</p>
        </div>
      </div>

      <!-- Results -->
      <div v-if="resultValeur" class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div class="text-center">
          <div class="mb-6">
            <div v-if="resultClass === 'fakeNews'" class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
              <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 19c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div v-else class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          
          <h2 class="text-2xl font-light text-gray-900 mb-4">Analysis Complete</h2>
          
          <div class="space-y-4">
            <div class="text-lg text-gray-700">
              <span class="font-medium">Classification:</span>
              <span class="ml-2 font-semibold" :class="resultClass">
                {{ resultValeur }}
              </span>
            </div>
            
            <div class="text-lg text-gray-700">
              <span class="font-medium">Confidence:</span>
              <span class="ml-2 font-semibold" :class="resultClass">
                {{ (probability * 100).toFixed(1) }}%
              </span>
            </div>
            
            <div class="text-sm text-gray-500">
              Model: {{ modelExplanations[typemodel].title }}
            </div>
            
            <!-- Confidence Bar -->
            <div class="mt-6">
              <div class="bg-gray-200 rounded-full h-2 overflow-hidden">
                <div 
                  class="h-full transition-all duration-1000 rounded-full"
                  :class="resultClass === 'fakeNews' ? 'bg-red-500' : 'bg-green-500'"
                  :style="{ width: (probability * 100) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <div class="mt-8 text-center">
        <p class="text-sm text-gray-500 leading-relaxed">
          This tool provides automated analysis and should not be the sole basis for determining news authenticity. 
          Always cross-reference with multiple reliable sources.
        </p>
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

/* Smooth transitions */
* {
  transition: all 0.2s ease;
}

/* Focus states */
select:focus,
textarea:focus,
button:focus {
  outline: none;
}

/* Custom scrollbar for textarea */
textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>
