<script setup>
import RowBox from './components/RowBox.vue'

getFakeRequest();

async function getFakeRequest() {
  try {

    // Fake API fetch
    const response = await fetch('http://127.0.0.1:8000/github/user')  //'https://jsonplaceholder.typicode.com/posts/1'  //'127.0.0.1:8000/github/user'

    // takes response, converts to JavaScript Promise object
    const json = await response.json() 

    // Selects first div with 'fake_request' id attribute
    const fakeDiv = document.getElementById('fake_request');
    
    // Inserts content into that div in the specified format
    // For full JSON string, use: '<pre>' + JSON.stringify(json, null, 2) + '</pre>'
    fakeDiv.innerHTML = '<pre>' + JSON.stringify(json, null, 2) + '</pre>'
    // fakeDiv.innerHTML = '<p><h4>Fake Request Data:</h4><br>' + json.url + '</p>';

  } catch (error) {
    console.error('Error:', error)
  }   
}

async function sendGithubUrl(url) {

  //should be link of where the input should go(test with daniels function)
  const urlDestination = "http://example.com/api"; 

  //key-value pair convention
  const data = {url: 'api.github/users'};

  try {
      //make the post request that sends the data to its destination
      const response = await fetch(urlDestination, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      //see if operation was succesful by checking response status
      if (response.ok) { 
          console.log("GitHub URL sent successfully!");
      } else {
          console.error("Failed to send GitHub URL. Status code:", response.status);
      }
  } catch (error) {
      console.error("Error:", error);
  }
}

//const githubUrl = 'https://github.com/user/repo.git';
//sendGithubUrl(githubUrl);

</script>

<template>
  <header>
    <div>
      GitHub Analysis Tool (GAT)
    </div>
  </header>

  <main>
    <br><br>
    <div id="fake_request"></div>
    <br>
    <RowBox n_blocks=5 />
    <RowBox n_blocks=1 />
    <RowBox n_blocks=3 />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

</style>
