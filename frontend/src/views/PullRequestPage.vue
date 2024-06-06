<template>
  <header>
    <router-link :to="`/repoinfo/${repositoryId}`">Repository Information</router-link>
    <router-link style="margin-left: 2%" to="/prpage">Pull Requests</router-link>
    <router-link style="margin-left: 2%" to="/commitpage">Commits</router-link>
    <router-link style="margin-left: 2%" to="/commentpage">Comments</router-link>
  </header>

  <router-view />

  <header>
    <div v-if="pullpackage" style="font-size: 180%; margin-top: 30px;">
      {{ pullpackage.title }}
    </div>
  </header>

  <div v-if="pullpackage" style=" display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px; font-size: larger;" for="commits">Commits:</label>
      <div id="commits" class="row" v-for="commit in pullpackage.commits">
        <router-link :to="{ path: '/commitpage' + commit.url}"><button class="button-6">
            <span><h2 style="margin-left: 0.3rem;">{{ commit.title }}</h2></span>
            <span class="last-accessed">Author: {{ commit.user }}</span>
            <span class="last-accessed">Date: {{ commit.date }}</span>
        </button></router-link>
      </div>
    </div>
  </div>


  
  <div v-if="pullpackage">
    <body>
      This is a pull request by {{ pullpackage.user }} created on {{ pullpackage.date }}. 

      <div class="grid-container">
        <div id="commits" class="row" v-for="commit in pullpackage.commits">
          <div class="grid-item">
          {{ commit.title }}
          <body>
            Date: {{ commit.date }}
            <div>
              User: {{ commit.user }}
            </div>
            <div>
              Semantic Score {{ commit.semantic_score }}
            </div>
            <div>
              Updated At: {{ commit.updated_at }}
            </div>
          </body>
          </div>
        </div>
      </div>
    </body>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import fakejson from '../test.json';
import { useRoute } from 'vue-router';
import { state } from '../repoPackage.js';
import CommitPage from './CommitPage.vue';

export default {
  setup() {
    const route = useRoute();
    const pullpackage = ref(null);

    onMounted(async () => {
      console.log('onMounted');
      console.log(state.githubResponse);
      if (state.githubResponse) {
        console.log('in if');
        for (let i=0; i < state.githubResponse.Repo.pull_requests.length - 1; i++) {
          if (state.githubResponse.Repo.pull_requests[i].number == route.params.id) {
            pullpackage.value = state.githubResponse.Repo.pull_requests[i];
          }
        }
        console.log(pullpackage.value);
      }
      if (pullpackage.value) {
        console.log(pullpackage.value.title)
      } else {
        console.log('failure')
      }
    });

    return {
      state,
      pullpackage,
    };
  },

  data() {

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
    height: auto;
    padding: 10px;
  }

  .grid-item {
    background-color: #157eff4d; /* Background color for grid items */
    padding: 10px; /* Padding inside grid items */
    text-align: left; /* Centering text inside grid items */
    border: 1px solid #ccc; /* Border for grid items */
    min-height: 50px;
    height: auto;
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
