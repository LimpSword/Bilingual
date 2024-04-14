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
            <div v-if="showErrorMessage" class="error-message">{{ errorMessage }}</div>
          </transition>
          <div class="button-container">
            <button @click="checkTranslation" v-if="showCheckButton">Answer</button>
            <button @click="iWasCorrect" v-if="showCorrectButton">I was correct</button>
            <button @click="skip" v-if="showSkipButton">Skip</button>
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

function levenshteinDistance(str1, str2) {
  const m = str1.length;
  const n = str2.length;

  // Create a matrix to store the distances
  const dp = [];
  for (let i = 0; i <= m; i++) {
    dp[i] = [];
    dp[i][0] = i;
  }
  for (let j = 0; j <= n; j++) {
    dp[0][j] = j;
  }

  // Calculate the distances
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1, // Deletion
        dp[i][j - 1] + 1, // Insertion
        dp[i - 1][j - 1] + cost // Substitution
      );
    }
  }

  // Return the distance between the two strings
  return dp[m][n];
}


export default {
  data() {
    return {
      term: "",
      translation: "",
      showErrorMessage: false,
      showCheckButton: true,
      showCorrectButton: false,
      showSkipButton: false,
      showCorrectMessage: false,
      errorMessage: "Incorrect translation. Please try again."
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
        if (levenshteinDistance(response.data.correctTranslation, this.translation) <= 2 || this.term.toLowerCase() === this.translation.toLowerCase()){
          this.errorMessage = "Incorrect translation. Did you mean " + response.data.correctTranslation + "?";
          this.showErrorMessage = true;
          this.showCorrectButton = true;
          this.showSkipButton = true;
        } else {
          this.errorMessage = "Incorrect translation. It is " + response.data.correctTranslation + " please write it before continuing.";
          this.showErrorMessage = true;
          this.showSkipButton = true;
          this.showCorrectButton = false;
        }
      }
    },
    async iWasCorrect() {
      // Logic to handle the "I was correct" button click
      // You can add your custom logic here
      await this.nextWord();
    },
    async skip() {
      // Logic to handle the "Skip" button click
      // You can add your custom logic here
      await this.nextWord();
    },
    async nextWord() {
      this.translation = "";
      this.showErrorMessage = false;
      await this.getRandomWord();
      this.showCheckButton = true;
      this.showCorrectButton = false;
      this.showSkipButton = false;
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