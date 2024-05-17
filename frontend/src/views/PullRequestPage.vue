<template>
  <header>
    <div style="font-size: 180%;">
      Pull Request Page
    </div>
  </header>
  <body>
    <div style="font-size: 100%; color: grey; margin-bottom: 20px;">
      This is the pull request information.
    </div>

    <div class="box-container">
      <div class="box">
        <button class="button-6" style="width: 100px; height: 100px; font-size: 250%;">23%</button>
        <div>Semantic Score</div>
      </div>
      <div class="box">
        <button class="button-6" style="width: 100px; height: 100px; font-size: 250%;">45</button>
        <div>Number of Pull Requests</div>
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
