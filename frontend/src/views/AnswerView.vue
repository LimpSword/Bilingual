<template>
  <div id="app">
    <main>
      <div class="panel">
        <div class="panel-header">
          <h2>{{ term }}</h2>
        </div>
        <div class="panel-body">
          <input v-model="translation" type="text" placeholder="Type the translation" />
          <div class="button-container">
            <button @click="submitTranslation">Answer</button>
            <button @click="showHint = false" v-if="showHint">Don't know?</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      term: "",
      translation: "",
      showHint: true,
    };
  },
  async created() {
    const response = await axios.get('/random-word')
    this.term = response.data.english
  },
  methods: {
    async submitTranslation() {
      const response = await axios.post('/check-translation', {
        english: this.term,
        french: this.translation
      })
      if (response.data.correct) {
        alert('Correct!')
        const newResponse = await axios.get('/random-word')
        this.term = newResponse.data.english
        this.translation = ''
      } else {
        alert('Incorrect. The correct translation is ' + response.data.correctTranslation)
        this.translation = ''
      }
    },
  },
};
</script>

<style scoped>
#app {
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #333;
  margin-top: 60px;
}

.panel {
  background-color: #fff;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 800px;
  margin: 2rem auto;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: left;
}

.panel-header {
  width: 100%;
  margin-bottom: 7rem;
}

.panel-header h2 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.panel-body {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #6366f1;
}

.button-container {
  display: flex;
  justify-content: center;
}

.button-container button {
  background-color: #6366f1;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  margin: 0 0.5rem;
  transition: background-color 0.3s ease;
}

.button-container button:hover {
  background-color: #4245eb;
}
</style>