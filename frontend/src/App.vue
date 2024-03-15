<script setup>
import RowBox from './components/RowBox.vue'

getFakeRequest();

async function getFakeRequest() {
  try {
    // Fake API fetch
    const response = await fetch('https://jsonplaceholder.typicode.com/posts/1') 

    // takes response, converts to JavaScript Promise object
    const json = await response.json() 

    // Selects first div with 'fake_request' id attribute
    const fakeDiv = document.getElementById('fake_request');

    // Inserts content into that div in the specified format
    // For full JSON string, use: '<pre>' + JSON.stringify(json, null, 2) + '</pre>'
    fakeDiv.innerHTML = '<p><h4>Fake Request Data:</h4><br>' + json.title + json.body + '</p>';

  } catch (error) {
    console.error('Error:', error)
  }   
}

</script>

<template>
  <header>
    <div>
      GitHub Analysis Tool (GAT)
    </div>
  </header>

  <main>
    <br><br>
    <div id="fake_request"></div>
    <br>
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
