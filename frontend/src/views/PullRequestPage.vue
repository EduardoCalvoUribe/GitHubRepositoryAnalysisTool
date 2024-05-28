<template>
  <div>
    <header>
      <router-link :to="`/repoinfo/${repositoryId}`">Repository Information</router-link>
      <router-link style="margin-left: 2%" to="/prpage">Pull Requests</router-link>
      <router-link style="margin-left: 2%" to="/commitpage">Commits</router-link>
      <router-link style="margin-left: 2%" to="/commentpage">Comments</router-link>
    </header>

    <router-view />

    <header>
      <div style="font-size: 180%; margin-top: 30px;">
        Pull Request Page
      </div>
    </header>
    <div style="font-size: 100%; color: grey; margin-bottom: 20px;">
      This is the pull request information.
    </div>

    <div class="grid-container" v-for="pullitem in pullitems" :key="pullitem.id">
      <div class="grid-item" v-for="item in items" :key="item.id">
        {{ item.text }}
      </div>
    </div>
  </div>
</template>

<script>
import fakejson from '../test.json';
import { useRoute } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const data = { id: route.params.id };
    console.log('Route data:', data);

    return {
      data,
    };
  },

  data() {
    return {
      repositoryId: fakejson.repository.pull_requests.id,
      selectedRange: null,
      pullitems: [
        { id: 1, text: 'Pull request ID: ' + fakejson.repository.pull_requests[0].commits[0].id }
      ],
      items: [
        { id: 1, text: 'Date: ' + fakejson.repository.pull_requests[0].commits[0].date },
        { id: 2, text: 'Author: ' + fakejson.repository.pull_requests[0].commits[0].author },
        { id: 3, text: 'Message: ' + fakejson.repository.pull_requests[0].commits[0].message },
        { id: 4, text: 'Semantic Score: ' + fakejson.repository.pull_requests[0].commits[0].semantic_score },
      ],
    };
  },
};
</script>

<style scoped>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
  .grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* Adjust the number of columns as needed */
    gap: 10px; /* Spacing between grid items */
  }

  .grid-item {
    background-color: #157eff4d; /* Background color for grid items */
    padding: 50px; /* Padding inside grid items */
    text-align: center; /* Centering text inside grid items */
    border: 1px solid #ccc; /* Border for grid items */
  }

  .box-container {
    display: flex;
    gap: 10px; /* Space between boxes */
    justify-content: center; /* Center the boxes horizontally */
    padding: 20px 0; /* Optional: padding around the container */
    text-align: center;
  }

  .box {
    flex: 1; /* Each box takes equal space */
    padding: 20px;
    background-color: rgb(255, 255, 255);
    text-align: center;
    border: 1px solid #ffffff;
  }
}
</style>
