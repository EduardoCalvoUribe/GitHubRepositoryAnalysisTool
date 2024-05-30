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
            "last_accessed": "2022-01-01",
            "id": "1"
        },
        {
            "name": "repo2",
            "last_accessed": "2022-01-02",
            "id": "2"
        },
        {
            "name": "repo3",
            "last_accessed": "2022-01-03",
            "id": "3"
        },
        {
            "name": "repo4",
            "last_accessed": "2022-01-04",
            "id": "4"
        },
    ]);

    onMounted(async () => {
      try {
        const info = await fetchData(''); // Insert correct endpoint here.
        if (info) {
          repoInfo.value = info; // Update repoInfo with the fetched backend db data.
        }
      } catch (error) {
        console.error('Error:', error)
      }
    });

    return { repoInfo }; // allows for repoInfo to be used in the template of this file
  },
  data() {
    return {
      invalidInput: false, // set to false by default so false message is not displayed constantly
      selectedSort: null, // sort option user selects from dropdown menu, default set to newest to oldest?
      sorts: [ // different possible sort options
        { name: 'Date Oldest to Newest' },
        { name: 'Date Newest to Oldest' },
      ],
    }
  },
  methods: {
   
    async checkInput(str) {
      const regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+(?:\.git)?\/?$/; // regular expression that checks whether a string is a valid Github repo url
      return regex.test(str); // boolean true or false is returned
    },

    async handleGithubURLSubmit(inputUrl) {
      this.invalidInput = false; // sets variable invalidInput to false so that false message is not displayed
      if (!(await this.checkInput(inputUrl))) { // checks if input url from user is valid Github repo url
        this.invalidInput = true; // if input is not valid invalidInput is set to false so false message can be displayed
        return;
      }

      const data = {'url': inputUrl}; // define data to be sent in postOptions, repo url in this case

      const postOptions = { // defines how data is sent to backend, POST request in this case
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };

      try {
          const response = await fetchData('http://127.0.0.1:8000/all/', postOptions); // send repo url to get github information function through 'all' path
      } catch (error) {
          console.error('Error:', error);
      }
    },

    async handleDeleteRequest(repo) {
      const data = {'url': repo}; // define data to be sent in postOptions, repo id in this case

      const postOptions = { // defines how data is sent to backend, POST request in this case
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };
      
      try {
          const response = await fetchData('http://127.0.0.1:8000/delete/', postOptions); // send repo name to backend delete function through path 'delete'
      } catch (error) {
          console.error('Error:', error);
      }
    },
  }
};
</script>

<template>
  <header>
    <div style="font-size: 180%;  margin-top: 30px;">
      Repository Analysis Tool
    </div>
  </header>

  <main>
    <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <label style="display: inline-block; width: 250px;" for="urlTextfield" >Enter GitHub URL:</label>
        <div style="display: flex; align-items: center;">
          <input id="urlTextfield" v-model="inputUrl" style="width: 500px; height: 50px;"></input>
          <button class="button-6" style="width: 57px; height: 50px; margin-left: 3px; font-size: smaller;" @click="handleGithubURLSubmit(inputUrl)" >Submit</button>
        </div>  
      </div>
    </div> 

    <div v-if="invalidInput" style="color: red; margin-top: 2%; display: flex; justify-content: center; margin-bottom: 5%">Invalid input! Please enter a valid GitHub URL.</div>

    <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by" class="w-full md:w-14rem" />

    <div class="row" v-for="repo in repoInfo">
      <router-link :to="{ path: '/repoinfo/' + repo.id }"><button class="button-6" > 
          <span><h2 style="margin-left: 0.3rem;">{{ repo.name }}</h2></span>
          <span class="last-accessed">Last Accessed: {{ repo.last_accessed }}</span>
      </button></router-link>
      <button class="button-6" style="font-weight: 100; padding-inline: 1.1rem; width: 45px; margin-left: -8px; border-top-left-radius: 0; border-bottom-left-radius: 0;">
        <div style="margin-bottom: 3px; font-weight: 100" @click="handleDeleteRequest(repo.id)">x</div>
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