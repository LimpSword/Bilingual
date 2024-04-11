<template>
  <div class="not-found h-[calc(100vh-4rem)]">
    <h1>404</h1>
    <h3>Page not found</h3>
  </div>
</template>

<style scoped>
  .not-found {
    display: flex;
    flex-direction: column;
    place-items: center;
    place-content: center;
    font-size: 2rem;
    color: var(--color-text);
  }

  h1 {
    font-size: 5rem;
    font-weight: 500;
    margin: 0;
    color: var(--color-heading);
  }

  h3 {
    font-size: 1.5rem;
    font-weight: 400;
    margin: 0;
    color: var(--color-text);
  }
</style>