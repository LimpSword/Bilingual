<template>
  <div id="app">
    <main>
      <div class="panel">
        <div class="panel-header">
          <h2>{{ term }}</h2>
        </div>
        <div class="panel-body">
          <input v-model="translation" type="text" placeholder="Type the translation" />
          <transition name="fade">
            <div v-if="showErrorMessage" class="error-message">Incorrect translation. Please try again.</div>
          </transition>
          <div class="button-container">
            <button @click="checkTranslation" v-if="showCheckButton">Check</button>
            <button @click="nextWord" v-else class="next-button">Next Word</button>
          </div>
          <transition name="fade">
            <div v-if="showCorrectMessage" class="correct-message">Correct!</div>
          </transition>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      term: "",
      translation: "",
      showHint: true,
      showErrorMessage: false,
      showCheckButton: true,
      showCorrectMessage: false
    };
  },
  async created() {
    await this.getRandomWord();
  },
  methods: {
    async getRandomWord() {
      const response = await axios.get(import.meta.env.VITE_API_URL + '/random-word');
      this.term = response.data.english;
    },
    async checkTranslation() {
      const response = await axios.post(import.meta.env.VITE_API_URL + '/check-translation', {
        english: this.term,
        french: this.translation
      });
      if (response.data.correct) {
        this.showCorrectMessage = true;
        setTimeout(() => {
          this.showCorrectMessage = false;
          this.nextWord();
        }, 2000); // Hide correct message after 2 seconds
      } else {
        this.showErrorMessage = true;
      }
    },
    async nextWord() {
      this.translation = "";
      this.showErrorMessage = false;
      await this.getRandomWord();
      this.showCheckButton = true;
    }
  }
};
</script>

<style scoped>
/* Your existing styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.correct-message {
  color: green;
  margin-top: 1rem;
  font-weight: bold;
}

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

.error-message {
  color: red;
  margin-bottom: 1rem;
}

</style>