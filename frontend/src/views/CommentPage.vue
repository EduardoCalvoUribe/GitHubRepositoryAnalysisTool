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
        for (let i=0; i < state.githubResponse.Repo.pull_requests.commits.length - 1; i++) {
          if (state.githubResponse.Repo.pull_requests[i].url == decodeURIComponent(route.params.url)) {
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

<template>
  <header>
    <RouterLink to="/repoinfo/${id}">Repository Infomation</RouterLink>
    <RouterLink style="margin-left: 2%" to="/prpage">Pull Requests</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commitpage">Commits</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commentpage">Comments</RouterLink>

  </header>

  <RouterView />
    <header>
      <div style="font-size: 180%;  margin-top: 30px;">
        Comment Page
      </div>
    </header>
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