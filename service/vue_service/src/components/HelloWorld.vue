<script>
import axios from 'axios';

export default {
  data() {
    return {
      newsInput: '',
      loading: false,
      displayResult: false
    };
  },
  methods: {
    submitNews() {
      this.loading = true;  // Démarre l'indicateur de chargement
      const news = this.newsInput;
      console.log(news);
      axios.post('http://localhost:3000/scrape', { url: news })
          .then(response => {
            console.log('Scraped content:', response.data.body);
            this.displayResult = true;
            setTimeout(() => {
              this.loading = false;  // Arrête l'indicateur de chargement après 5 secondes
            }, 5000);
          })
          .catch(error => {
            console.error('Error scraping:', error);
            this.loading = false;
          });
    }
  }
}
</script>

<template>
  <div>
    <h1>Fake news detector:</h1>
    <form @submit.prevent="submitNews">
      <label for="news">Enter the news here:</label>
      <input type="text" id="news" name="news" v-model="newsInput">
      <button type="submit">Submit</button>
    </form>
    <span id="result">
      <!-- Affiche une icône de chargement ou un message pendant le chargement -->
      <span v-if="loading">
        <img src="https://media1.tenor.com/images/21c0e8dc0259f94a7aae44817bd24b1d/tenor.gif?itemid=5434959" alt="Loading..."> <!-- Assurez-vous de remplacer par le chemin correct de votre icône -->
        <!-- Ou simplement un message texte -->
        <!-- <p>Chargement...</p> -->
      </span>
    </span>
  </div>
</template>
<style>
/* Style de base pour le conteneur principal */
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f4f4f4;
  font-family: 'Arial', sans-serif;
}

/* Titre */
h1 {
  color: #333;
  margin-bottom: 20px;
}

/* Style du formulaire */
form {
  display: flex;
  flex-direction: column;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding: 20px;
  background: white;
  border-radius: 8px;
}

/* Label styling */
label {
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

/* Input text styling */
input[type="text"] {
  padding: 10px;
  margin-bottom: 20px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

/* Bouton de soumission */
button {
  background-color: #0056b3;
  color: white;
  border: none;
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #003580;
}
span{
  margin: 10px;
}
img{
  border-radius: 50%;
}
</style>
