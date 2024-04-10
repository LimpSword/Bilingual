<script setup>
import { RouterView } from 'vue-router'
  import { onMounted } from "vue";
  import { Tooltip, initTWE } from "tw-elements";

  onMounted(() => {
    initTWE({ Tooltip }, { allowReinits: true });
  });
</script>

<template>
  <RouterView />
</template>