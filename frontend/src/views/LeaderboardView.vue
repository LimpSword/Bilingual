<template>
  <div class="min-h-[calc(100vh-4rem)] py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:px-6 bg-gray-100">
        <h1 class="text-lg leading-6 font-semibold text-gray-700">Leaderboard</h1>
      </div>
      <div class="px-4 py-5 sm:p-6">
        <table class="w-full">
          <thead>
          <tr class="text-sm font-medium text-gray-500 uppercase bg-gray-50">
            <th scope="col" class="py-3 px-2 w-12">Rank</th>
            <th scope="col" class="py-3 px-6 border-l border-r border-gray-200">Username</th>
            <th scope="col" class="py-3 px-6">Elo</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(player, index) in leaderboard" :key="player.id"
              class="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition duration-150 ease-in-out">
            <td class="py-4 px-2 text-sm font-semibold text-gray-900 w-12">{{ index + 1 }}</td>
            <td class="py-4 px-6 text-sm text-gray-700 border-l border-r border-gray-200">{{ player.username }}</td>
            <td class="py-4 px-6 text-sm text-gray-700">{{ player.elo }}</td>
          </tr>
          </tbody>
        </table>
        <!-- Special states -->
        <div v-if="loading" class="flex justify-center items-center mt-2">
          <div class="loader"></div>
        </div>
        <div v-if="!loading && leaderboard.length === 0" class="text-center text-gray-500 mt-4">
          No players found
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Fetch the leaderboard data from the API
import {ref, onMounted} from 'vue'
import axios from 'axios'

const leaderboard = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await axios.get(import.meta.env.VITE_API_URL + '/leaderboard')
    leaderboard.value = response.data
  } catch (error) {
    console.error('Error fetching leaderboard:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>