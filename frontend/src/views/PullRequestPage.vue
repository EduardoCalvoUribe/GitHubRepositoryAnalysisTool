<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { state } from '../repoPackage.js';

export default {
  setup() {
    const route = useRoute();
    const pullpackage = ref(null);

    onMounted(async () => {
      if (state.githubResponse) {
        for (let i = 0; i < state.githubResponse.Repo.pull_requests.length; i++) {
          if (state.githubResponse.Repo.pull_requests[i].url == decodeURIComponent(route.params.url)) {
            pullpackage.value = state.githubResponse.Repo.pull_requests[i];
            break;
          }
        }
      }
    });

    return {
      pullpackage,
    };
  },
};
</script>

<template>
  <header>
    <div v-if="pullpackage" style="margin-top: 50px">
      <h1>Pull Request</h1>
      <div style="font-size: 180%; margin-bottom: 20px; margin-top: 40px;">{{ pullpackage.title }}</div>
      <div>User: {{ pullpackage.user }}</div>
      <div>Created: {{ pullpackage.date }}</div>
      <div>Description: {{ pullpackage.body }}</div>
    </div>
  </header>

  <div v-if="pullpackage" class="grid-container">
    <div class="info-section">
      <button class="button-6" style="margin-top: 10px; justify-content: center; height:100px; width:150px">
        Number of Commits: {{ pullpackage.number_commits ? pullpackage.number_commits : 'N/A' }}
      </button>
    </div>

    <div class="info-section">
      <button class="button-6" style="margin-top: 10px; justify-content: center; height:100px; width:150px">
        Number of Comments: {{ pullpackage.number_comments ? pullpackage.number_comments : 'N/A' }}
      </button>
    </div>

    <div class="info-section">
      <button class="button-6" style="margin-top: 10px; justify-content: center; height:100px; width:150px">
        Average Semantic Score: {{ pullpackage.average_semantic ? pullpackage.average_semantic : 'N/A' }}
      </button>
    </div>
  </div>


  <div v-if="pullpackage" class="grid-container">
    <div class="grid-item" v-for="commit in pullpackage.commits" :key="commit.id">
      {{ commit.title }}
      <div>Date: {{ commit.date }}</div>
      <div>User: {{ commit.user }}</div>
      <div>Semantic Score: {{ commit.semantic_score }}</div>
      <div>Updated At: {{ commit.updated_at }}</div>
    </div>
  </div>

  <router-link :to="{path: '/' }">
    <button class="button-6" style="width: 50px; height: 50px; justify-content: center; font-size: 90%;">Back</button>
  </router-link>
</template>

<style scoped>
@media (min-width: 1024px) {
  .grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
  }

  .grid-item {
    background-color: #157eff4d;
    padding: 10px;
    border: 1px solid #ccc;
  }
}
</style>
