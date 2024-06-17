<template>
  <header>
    <!-- <RouterLink to="/">Home</RouterLink> -->
  </header>

  <header>
    <div style="font-size: 180%; margin-top: 30px;">
      User page
    </div>
  </header>

  <main>
    <div style="margin-top: 20px; display: flex; justify-content: center; align-items: center;">
      <Dropdown v-model="localSelectedUser" :options="users" optionLabel="label" placeholder="Select a user"
        style="width: 250px; margin-right: 10px;" />
      <div class="stat-box" :style="scoreColor">
        <strong>Avg. Semantic Score</strong>
        <div>{{ roundedAverageSemanticScore }}</div>
      </div>
    </div>

    <!-- <div style="margin-top: 10px; display: flex; justify-content: center;">
      <button @click="toggleDetails" class="button-6" style="width: 200px;">Further Analytics</button>
    </div> -->

    <!-- v-if="showDetails" -->
    <div class="details-section">
      <div class="stat-box">
        <strong>Total Pull Requests</strong>
        <div>{{ totalPullRequests }}</div>
      </div>
      <div class="stat-box">
        <strong>Total Commits</strong>
        <div>{{ totalCommits }}</div>
      </div>
      <div class="stat-box">
        <strong>Total Comments</strong>
        <div>{{ totalComments }}</div>
      </div>
      <div class="stat-box">
        <strong>Avg. PR Title Semantic Score</strong>
        <div>{{ roundedAveragePrTitleSemanticScore }}</div>
      </div>
      <div class="stat-box">
        <strong>Avg. PR Body Semantic Score</strong>
        <div>{{ roundedAveragePrBodySemanticScore }}</div>
      </div>
      <div class="stat-box">
        <strong>Avg. Commit Semantic Score</strong>
        <div>{{ roundedAverageCommitSemanticScore }}</div>
      </div>
      <div class="stat-box">
        <strong>Avg. Comment Semantic Score</strong>
        <div>{{ roundedAverageCommentSemanticScore }}</div>
      </div>
    </div>

    <div v-if="userDetails">
      <section style="margin-top: 20px;">
        <h3>Pull Requests</h3>
        <div class="scrollable-section">
          <div v-for="pr in userDetails.pullRequests" :key="pr.id" class="info-section">
            <div class="stat-container">
              <div><strong>Title:</strong> {{ pr.title }}</div>
              <div><strong>Date:</strong> {{ pr.date }}</div>
              <div><strong>Semantic Score (Title):</strong> {{ round(pr.pr_title_semantic) }}</div>
              <div><strong>Semantic Score (Body):</strong> {{ round(pr.pr_body_semantic) }}</div>
              <div><strong>Average Semantic Score (Commits):</strong> {{ round(pr.average_semantic) }}</div>
            </div>
          </div>
        </div>
      </section>

      <section style="margin-top: 20px;">
        <h3>Commits</h3>
        <div class="scrollable-section">
          <div v-for="commit in userDetails.commits" :key="commit.id" class="info-section">
            <div class="stat-container">
              <div><strong>Title:</strong> {{ commit.title }}</div>
              <div><strong>Date:</strong> {{ commit.date }}</div>
              <div><strong>Semantic Score:</strong> {{ round(commit.semantic_score) }}</div>
            </div>
          </div>
        </div>
      </section>

      <section style="margin-top: 20px;">
        <h3>Comments</h3>
        <div class="scrollable-section">
          <div v-for="comment in userDetails.comments" :key="comment.id" class="info-section">
            <div class="stat-container">

              <div><strong>Body:</strong> {{ comment.body }}</div>
              <div><strong>Date:</strong> {{ comment.date }}</div>
              <div><strong>Semantic Score:</strong> {{ round(comment.semantic_score) }}</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>

  <button @click="goBack" class="button-6"
    style="width: 50px; height: 50px; font-size: 90%; margin-top: 20px; text-align: center; padding: 0px;">Back</button>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { state } from '../repoPackage.js';
import { useRouter, useRoute } from 'vue-router';
import Dropdown from 'primevue/dropdown';
import { getGradientColor } from '../colorUtils.js';

export default {
  components: {
    Dropdown,
  },
  setup(props, { emit }) {
    const router = useRouter();
    const route = useRoute();
    const selectedUserQuery = route.query.selectedUser;
    const localSelectedUser = ref(selectedUserQuery ? { label: selectedUserQuery, value: selectedUserQuery } : null);
    const averageSemanticScore = ref(0);
    const userDetails = ref(null);
    const totalPullRequests = ref(0);
    const totalCommits = ref(0);
    const totalComments = ref(0);
    const averagePrTitleSemanticScore = ref(0);
    const averagePrBodySemanticScore = ref(0);
    const averageCommitSemanticScore = ref(0);
    const averageCommentSemanticScore = ref(0);
    // const showDetails = ref(false);

    const goBack = () => {
      router.go(-1); // Go back to the previous page
    };

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
      if (localSelectedUser.value && state.githubResponse && state.githubResponse.Repo.pull_requests) {
        let totalScore = 0;
        let prTitleScore = 0;
        let prBodyScore = 0;
        let commitScore = 0;
        let commentScore = 0;
        let prCount = 0;
        let commitCount = 0;
        let commentCount = 0;
        let count = 0;
        const pullRequests = [];
        const commits = [];
        const comments = [];

        state.githubResponse.Repo.pull_requests.forEach(pr => {
          if (pr.user === localSelectedUser.value.value) {
            totalScore += pr.pr_title_semantic + pr.pr_body_semantic + pr.average_semantic;
            prTitleScore += pr.pr_title_semantic;
            prBodyScore += pr.pr_body_semantic;
            count += 3;
            prCount++;
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
            if (commit.user === localSelectedUser.value.value) {
              totalScore += commit.semantic_score;
              commitScore += commit.semantic_score;
              count++;
              commitCount++;
              console.log(commit.name, "name");
              commits.push({
                id: commit.id,
                title: commit.title,
                date: commit.date,
                semantic_score: commit.semantic_score,
              });
            }
          });

          pr.comments.forEach(comment => {
            if (comment.user === localSelectedUser.value.value) {
              totalScore += comment.semantic_score;
              commentScore += comment.semantic_score;
              count++;
              commentCount++;
              comments.push({
                id: comment.id,
                body: comment.body,
                date: comment.date,
                semantic_score: comment.semantic_score,
              });
            }
          });
        });

        averageSemanticScore.value = count ? (totalScore / count).toFixed(2) : 0;
        averagePrTitleSemanticScore.value = prCount ? (prTitleScore / prCount).toFixed(2) : 0;
        averagePrBodySemanticScore.value = prCount ? (prBodyScore / prCount).toFixed(2) : 0;
        averageCommitSemanticScore.value = commitCount ? (commitScore / commitCount).toFixed(2) : 0;
        averageCommentSemanticScore.value = commentCount ? (commentScore / commentCount).toFixed(2) : 0;
        totalPullRequests.value = prCount;
        totalCommits.value = commitCount;
        totalComments.value = commentCount;
        userDetails.value = { pullRequests, commits, comments };
      }
    };

    // const toggleDetails = () => {
    //   showDetails.value = !showDetails.value;
    // };

    const updateUserInURL = (user) => {
      router.replace({ path: '/userpage', query: { selectedUser: user.value } });
    };

    watch(localSelectedUser, (newUser) => {
      emit('update:selectedUser', newUser);
      fetchUserData();
      if (newUser) {
        updateUserInURL(newUser);
      }
    });

    onMounted(() => {
      if (state.githubResponse) {
        localStorage.setItem('data', JSON.stringify(state.githubResponse));
      }
      const storedData = localStorage.getItem('data');
      if (storedData) {
        state.githubResponse = JSON.parse(storedData);
      }
      if (localSelectedUser.value) {
        fetchUserData();
      }

    });

    const round = (value) => Math.round(value);

    const roundedAverageSemanticScore = computed(() => round(averageSemanticScore.value));
    const roundedAveragePrTitleSemanticScore = computed(() => round(averagePrTitleSemanticScore.value));
    const roundedAveragePrBodySemanticScore = computed(() => round(averagePrBodySemanticScore.value));
    const roundedAverageCommitSemanticScore = computed(() => round(averageCommitSemanticScore.value));
    const roundedAverageCommentSemanticScore = computed(() => round(averageCommentSemanticScore.value));

    return {
      localSelectedUser,
      averageSemanticScore,
      users,
      userDetails,
      totalPullRequests,
      totalCommits,
      totalComments,
      averagePrTitleSemanticScore,
      averagePrBodySemanticScore,
      averageCommitSemanticScore,
      averageCommentSemanticScore,
      fetchUserData,
      goBack,
      // toggleDetails,
      // showDetails,
      roundedAverageSemanticScore,
      roundedAveragePrTitleSemanticScore,
      roundedAveragePrBodySemanticScore,
      roundedAverageCommitSemanticScore,
      roundedAverageCommentSemanticScore,
      round,
    };
  },
  computed: {
    scoreColor() {
      return {
        border: `5px solid ${getGradientColor(this.roundedAverageSemanticScore, 10)}`,
        padding: '10px',
        paddingTop: '8px',
      }
    }
  },
};
</script>

<style scoped>
.stat-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin: 10px;
  display: inline-block;
  width: 150px;
  text-align: center;
  font-size: 120%;
  background-color: #f9f9f9;
  vertical-align: top;
}

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
  max-height: 400px;
  overflow-y: auto;
}

.detail-button {
  padding: 10px;
  font-size: 90%;
  display: inline-block;
  vertical-align: top;
}

.details-section {
  margin-top: 20px;
}

.button-6 {
  appearance: none;
  background-color: #007bff;
  border: 1px solid #007bff;
  border-radius: 0.375rem;
  box-shadow: none;
  color: #ffffff;
  cursor: pointer;
  display: inline-block;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.25;
  padding: 0.5rem 1rem;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
  user-select: none;
  vertical-align: middle;
}

.button-6:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
</style>
