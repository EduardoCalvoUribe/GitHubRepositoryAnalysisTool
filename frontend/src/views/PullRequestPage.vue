<script>
import testJson from '../test.json';

export default {
  data() {
    return {
      repositoryId: testJson.repository.id,
      number_of_pullrequests: testJson.repository.number_of_pullrequests,
      number_of_commits: testJson.repository.number_of_commits
    };
          }
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
      Pull Request Page
    </div>
  </header>
  <body>
    <div style="font-size: 100%; color: grey; margin-bottom: 20px;">
      This is the pull request information.
    </div>

   
  </body>
</template>

<style scoped>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
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
