<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';
import { state } from '../repoPackage.js';
import { getGradientColor } from '../colorUtils.js';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const pullpackage = ref(null);
    const goBack = () => {
      router.go(-1); // Go back to the previous page
    };

    if (state.githubResponse) {
      localStorage.setItem('data', JSON.stringify(state.githubResponse));
    }
    const storedData = localStorage.getItem('data');
    onMounted(async () => {
      if (storedData) {
        state.githubResponse = JSON.parse(storedData);
      }
      if (state.githubResponse) {
        for (let i = 0; i < state.githubResponse.Repo.pull_requests.length; i++) {
          if (state.githubResponse.Repo.pull_requests[i].url == decodeURIComponent(route.params.url)) {
            pullpackage.value = state.githubResponse.Repo.pull_requests[i];
            break;
          }
        }
      }
      localStorage.setItem('data', JSON.stringify(state.githubResponse));
    });

    const scoreColor = computed(() => {
      const score = pullpackage.value ? pullpackage.value.average_semantic : 0;
      return {
        border: `5px solid ${getGradientColor(score, 10)}`,
        padding: '10px',
        paddingTop: '8px',
      };
    });

    return {
      pullpackage,
      goBack,
      scoreColor,
    };
  },
}
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

  <div v-if="pullpackage" class="grid-container-2">
    <div class="info-section">
      <div class="stat-container">
        Number of Commits: {{ pullpackage.number_commits ? pullpackage.number_commits : 'N/A' }}
      </div>
    </div>

    <div class="info-section">
      <div class="stat-container">
        Number of Comments: {{ pullpackage.number_comments ? pullpackage.number_comments : 'N/A' }}
      </div>
    </div>

    <div class="info-section">
      <div :style="scoreColor" class="stat-container">
        Average Semantic Score: {{ pullpackage.average_semantic ? pullpackage.average_semantic.toFixed(2) : 'N/A' }}/100
      </div>
    </div>
  </div>

  <div v-if="pullpackage" class="grid-container" style="max-height: 300px; overflow-y: auto;">
    <div class="grid-item" style="border-radius: 10px;" v-for="commit in pullpackage.commits" :key="commit.id">
      {{ commit.title }}
      <div>Date: {{ commit.date }}</div>
      <div>User: {{ commit.user }}</div>
      <div>Semantic Score: {{ commit.semantic_score.toFixed(2) }}</div>
      <div>Updated At: {{ commit.updated_at }}</div>
    </div>
  </div>

  <button @click="goBack" class="button-6"
    style="width: 50px; height: 50px; justify-content: center; font-size: 90%; margin-top: 20px;">Back</button>
</template>

<style scoped>
@media (min-width: 1024px) {
  .grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
  }

  .grid-container-2 {
    display: flex;
    grid-template-columns: repeat(3, 1fr);
    align-items: center;
    justify-content: space-evenly;
    gap: 10px;
    padding: 10px;
  }

  .grid-item {
    background-color: #157eff4d;
    padding: 10px;
    border: 1px solid #ccc;
  }
}

.stat-container {
  background-color: white;
  border: 1px solid #157eff4d;
  border-radius: 5px;
  width: 100%;
  height: 50px;
  width: 300px;
  margin-top: 20px;
  justify-content: center;
  text-align: center;
  padding: 4%;
}
</style>
