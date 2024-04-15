<template>
  <div class="new-category">
    <div class="panel">
      <h2>New Category</h2>
      <div class="category-name">
        <label for="categoryName">Category Name:</label>
        <input id="categoryName" v-model="categoryName" type="text" placeholder="Enter category name">
      </div>

      <div class="input-method">
        <input type="radio" id="addWordsManually" value="manual" v-model="inputMethod">
        <label for="addWordsManually">Add Words Manually</label>
        <input type="radio" id="uploadCSV" value="csv" v-model="inputMethod">
        <label for="uploadCSV">Upload CSV</label>
      </div>

      <div v-if="inputMethod === 'manual'" class="manual-input">
        <h3>Add Words Manually</h3>
        <div class="word-input-container">
          <div v-for="(word, index) in words" :key="index" class="word-input">
            <input v-model="word.word" type="text" placeholder="Word">
            <input v-model="word.translation" type="text" placeholder="Translation">
            <button @click="removeWord(index)">Remove</button>
          </div>
        </div>
        <button @click="addWord" class="add-word-btn">Add Word</button>
      </div>

      <div v-else-if="inputMethod === 'csv'" class="csv-upload">
        <h3>Upload CSV</h3>
        <input type="file" accept=".csv" @change="handleFileUpload">
      </div>

      <button @click="saveCategory" class="save-btn">Save Category</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      categoryName: '',
      inputMethod: 'manual',
      words: [{ word: '', translation: '' }],
    };
  },
  methods: {
    addWord() {
      this.words.push({ word: '', translation: '' });
    },
    removeWord(index) {
      this.words.splice(index, 1);
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          // Parse CSV data and update words array
          const csvData = reader.result;
          // Your CSV parsing logic here
          console.log(csvData);
        };
        reader.readAsText(file);
      }
    },
    async saveCategory() {
      // Validate inputs and save category
      const response = await axios.post(import.meta.env.VITE_API_URL + '/new-category', {
        categoryName: this.categoryName,
        words: this.words,
      });
      console.log('Category Name:', this.categoryName);
      console.log('Words:', this.words);
    },
  },
};
</script>

<style scoped>
.new-category {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.panel {
  background-color: #f2f2f2;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 70%; /* Increased width */
  padding: 2rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.category-name,
.input-method,
.manual-input,
.csv-upload {
  margin-bottom: 1rem;
}

input[type="text"] {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  height: 30px; /* Reduced height */
}

input[type="radio"] {
  margin-right: 0.5rem;
}

.word-input-container {
  max-height: 300px; /* Adjust the max height as needed */
  overflow-y: auto;
}

.word-input {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.word-input input {
  margin-right: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.word-input button {
  padding: 0.5rem;
  border: none;
  background-color: #6366f1;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.word-input button:hover {
  background-color: #4245eb;
}

.add-word-btn,
.save-btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #6366f1;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.add-word-btn:hover,
.save-btn:hover {
  background-color: #4245eb;
}
</style>
