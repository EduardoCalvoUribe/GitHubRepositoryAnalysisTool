<!-- Copyright 2024 Radboud University, Modern Software Development Techniques

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';
import { state } from '../repoPackage.js';
import { getGradientColor } from '../colorUtils.js';

export default {
  setup() {
    /**
     * @constant {Route} route - The current route object.
     */
    const route = useRoute();

    /**
     * @constant {Router} router - The router instance.
     */
    const router = useRouter();

    /**
     * @constant {Ref} pullpackage - A reactive reference to hold the pull request details.
     */
    const pullpackage = ref(null);

    /**
     * Navigates back to the previous page.
     * @function goBack
     */
    const goBack = () => {
      // Go back to the previous page
      router.go(-1); 
    };

    /**
     * Stores the GitHub response data in localStorage if available.
     */
    if (state.githubResponse) {
      localStorage.setItem('data', JSON.stringify(state.githubResponse));
    }

    /**
     * @constant {string} storedData - The GitHub response data retrieved from localStorage.
     */
    const storedData = localStorage.getItem('data');

    /**
     * Fetches and processes the pull request data when the component is mounted.
     * @async
     * @function onMounted
     */
    onMounted(async () => {
      // Check if storedData has a value.
      if (storedData) {
        // Parse data back to JSON format.
        state.githubResponse = JSON.parse(storedData);
      }
      // Check if state.githubReponse has a value.
      if (state.githubResponse) {
        // Loop through all pull requests.
        for (let i = 0; i < state.githubResponse.Repo.pull_requests.length; i++) {
          // Check which pull request matches with given pull request URL.
          if (state.githubResponse.Repo.pull_requests[i].url == decodeURIComponent(route.params.url)) {
            // Fill pullpackage with information about the pull request.
            pullpackage.value = state.githubResponse.Repo.pull_requests[i];
            break;
          }
        }
      }
      localStorage.setItem('data', JSON.stringify(state.githubResponse));
    });

    /**
     * Computes the style for the semantic score based on the score value.
     * @constant {ComputedRef} scoreColor
     * @returns {Object} The style object with the border color set based on the semantic score.
     */
    const scoreColor = computed(() => {
      // Checks if pullpackage has a value and sets score to pull requests average semantic or 0 otherwise.
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
  <!-- Header for the page that shows user, creation date and body of pull request -->
  <header>
    <div v-if="pullpackage" style="margin-top: 50px">
      <h1>Pull Request</h1>
      <div style="font-size: 180%; margin-bottom: 20px; margin-top: 40px;">{{ pullpackage.title }}</div>
      <div>User: {{ pullpackage.user }}</div>
      <div>Created: {{ pullpackage.date }}</div>
      <div>Description: {{ pullpackage.body }}</div>
    </div>
  </header>

  <!-- Info boxes that show general information about pull request -->
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

  <!-- Loop that shows all commits on the pull request -->
  <div v-if="pullpackage" class="grid-container" style="max-height: 300px; overflow-y: auto;">
    <div class="grid-item" style="border-radius: 10px;" v-for="commit in pullpackage.commits" :key="commit.id">
      {{ commit.title }}
      <div>Date: {{ commit.date }}</div>
      <div>User: {{ commit.user }}</div>
      <div>Semantic Score: {{ commit.semantic_score.toFixed(2) }}</div>
      <div>Updated At: {{ commit.updated_at }}</div>
    </div>
  </div>
  
  <!-- Back button to go to previous page -->
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
