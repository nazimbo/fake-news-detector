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
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-6">
    <div
      class="max-w-lg w-full bg-white bg-opacity-80 backdrop-blur-lg rounded-lg shadow-lg p-6"
    >
      <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">
        Fake News Detector
      </h1>
      <div class="mb-4">
        <label for="model" class="block text-gray-700 font-semibold mb-2"
          >Choose the model:</label
        >
        <select
          id="model"
          v-model="typemodel"
          class="block w-full bg-gray-50 border border-gray-300 rounded-md py-2 px-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="naive_bayes">Naive Bayes</option>
          <option value="logistic_regression">Logistic Regression</option>
          <option value="random_forest">Random Forest</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="newsText" class="block text-gray-700 font-semibold mb-2"
          >Enter the news text to check:</label
        >
        <textarea
          id="newsText"
          v-model="news"
          placeholder="Type the news text here..."
          class="block w-full bg-gray-50 border border-gray-300 rounded-md py-2 px-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 h-40 resize-none"
        ></textarea>
      </div>
      <div class="flex justify-center">
        <button
          @click="checkNews"
          class="bg-indigo-500 text-white font-semibold py-2 px-4 rounded-md shadow-md hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Checking...</span>
          <span v-else>Check News</span>
        </button>
      </div>
      <div v-if="errorMessage" class="mt-4 text-center text-red-600">
        {{ errorMessage }}
      </div>
      <div v-if="resultValeur" class="mt-6 text-center">
        <p class="text-xl font-semibold text-gray-800">
          The model <span class="font-bold">{{ modelName }}</span> estimated
          this to be <span :class="resultClass">{{ resultValeur }}</span> with a
          probability of
          <span :class="resultClass"
            >{{ (probability * 100).toFixed(2) }}%</span
          >
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fakeNews {
  color: #ef4444; /* red-500 */
  font-weight: 700;
}

.trueNews {
  color: #10b981; /* green-500 */
  font-weight: 700;
}
</style>
