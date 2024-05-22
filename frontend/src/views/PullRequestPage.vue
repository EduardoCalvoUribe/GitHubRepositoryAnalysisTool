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

    <div class="box-container">
      <div class="box">
        <button class="button-6" style="width: 100px; height: 100px; font-size: 250%;">{{number_of_pullrequests}}</button>
        <div>Number of Pull Requests</div>
      </div>
      <div class="box">
        <button class="button-6" style="width: 100px; height: 100px; font-size: 250%;">{{ number_of_commits }}</button>
        <div>Number of Commits</div>
      </div>
      <div class="box">
        <button class="button-6" style="width: 100px; height: 100px; font-size: 250%;">3</button>
        <div>Commits per Pull Request</div>
      </div>
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
