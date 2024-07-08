<script setup>
import { ref } from "vue";
import axios from "axios";

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
    const response = await axios.post("http://127.0.0.1:5000/predict", newsJson);
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
    errorMessage.value = "An error occurred while fetching the prediction. Please try again.";
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-6">
    <div class="max-w-lg w-full bg-white bg-opacity-80 backdrop-blur-lg rounded-lg shadow-lg p-6">
      <h1 class="text-3xl font-bold text-center mb-6">Fake News Detector</h1>
      <div class="mb-4">
        <label for="model" class="block text-gray-700 font-semibold mb-2">Choose the model:</label>
        <select id="model" v-model="typemodel" class="block w-full bg-gray-50 border border-gray-300 rounded-md py-2 px-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="naive_bayes">Naive Bayes</option>
          <option value="logistic_regression">Logistic Regression</option>
          <option value="random_forest">Random Forest</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="newsText" class="block text-gray-700 font-semibold mb-2">Enter the news text to check:</label>
        <textarea id="newsText" v-model="news" placeholder="Type the news text here..." class="block w-full bg-gray-50 border border-gray-300 rounded-md py-2 px-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 h-40"></textarea>
      </div>
      <div class="flex justify-center">
        <button @click="checkNews" class="bg-indigo-500 text-white font-semibold py-2 px-4 rounded-md shadow-md hover:bg-indigo-600 transition duration-200" :disabled="isLoading">
          <span v-if="isLoading">Checking...</span>
          <span v-else>Check News</span>
        </button>
      </div>
      <div v-if="errorMessage" class="mt-4 text-center text-red-600">
        {{ errorMessage }}
      </div>
      <div v-if="resultValeur" class="mt-6 text-center">
        <p class="text-xl font-semibold">
          Le modèle {{ modelName }} a estimé que c'était une <span :class="resultClass">{{ resultValeur }}</span> avec une probabilité de <span :class="resultClass">{{ (probability * 100).toFixed(2) }}%</span>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fakeNews {
  color: red;
}
.trueNews {
  color: green;
}
</style>
