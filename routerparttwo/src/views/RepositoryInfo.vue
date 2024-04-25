<template>
    <div class="grid-container">
      <div class="grid-item" v-for="item in items" :key="item.id">
        {{ item.text }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        items: [
          { id: 1, text: 'Number of Pull Requests', },
          { id: 2, text: 'Number of Commits' },
          { id: 3, text: 'Extra Repository Information' },
          // Add more items as needed
        ]
      }
    }
  }
  </script>
  
  <style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* Adjust the number of columns as needed */
    gap: 10px; /* Spacing between grid items */
  }
  
  .grid-item {
    background-color: #b60aad; /* Background color for grid items */
    padding: 50px; /* Padding inside grid items */
    text-align: center; /* Centering text inside grid items */
    border: 1px solid #ccc; /* Border for grid items */
  }
</style>
  