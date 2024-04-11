<template>
</template>

<script setup>
import {signOut} from "@/session_utils.js";

signOut();

window.location.href = '/';
</script>