<script setup>
import RowBox from './components/RowBox.vue'
</script>

<template>
  <header>
    <div>
      GitHub Analysis Tool (GAT)
    </div>
  </header>

  <main>
    <RowBox n_blocks=5 />
    <RowBox n_blocks=1 />
    <RowBox n_blocks=3 />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

</style>
