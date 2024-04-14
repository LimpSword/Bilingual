<template>
  <div class="flex h-[calc(60vh+10rem)]">
    <!-- Left Pane -->
    <div class="hidden lg:flex items-center justify-center flex-1 text-black">
      <div class="max-w-md text-center">
        <img src="@/assets/online_learning.png">
      </div>
    </div>
    <!-- Right Pane -->
    <div class="w-full lg:w-1/2 flex items-center justify-center">
      <div class="w-full p-6">
        <h1 class="text-7xl font-semibold mb-6 text-black text-center">Learn any language here!</h1>
        <div class="mt-12 flex flex-col lg:flex-row items-center justify-between">
          <div class="w-full mb-2 lg:mb-0">
            <a href="/solo"
                        class="w-2/3 h-20 flex m-auto justify-center items-center gap-2 bg-blue-300 text-2xl text-white p-2 rounded-md hover:bg-blue-400 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition-colors duration-300">
              <img class="w-10"
                   src="@/assets/computer_icon.png"
                   alt="">
              Play Solo
            </a>
          </div>
        </div>
        <div class="mt-12 flex flex-col lg:flex-row items-center justify-between">
          <div class="w-full mb-2 lg:mb-0">
            <a href="/multiplayer"
                        class="w-2/3 h-20 flex m-auto justify-center items-center gap-2 bg-green-400 text-2xl text-white p-2 rounded-md hover:bg-green-500 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition-colors duration-300">
              <img class="w-10" src="@/assets/multiplayer_icon.png" alt="">
              Play Multiplayer
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
RouterLink {
  padding: 0;
  margin: 0;
}
</style>
<script setup lang="ts">
</script>