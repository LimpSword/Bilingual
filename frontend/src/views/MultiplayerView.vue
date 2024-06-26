<template>
  <div id="remove-when-game">
    <h1 class="text-4xl text-center mt-[calc(3vh)] leading-6 font-semibold text-gray-700">Play with someone!</h1>
    <div class="flex py-12 px-4 sm:px-6 lg:px-8">
      <!-- Left Pane -->
      <div class="hidden lg:flex items-center justify-center flex-1 text-black">
        <div class="max-w-md">
          <p class="text-2xl font-semibold">Play against another person to gain Elo and expand your vocabulary!</p>
          <p class="mt-5 text-xl">The vocabulary in multiplayer is limited but is expanding with your Elo!</p>
          <p class="mt-3">Currently only available from French to English</p>
        </div>
      </div>
      <!-- Right Pane -->
      <div class="w-full lg:w-1/2 flex items-center justify-center">
        <div class="w-full p-6">
          <div class="mt-12 flex flex-col lg:flex-row items-center justify-between">
            <div class="w-full mb-2 lg:mb-0">
              <button id="buttonInQueue" @click="joinQueue()"
                      class="shadow-lg w-2/3 h-20 hidden flex m-auto justify-center items-center gap-2 bg-red-400 text-2xl text-white p-2 rounded-md hover:bg-red-500 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition-colors duration-300">
                <img class="w-10" src="@/assets/multiplayer_icon.png" alt="">
                Quit the queue
              </button>
              <button id="buttonNotInQueue" v-if="!isInQueue" @click="joinQueue()"
                      class="shadow-lg w-2/3 h-20 flex m-auto justify-center items-center gap-2 bg-green-400 text-2xl text-white p-2 rounded-md hover:bg-green-500 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition-colors duration-300">
                <img class="w-10" src="@/assets/multiplayer_icon.png" alt="">
                Join the queue
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div id="add-when-game" class="hidden">
    <div class="flex justify-center items-center min-h-[calc(50vh)]">
      <div class="bg-gray-50 rounded-lg shadow-lg p-8 min-w-[calc(50%)] mx-auto bg-opacity-60">
        <h1 class="text-5xl font-bold text-yellow-500 mb-4 hidden" id="result"></h1>
        <h1 class="text-3xl font-bold text-gray-800 mb-4 hidden" id="start-timer"></h1>
        <h1 class="text-2xl font-bold text-gray-700 mb-4 hidden" id="opponent"></h1>
        <ConfettiExplosion v-if="visible"/>
        <h1 id="to-translate" class="text-2xl font-bold text-gray-800 mb-4">Word to translate:</h1>
        <h2 class="text-lg font-semibold text-gray-700 mb-2">Translation</h2>
        <input type="text" placeholder="Your translation" id="translation"
               class="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4">
        <button @click="sendTranslation"
                class="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition-colors duration-300">
          Submit
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import ConfettiExplosion from "vue-confetti-explosion";
import {nextTick, ref} from "vue";
import {isUserLoggedIn} from "@/session_utils.js";

let isInQueue = false
let ws

let round = 0

const visible = ref(false);

function sendTranslation() {
  const translation = document.getElementById("translation").value
  if (translation !== "") {
    ws.send(translation)
    document.getElementById("translation").value = ""
  }
}

function joinQueue() {
  isInQueue = !isInQueue
  if (isInQueue) {
    document.getElementById("buttonInQueue").classList.remove("hidden")
    document.getElementById("buttonNotInQueue").classList.add("hidden")

    // Connect to the WebSocket server
    ws = new WebSocket(import.meta.env.VITE_WS_URL)
    ws.onopen = () => {
      console.log('Connected to the WebSocket server')
      if (isUserLoggedIn()) {
        ws.send("/name " + localStorage.getItem("username") + " " + localStorage.getItem("email"))
      } else {
        ws.send("/name anonymous email")
      }
      // wait for "hello"
      ws.onmessage = (event) => {
        const message = event.data
        if (message.startsWith("/hello")) {
          document.getElementById("remove-when-game").classList.add("hidden")
          document.getElementById("add-when-game").classList.remove("hidden")

          let opponent = message.split(" ")[1]
          document.getElementById("opponent").innerText = "You are playing against " + opponent
          document.getElementById("opponent").classList.remove("hidden")

          // start the timer
          let time = 3
          document.getElementById("start-timer").classList.remove("hidden")
          const timer = setInterval(() => {
            document.getElementById("start-timer").innerText = "Game starting in " + time + " seconds"
            time--
            if (time < 0) {
              clearInterval(timer)
              document.getElementById("start-timer").classList.add("hidden")
            }
          }, 1000)
        } else {
          if (message.startsWith("/end")) {
            // finished
            ws.close()

            // has won?
            const result = message.split(" ")[1]
            if (result === "win") {
              document.getElementById("result").innerText = "You have won the game! 🎉"
              document.getElementById("result").classList.remove("hidden")
            } else {
              document.getElementById("result").innerText = "You have lost the game 😢"
              document.getElementById("result").classList.remove("hidden")
            }

            // Wait 10s
            setTimeout(() => {
              document.getElementById("remove-when-game").classList.remove("hidden")
              document.getElementById("add-when-game").classList.add("hidden")

              // Refresh the page
              location.reload()
            }, 10000)
          } else {
            // if message starts with result then it is the result of the translation
            if (message.startsWith("/result")) {
              const result = message.split(" ")[1]
              document.getElementById("start-timer").classList.remove("hidden")
              if (result === "success") {
                document.getElementById("start-timer").innerText = "You are correct! Round won! 🎉"

                async function confetti() {
                  visible.value = false;
                  await nextTick();
                  visible.value = true;
                }

                confetti()
              } else {
                document.getElementById("start-timer").innerText = "You lost the round 😢"
              }
              setTimeout(() => {
                document.getElementById("start-timer").classList.add("hidden")
              }, 5000)
            } else {
              round++
              // update the word to translate
              document.getElementById("to-translate").innerText = "Word to translate (" + round + "/5): " + message

              // wait 4.9s
              setTimeout(() => {
                sendTranslation()
              }, 4900)
            }
          }
        }
      }
    }
  } else {
    document.getElementById("buttonInQueue").classList.add("hidden")
    document.getElementById("buttonNotInQueue").classList.remove("hidden")
  }
}
</script>