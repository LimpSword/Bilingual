<template>
  <div id="app">
    <div class="container">
      <div class="panel lookup-translation">
        <h2>Look up Translation</h2>
        <div class="input-group">
          <input v-model="wordToTranslate" type="text" placeholder="Enter a word"/>
          <select v-model="originLanguage">
            <option v-for="language in languages" :key="language">{{ language }}</option>
          </select>
          <select v-model="selectedLanguage">
            <option v-for="language in languages" :key="language">{{ language }}</option>
          </select>
          <button @click="getTranslation">Translate</button>
        </div>
        <!-- Display translations here -->
        <div class="translation-results" v-if="translations.length > 0">
          <h3>Translations:</h3>
          <div class="translation-item" v-for="(translation, index) in translations" :key="index">
            <div class="translation-row">
              <div class="frword">{{ translation.frword }}</div>
              <div class="translation-details">
                <div v-for="(translationDetail, detailIndex) in translation.toword" :key="detailIndex" class="translation-detail">
                  {{ translationDetail }}
                </div>
                <div v-if="translation.frex || translation.toex" class="translation-example">
                  <b>Example:</b> {{ translation.frex }} <br> {{ translation.toex }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- End of translation display -->
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
      axios.post( 'http://127.0.0.1:5000/moreTrad',  {'word' : this.wordToTranslate, 'origin_language' : originLanguage ,'destination_language' : destinationLanguage})
          .then(response => {
            // Update component data with the response from the server
            console.log(response.data)
            this.translations = response.data;
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
  font-family: 'Arial', sans-serif;
  color: #333;
  margin-top: 30px;
}

.container {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.panel {
  background-color: #f2f2f2;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 50%;
  min-height: 600px;
  padding: 2rem;
}

.panel h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.lookup-translation {
  max-height: 80vh; /* Limit the maximum height of the translation section */
  overflow: hidden; /* Hide any content that overflows */
}

.translation-results {
  overflow-y: auto; /* Enable vertical scrolling when content overflows */
  max-height: calc(80vh - 200px); /* Adjusted maximum height to prevent overflow */
}

.input-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

input, select, button {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #6366f1;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #4245eb;
}

.translation-results {
  margin-top: 1rem;
}

.translation-item {
  margin-bottom: 2rem; /* Increased margin between translation items */
  border-radius: 8px; /* Add border radius for rounded corners */
  background-color: #fff; /* White background */
  padding: 1rem; /* Padding for inner content */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a subtle box shadow */
}

.translation-index {
  font-weight: bold;
}

.translation-content {
  margin-left: 1rem;
}

.frword {
  font-weight: bold;
}

.translation-detail {
  margin-left: 1rem;
}

.translation-example {
  margin-left: 1rem;
  font-style: italic;
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

.select-category {
  overflow-y: auto; /* Enable vertical scrolling for the category panel */
  max-height: 80vh; /* Limit the maximum height of the category panel */
}

.create-category-button {
  background-color: #ccc;
  color: #333;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.create-category-button:hover {
  background-color: #888;
}


.translation-row {
  display: flex;
  align-items: flex-start;
}

.frword {
  font-weight: bold;
  min-width: 120px; /* Adjust the width as needed */
}

.translation-details {
  flex-grow: 1;
}

.translation-detail {
  margin-bottom: 0.5rem; /* Reduced margin between translation details */
}

.translation-example {
  font-style: italic;
  margin-top: 0.5rem; /* Add margin above examples */
}

</style>
