<script setup>
import {RouterView} from 'vue-router'
import {onMounted} from "vue";
import {Tooltip, initTWE} from "tw-elements";
import Navbar from "@/components/Navbar.vue";

onMounted(() => {
  initTWE({Tooltip}, {allowReinits: true});
});
</script>

<template>
  <Navbar/>
  <RouterView/>
</template>

<style>
body {
  background: rgb(212,252,252);
  background: linear-gradient(0deg, rgba(212,252,252,1) 0%, rgba(251,248,242,1) 100%);
}
</style>