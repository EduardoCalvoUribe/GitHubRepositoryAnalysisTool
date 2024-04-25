<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <TheWelcome />
  </main>
  <header>
    
    <div class="wrapper">
      <HelloWorld msg="Repository Analysis Tool" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/RepositoryAnalysis">Repository Analysis</RouterLink>
      </nav>
    </div>
  </header>
</template>
