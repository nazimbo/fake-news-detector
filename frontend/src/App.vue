<script setup>
import { ref } from 'vue';
import axios from 'axios';

const news = ref('');

function checkNews() {
  // Transformation de la valeur de news en JSON avec la clé article
  const newsJson = { article: news.value };
  
  console.log(newsJson); // Afficher le JSON dans la console
  
  axios.post('http://127.0.0.1:5000/predict', newsJson)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}
</script>

<template>
  <div>
    <h1>Fake news detector</h1>
    <div>
      <label for="newsText">Enter the news text to check:</label><br />
      <span>
        <textarea id="newsText" v-model="news" placeholder="Type the news text here..." class="news-textarea"></textarea>
      </span>
      <br />
      <span>
        <button @click="checkNews">Check news</button>
      </span>
    </div>
  </div>
</template>

<style scoped>
.news-textarea {
  width: 400px;
  height: 200px;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
