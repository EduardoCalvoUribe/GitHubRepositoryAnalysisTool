<script>
import { ref, onMounted, computed } from 'vue';
import { fetchData } from '../fetchData.js'

export default {
  components: {
  },
  setup() {
    const repoInfo = ref(null);
    // const repoInfo = ref([ // Uses this by default, but is updated with fetched data from backend in onMounted.
    //     {
    //         "name": "repo1",
    //         "last_accessed": "2022-01-01",
    //         "id": "1"
    //     },
    //     {
    //         "name": "repo2",
    //         "last_accessed": "2022-01-02",
    //         "id": "2"
    //     },
    //     {
    //         "name": "repo3",
    //         "last_accessed": "2022-01-03",
    //         "id": "3"
    //     },
    //     {
    //         "name": "repo4",
    //         "last_accessed": "2022-01-04",
    //         "id": "4"
    //     },
    // ]);

    const selectedSort = ref({ name: 'Date Newest to Oldest' }); // sort option user selects from dropdown menu, default set to newest to oldest?
    const sorts = [ // different possible sort options
        { name: 'Date Oldest to Newest' },
        { name: 'Date Newest to Oldest' },
    ];

    onMounted(async () => {
      try {
        const info = await fetchData('http://127.0.0.1:8000/home'); // Insert correct endpoint here.
        if (info) {
          repoInfo.value = info; // Update repoInfo with the fetched backend db data.
        }
      } catch (error) {
        console.error('Error:', error)
      }
    });

    const sortListsDate = (list, choice) => {
      if (choice.name == 'Date Oldest to Newest') {
        // const sorted_list = list.sort((a,b) => new Date(a.updated_at) - new Date(b.updated_at));
        const sorted_list = Object.fromEntries(Object.entries(list).sort(([,a],[,b]) => a - b));
        console.log(sorted_list);
        return sorted_list;
      } else {
        // const sorted_list = list.sort((a,b) => new Date(b.updated_at) - new Date(a.updated_at));
        const sorted_list = Object.fromEntries(Object.entries(list).sort(([,a],[,b]) => b - a));
        return sorted_list;
      }
    };

    const sortedRepos = computed(() => {
      if (!repoInfo.value) return [];
      else return sortListsDate(repoInfo.value, selectedSort.value);
    });

    return { 
      repoInfo, // allows for repoInfo to be used in the template of this file
      sortedRepos,
      selectedSort,
      sorts
    }; 
  },
  data() {
    return {
      invalidInput: false, // set to false by default so false message is not displayed constantly
    }
  },
  methods: {
   
    async checkInput(str) {
      const regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+(?:\.git)?\/?$/; // regular expression that checks whether a string is a valid Github repo url
      return regex.test(str); // boolean true or false is returned
    },

    async handleGithubURLSubmit(inputUrl) {
      console.log('entered function');
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
          console.log('entered try');
          const response = await fetchData('http://127.0.0.1:8000/all/', postOptions); // send repo url to get github information function through 'all' path
          if (response) {
            console.log('reload')
            location.reload();
          }
      } catch (error) {
          console.error('Error:', error);
      }
      // window.location.reload();
      // this.$router.push({ path: this.$route.path })
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

    <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by" class="w-full md:w-14rem" />
        <label style="justify-content: center; display: inline-block; width: 250px; font-size: larger;" for="repos">Tracked Repositories:</label>
        <div id="repos" v-for="x in repoInfo" >
          <template v-for="repo in x" class="column">
          <router-link :to="{ path: '/repoinfo/' + encodeURIComponent(repo.url) }"><button class="button-6" > 
              <span><h2 style="margin-left: 0.3rem;">{{ repo.name }}</h2></span>
              <span class="last-accessed">Last Accessed: {{ repo.updated_at }}</span>
          </button></router-link>
          <button class="button-6" style="font-weight: 100; padding-inline: 1.1rem; width: 45px; margin-left: -8px; border-top-left-radius: 0; border-bottom-left-radius: 0;">
            <div style="margin-bottom: 3px; font-weight: 100" @click="handleDeleteRequest(repo.id)">x</div>
          </button>
          <br>  
        </template>
        </div> 
      </div>
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
