<script>
import { onMounted } from 'vue';
import { fetchData } from './fetchData.js'

import Badge from './components/Badge.vue';
import BaseSlider from './components/BaseSlider.vue';
import CustomControls from './views/components/CustomControls.vue';


export default {
  components: {
    Badge,
    BaseSlider,
    CustomControls,
  },
  setup() {
    onMounted(async () => {
      try {
        // Fetches json data from specified URL using our fetchData function (will be our backend endpoints)
        const json_response = await fetchData('http://127.0.0.1:8000/github/user');
        const fake_response = await fetchData('http://jsonplaceholder.typicode.com/posts/1');

        // Selects first div with specified id (such as 'github_request')
        const githubDiv = document.getElementById('github_request');
        const fakeDiv = document.getElementById('fake_request');

        console.log(json_response);

        // Inserts content of json into that div in whatever specified format
        githubDiv.innerHTML = '<p><h5>Data from Backend:</h5><br>' + json_response.url + '</p>';
        fakeDiv.innerHTML = '<pre>' + JSON.stringify(fake_response, null, 2) + '</pre>';

      } catch (error) {
        console.error('Error:', error)
      }
    });
  }
};
</script>


<template>
  <header>
    <div>
      GitHub Analysis Tool (GAT)
    </div>
  </header>

  <main>
    <br><br>
    <div id="github_request"></div>
    <br><br>
    <h5>Fake Request:</h5>
    <div id="fake_request"></div>
    <br><br>

    <Badge type="primary" rounded>Primary</Badge>
    <Badge type="info" rounded>Info</Badge>
    <Badge type="danger" rounded>Danger</Badge>
    <Badge type="default" rounded>Default</Badge>
    <Badge type="warning" rounded>Warning</Badge>
    <Badge type="success" rounded>Success</Badge>
    
    <BaseSlider value=10 disabled="" type="primary" ></BaseSlider>

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
