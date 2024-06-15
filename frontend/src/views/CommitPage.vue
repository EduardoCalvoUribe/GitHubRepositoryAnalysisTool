<script>
import { useRouter } from 'vue-router';

export default {
  name: "CommitPage",
  setup() {
    const router = useRouter();

    const goBack = () => {
      router.go(-1);
    };

    return {
      goBack,
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
  <div class="page-container">
    <!-- Header Information -->
    <header>
      <h1 style="font-size: 180%; margin-top: 30px;">Commit Page</h1>
    </header>

    <!-- Commit Information and Code Section -->
    <div style="margin-top: 20px;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <!-- Top Information Boxes -->
        <div style="display: flex; width: 100%;">
          <!-- Commit Message Box -->
          <div style="border: 2px solid blue; padding: 10px; flex-grow: 2; margin-right: 10px;">
            <p><strong>Commit message:</strong> "Initial commit with all base files."</p>
          </div>

          <!-- Semantic Score Box -->
          <div style="border: 2px solid blue; padding: 10px; flex-grow: 1; margin-right: 10px; text-align: center;">
            <p><strong>Semantic score:</strong> 0-1</p>
          </div>

          <!-- Timestamp Box -->
          <div style="border: 2px solid blue; padding: 10px; flex-grow: 1; text-align: center;">
            <p><strong>Time stamp of commit:</strong> Jan 1, 1:00 PM</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <button @click="goBack" class="button-6" style="width: 50px; height: 50px; font-size: 90%; margin-top: 20px;">Back</button>
</template>

<style scoped>
.page-container {
  width: 80%;
  margin: 0 auto;
}
</style>
