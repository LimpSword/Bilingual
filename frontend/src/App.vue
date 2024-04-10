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