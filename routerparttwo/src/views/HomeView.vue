<script>
import { ref, onMounted } from 'vue';
import { fetchData } from '../fetchData.js'

export default {
  components: {
  },
  setup() {
    const repoInfo = ref([
        {
            "name": "repo1",
            "last_accessed": "2022-01-01"
        },
        {
            "name": "repo2",
            "last_accessed": "2022-01-02"
        },
        {
            "name": "repo3",
            "last_accessed": "2022-01-03"
        },
        {
            "name": "repo4",
            "last_accessed": "2022-01-04"
        },
    ]);

    onMounted(async () => {
      try {
        // Fetches json data from specified URL using our fetchData function (will be our backend endpoints)
        // const json_response = await fetchData('http://127.0.0.1:8000/github/user');
        // const fake_response = await fetchData('http://jsonplaceholder.typicode.com/posts/1');

        // Selects first div with specified id (such as 'github_request')
        // const fakeDiv = document.getElementById('fake_request');

        // Inserts content of json into that div in whatever specified format
        // fakeDiv.innerHTML = '<pre>' + JSON.stringify(fake_response, null, 2) + '</pre>';
        

        // this.tableContent = '<p>Test content for tableContent</p>';
        // this.githubResponse = '<p>Test content for githubResponse</p>';
        // getTrackedRepositories();
      } catch (error) {
        console.error('Error:', error)
      }

      // const githubURL = ref('');

      // return { githubURL };

    });

    return { repoInfo };
  },
  // TODO: Fix githubURL, it's just empty. Input is not correctly retrieved from Input Box.
  data() {
    return {
      githubURL: '',
      tableContent: '',
      githubResponse: '',
      invalidInput: false
    }
  },
  methods: {

    async checkInput(str) {
      const regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+(?:\.git)?\/?$/;
      return regex.test(str);
    },

    async handleGithubURLSubmit(inputUrl) {
      //var githubURL = document.getElementById('githubURL').value;
      this.invalidInput = false;
      if (!(await this.checkInput(inputUrl))) {
        console.log('Not a github repository and githubURL value is: ', inputUrl)
        this.invalidInput = true;
        return;
      }

      console.log('handleGithubURLSubmit called and url given as valid', inputUrl) 

      const data = {'url': inputUrl};

      const postOptions = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };

      try {
          // https://github.com/IntersectMBO/plutus
          // TODO: Instead of cocatenating, extract from POST options (postOptions.body?). Also modify urls.py for this
          const response = await fetchData('http://127.0.0.1:8000/github/github-pulls/'.concat(inputUrl), postOptions);
          // const response = await fetch(url, postOptions);
          // const json = await response.json();
          this.githubResponse = '<p><h5>Data from Backend:</h5><br>' + JSON.stringify(response) + '</p>';

      } catch (error) {
          console.error('Error:', error);
      }
    },
  }
};
</script>


<template>
  <header>
    <div style="font-size: 180%;">
      Repository Analysis Tool
    </div>
  </header>

  <main>
    <div style="margin-top: 4%; display: flex; justify-content: center;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <label style="display: inline-block; width: 250px;" for="urlTextfield" >Enter GitHub URL:</label>
        <div style="display: flex; align-items: center;">
          <input id="urlTextfield" v-model="inputUrl" style="width: 500px; height: 50px;"></input>
          <button style="height: 50px; margin-left: 20px;" @click="handleGithubURLSubmit(inputUrl)" >Submit</button>
        </div>  
      </div>
    </div> 

    <div v-if="invalidInput" style="color: red; margin-top: 2%; display: flex; justify-content: center;">Invalid input! Please enter a valid GitHub URL.</div>

    <!-- id="github_request" -->
    <div style="margin-top: 10%;" v-html="githubResponse" ></div> 


    <!-- <br><br>
    <h5>Fake Request:</h5>
    <div id="fake_request"></div>
    <br><br> -->

    <div style="width: 100%; align-items: center; justify-content: center; vertical-align: center; margin-bottom: 4px" v-for="repo in repoInfo">
      <router-link :to="{ path: '/repoinfo' }"><button class="button-6" style="width: 50%;">
          <span><h2 style="margin-left: 0.3rem;">{{ repo.name }}</h2></span>
          <span class="last-accessed">Last Accessed: {{ repo.last_accessed }}</span>
      </button></router-link>
      <button class="button-6" style="margin-left: -3px; font-weight: 100; flex-grow: 0; padding-inline: 0.7rem">X</button>
    </div> 

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

