<template>
  <div id="app">
    <div class="container">
      <div class="panel lookup-translation">
        <h2>Look up Translation</h2>
        <input v-model="wordToTranslate" type="text" placeholder="Enter a word"/>
        <select v-model="originLanguage">
          <option v-for="language in languages" :key="language">{{ language }}</option>
        </select>
        <select v-model="selectedLanguage">
          <option v-for="language in languages" :key="language">{{ language }}</option>
        </select>
        <button @click="getTranslation">Translate</button>
        <div class="translation-results" v-if="translations.length > 0">
          <h3>Translations:</h3>
          <div v-for="(translation, index) in translations" :key="index">
            <div>{{ index + 1 }}. {{ translation.frword }}</div>
            <div v-for="(translationDetail, detailIndex) in translation.toword" :key="detailIndex">
              - {{ translationDetail }}
              <div v-if="translation.frex || translation.toex">
                <b>Example:</b> {{ translation.frex }} => {{ translation.toex }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="panel select-category">
        <h2>Select Category</h2>
        <div class="category-list">
          <button v-for="category in categories" :key="category.id" @click="selectCategory(category)">
            {{ category.name }}
          </button>
          <button class="create-category-button" @click="goToCreateCategoryPage">New Category</button>
        </div>
        <div class="selected-category" v-if="selectedCategory">
          <h3>Selected Category: {{ selectedCategory.name }}</h3>

          <div class="word-list">
            <div v-for="word in selectedCategory.words" :key="word.id">
              {{ word.label }}: {{ word.text }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      wordToTranslate: '',
      originLanguage: 'english',
      selectedLanguage: 'english',
      languages: ['english', 'french', 'spanish', 'japanese', 'korean', 'chinese', 'german', 'dutch', 'swedish', 'russian', 'portuguese', 'polish', 'romanian', 'czech', 'greek', 'turkish', 'icelandic', 'arabic', 'italian', 'other'],
      translations: [],
      categories: [
        {id: 1, name: 'Category 1', words: [{id: 1, label: 'Label 1', text: 'Word 1'}]},
        {id: 2, name: 'Category 2', words: [{id: 2, label: 'Label 2', text: 'Word 2'}]},
        {id: 3, name: 'Category 3', words: [{id: 3, label: 'Label 3', text: 'Word 3'}]},
      ],
      selectedCategory: null,
    };

  },
  methods: {
    getTranslation() {
      const originLanguage = 'english'; // Assuming default origin language is English
      const destinationLanguage = this.selectedLanguage.toLowerCase(); // Use the selected destination language

      // Make a GET request to your Flask server with the word, origin language, and destination language as parameters
      axios.get(`/translate?word=${this.wordToTranslate}&origin_language=${originLanguage}&destination_language=${destinationLanguage}`)
          .then(response => {
            // Update component data with the response from the server
            console.log(response.data)
            this.translations = response.data.translations;
          })
          .catch(error => {
            console.error('Error fetching translation:', error);
          });
    },
    selectCategory(category) {
      this.selectedCategory = category;
    },
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 2rem;
}

.panel {
  background-color: #f2f2f2;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 50%;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  text-align: left;
}

.panel h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

input, select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 1rem;
}

button {
  background-color: #6366f1;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

button:hover {
  background-color: #4245eb;
}

.translation-results {
  margin-top: 1rem;
  text-align: left;
}

.example-sentences {
  margin-top: 1rem;
  text-align: left;
}

.category-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.category-list button {
  text-align: left;
}

.selected-category {
  margin-top: 2rem;
}

.create-category-button {
  background-color: #ccc; /* Gray background color */
  color: #333; /* Dark text color */
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease; /* Smooth transition on hover */
}

.create-category-button:hover {
  background-color: #888; /* Darker gray background color on hover */
}

</style>