<script>
import { ref, onMounted } from 'vue';
import { fetchData } from '../fetchData.js'

export default {
  components: {
  },
  setup() {
    const repoInfo = ref([ // Uses this by default, but is updated with fetched data from backend in onMounted.
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
        const info = await fetchData(''); // Insert correct endpoint here.
        repoInfo.value = info; // Update repoInfo with the fetched backend db data.
      } catch (error) {
        console.error('Error:', error)
      }
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

    async handleDeleteRequest(repo) {
      //checking for correct repo name in console
      console.log(repo)

      const data = {'name': repo};

      const postOptions = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };
      // send repo name to backend through correct path that still needs to be created
      try {
        console.log('entered try')
        const response = await fetchData('', postOptions);
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
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
    <div style="margin-top: 8%;" v-html="githubResponse" ></div> 


    <div class="row" v-for="repo in repoInfo">
      <router-link :to="{ path: '/repoinfo' }"><button class="button-6">
          <span><h2 style="margin-left: 0.3rem;">{{ repo.name }}</h2></span>
          <span class="last-accessed">Last Accessed: {{ repo.last_accessed }}</span>
      </button></router-link>
      <button class="button-6" style="font-weight: 100; padding-inline: 1.1rem; width: 45px; margin-left: -8px; border-top-left-radius: 0; border-bottom-left-radius: 0;">
        <div style="margin-bottom: 3px; font-weight: 100" @click="handleDeleteRequest(repo.name)">x</div><!-- <i class="fa fa-times" style="font-size: 30px; "></i> -->
      </button>
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

