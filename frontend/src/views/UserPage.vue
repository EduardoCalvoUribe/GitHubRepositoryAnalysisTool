<template>
  <header>
    <RouterLink to="/">Home</RouterLink>
  </header>

  <header>
    <div style="font-size: 180%; margin-top: 30px;">
      User page
    </div>
  </header>

  <main>
    <div style="margin-top: 20px;">
      <label for="userSelect">Select a User:</label>
      <Dropdown v-model="selectedUser" :options="users" optionLabel="label" placeholder="Select a user" @change="fetchUserData" style="width: 250px;" />
    </div>

    <div v-if="selectedUser" style="margin-top: 20px;">
      <div style="font-size: 180%; margin-bottom: 20px;">
        Average Semantic Score for {{ selectedUser.label }}: {{ averageSemanticScore }}
      </div>

      <div v-if="userDetails">
        <section style="margin-top: 20px;">
          <h3>Pull Requests</h3>
          <div class="scrollable-section">
            <div v-for="pr in userDetails.pullRequests" :key="pr.id" class="info-section">
              <div class="stat-container">
                <div><strong>Title:</strong> {{ pr.title }}</div>
                <div><strong>Date:</strong> {{ pr.date }}</div>
                <div><strong>Semantic Score (Title):</strong> {{ pr.pr_title_semantic }}</div>
                <div><strong>Semantic Score (Body):</strong> {{ pr.pr_body_semantic }}</div>
                <div><strong>Average Semantic Score (Commits):</strong> {{ pr.average_semantic }}</div>
              </div>
            </div>
          </div>
        </section>

        <section style="margin-top: 20px;">
          <h3>Commits</h3>
          <div class="scrollable-section">
            <div v-for="commit in userDetails.commits" :key="commit.id" class="info-section">
              <div class="stat-container">
                <div><strong>Message:</strong> {{ commit.message }}</div>
                <div><strong>Date:</strong> {{ commit.date }}</div>
                <div><strong>Semantic Score:</strong> {{ commit.semantic_score }}</div>
              </div>
            </div>
          </div>
        </section>

        <section style="margin-top: 20px;">
          <h3>Comments</h3>
          <div class="scrollable-section">
            <div v-for="comment in userDetails.comments" :key="comment.id" class="info-section">
              <div class="stat-container">
                <div><strong>Content:</strong> {{ comment.content }}</div>
                <div><strong>Date:</strong> {{ comment.date }}</div>
                <div><strong>Semantic Score:</strong> {{ comment.semantic_score }}</div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </main>

  <router-link :to="{path: '/' }">
    <button class="button-6" style="width: 50px; height: 50px; font-size: 90%; margin-top: 20px">Back</button>
  </router-link>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { state } from '../repoPackage.js';
import Dropdown from 'primevue/dropdown';

export default {
  components: {
    Dropdown,
  },
  setup() {
    const selectedUser = ref(null);
    const averageSemanticScore = ref(0);
    const userDetails = ref(null);

    const users = computed(() => {
      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        const userSet = new Set();
        state.githubResponse.Repo.pull_requests.forEach(pr => {
          userSet.add(pr.user);
          pr.commits.forEach(commit => {
            userSet.add(commit.user);
          });
          pr.comments.forEach(comment => {
            userSet.add(comment.user);
          });
        });
        return Array.from(userSet).map(user => ({ label: user, value: user }));
      }
      return [];
    });

    const fetchUserData = () => {
      if (selectedUser.value && state.githubResponse && state.githubResponse.Repo.pull_requests) {
        let totalScore = 0;
        let count = 0;
        const pullRequests = [];
        const commits = [];
        const comments = [];

        state.githubResponse.Repo.pull_requests.forEach(pr => {
          if (pr.user === selectedUser.value.value) {
            totalScore += pr.pr_title_semantic + pr.pr_body_semantic + pr.average_semantic;
            count += 3;
            pullRequests.push({
              id: pr.number,
              title: pr.title,
              date: pr.date,
              pr_title_semantic: pr.pr_title_semantic,
              pr_body_semantic: pr.pr_body_semantic,
              average_semantic: pr.average_semantic,
            });
          }

          pr.commits.forEach(commit => {
            if (commit.user === selectedUser.value.value) {
              totalScore += commit.semantic_score;
              count++;
              commits.push({
                id: commit.id,
                message: commit.message,
                date: commit.date,
                semantic_score: commit.semantic_score,
              });
            }
          });

          pr.comments.forEach(comment => {
            if (comment.user === selectedUser.value.value) {
              totalScore += comment.semantic_score;
              count++;
              comments.push({
                id: comment.id,
                content: comment.content,
                date: comment.date,
                semantic_score: comment.semantic_score,
              });
            }
          });
        });

        averageSemanticScore.value = count ? (totalScore / count).toFixed(2) : 0;
        userDetails.value = { pullRequests, commits, comments };
      }
    };

    onMounted(() => {
      if (users.value.length > 0) {
        selectedUser.value = users.value[0];
        fetchUserData();
      }
    });

    return {
      selectedUser,
      averageSemanticScore,
      users,
      userDetails,
      fetchUserData,
    };
  },
};
</script>

<style scoped>
.info-section {
  margin-bottom: 20px;
}

.stat-container {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.scrollable-section {
  max-height: 400px; /* Adjust the height as necessary */
  overflow-y: auto;
}
</style>
