<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // Import useRouter
import { state } from '../repoPackage.js';
import CommitPage from './CommitPage.vue';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter(); // Initialize useRouter
    const pullpackage = ref(null);

    const goBack = () => {
      router.go(-1); // Go back to the previous page
    };

    onMounted(async () => {
      if (state.githubResponse) {
        console.log('in if');
        for (let i = 0; i < state.githubResponse.Repo.pull_requests.commits.length - 1; i++) {
          if (state.githubResponse.Repo.pull_requests[i].url == decodeURIComponent(route.params.url)) {
            pullpackage.value = state.githubResponse.Repo.pull_requests[i];
            break;
          }
        }
      }
    });

    return {
      state,
      pullpackage,
      goBack, // Return goBack method
    };
  },
};
</script>

<template>
  <header>
    <RouterLink to="/repoinfo/${id}">Repository Infomation</RouterLink>
    <RouterLink style="margin-left: 2%" to="/prpage">Pull Requests</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commitpage">Commits</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commentpage">Comments</RouterLink>
  </header>

  <RouterView />
  <header>
    <div style="font-size: 180%; margin-top: 30px;">
      Comment Page
    </div>
  </header>

  <button @click="goBack" class="button-6" style="width: 50px; height: 50px; font-size: 90%; margin-top: 20px;">Back</button>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
