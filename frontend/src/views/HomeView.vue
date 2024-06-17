<script>
import { ref, onMounted, computed } from 'vue';
import { fetchData } from '../fetchData.js';

export default {
  setup() {
    /**
     * @constant {Ref} repoInfo - A reactive reference holding repository information fetched from the backend.
     */
    const repoInfo = ref(null);
    
    /**
     * @constant {Ref} selectedSort - A reactive reference holding the currently selected sort option.
     * @default { name: 'Date Newest to Oldest' }
     */
    const selectedSort = ref({ name: 'Date Newest to Oldest' });

    /**
     * @constant {Array} sorts - An array of objects representing different sorting options.
     */
    const sorts = [
      { name: 'Date Oldest to Newest' },
      { name: 'Date Newest to Oldest' },
      { name: 'Semantic Score Ascending' },
      { name: 'Semantic Score Descending' },
    ];

    /**
     * Fetch repository data from the backend when the component is mounted.
     * @async
     * @function onMounted
     */
    onMounted(async () => {
      // Make request to backend for all repositories in the database.
      try {
        const info = await fetchData('http://127.0.0.1:8000/home');
        if (info) {
          repoInfo.value = info; // Fill repoInfo with response from backend.
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });

    /**
     * Sorts a list of repositories by date.
     * @function sortListsDate
     * @param {Array} list - The list of repositories to sort.
     * @param {Object} choice - The selected sort option.
     * @returns {Array} The sorted list of repositories.
     */
    const sortListsDate = (list, choice) => {
      // Check if ascending or descending is selected.
      if (choice.name === 'Date Oldest to Newest') {
        return list.sort((a, b) => new Date(a.updated_at) - new Date(b.updated_at));
      } else {
        return list.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
      }
    };

    /**
     * Sorts a list of repositories by semantic score.
     * @function sortListsScore
     * @param {Array} list - The list of repositories to sort.
     * @param {Object} choice - The selected sort option.
     * @returns {Array} The sorted list of repositories.
     */
    const sortListsScore = (list, choice) => {
      // Check if ascending or descending is selected.
      if (choice.name == 'Semantic Score Ascending') {
        return list.sort((a, b) => (a.average_semantic) - (b.average_semantic));
      } else {
        return list.sort((a, b) => (b.average_semantic) - (a.average_semantic));
      }
    };

    /**
     * Computed property to get the sorted list of repositories based on the selected sort option.
     * @constant {ComputedRef} sortedRepos
     * @returns {Array} The sorted list of repositories.
     */
    const sortedRepos = computed(() => {
      // Check if repoInfo has value.
      if (!repoInfo.value) return [];
      // Check which type of sort is selected
      else if (selectedSort.value.name.includes('Date')) {
        return sortListsDate(repoInfo.value.Repos, selectedSort.value);
      } else return sortListsScore(repoInfo.value.Repos, selectedSort.value);
    });

    return {
      repoInfo,
      sortedRepos,
      selectedSort,
      sorts,
    };
  },

  data() {
    return {
      /**
       * @property {boolean} invalidInput - A flag indicating whether the input URL is invalid.
       * @default false
       */
      invalidInput: false,

      /**
       * @property {boolean} busy - A flag indicating whether a process is currently running.
       * @default false
       */
      busy: false,

      /**
       * @property {string} inputUrl - The input URL entered by the user.
       * @default ''
       */
      inputUrl: '',
    };
  },

  methods: {
    /**
     * Simulates a process that takes some time.
     * @method handleClick
     */
    handleClick() {
      // Set busy to true.
      this.busy = true;
      // Take some time.
      setTimeout(() => { this.busy = false }, 2000);
    },

    /**
     * Validates the GitHub URL using a regular expression.
     * @async
     * @method checkInput
     * @param {string} str - The input URL to validate.
     * @returns {boolean} Whether the input URL is valid.
     */
    async checkInput(str) {
      // The specific regular expression checks if str is actual Github repository URL.
      const regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+(?:\.git)?\/?$/;
      return regex.test(str);
    },

    /**
     * Handles the submission of the GitHub URL.
     * @async
     * @method handleGithubURLSubmit
     * @param {string} inputUrl - The GitHub URL entered by the user.
     */
    async handleGithubURLSubmit(inputUrl) {
      // Set invalidInput to false.
      this.invalidInput = false;

      // Validate the input URL
      if (!(await this.checkInput(inputUrl))) {
        this.invalidInput = true;
        return;
      }
      // Define data to be sent to backend in POST request.
      const data = { url: inputUrl };
      // Define way of sending data to backend.
      const postOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };

      try {
        // Start the spinner.
        this.busy = true; 
        // Receive response from backend.
        const response = await fetchData('http://127.0.0.1:8000/all/', postOptions);
        if (response) {
          this.repoInfo = response;
        }
        // Set inputUrl back to empty string.
        this.inputUrl = '';
      } catch (error) {
        console.error('Error:', error);
      } finally {
        // Stop the spinner.
        this.busy = false; 
      }
    },

    /**
     * Handles the deletion of a repository.
     * @async
     * @method handleDeleteRequest
     * @param {Object} repo - The repository to delete.
     */
    async handleDeleteRequest(repo) {
      // Define data to be sent to backend in POST request.
      const data = { url: repo };
      // Define way of sending data to backend.
      const postOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };

      try {
        // Receive response from backend.
        const response = await fetchData('http://127.0.0.1:8000/delete/', postOptions);
        if (response) {
          this.repoInfo = response;
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>

<template>
  <!-- Header for the page -->
  <header>
    <div style="font-size: 180%; margin-top: 30px;">
      Repository Analysis Tool
    </div>
  </header>

  <main>
    <!-- URL input and submit button -->
    <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <label style="display: inline-block; width: 250px;" for="urlTextfield">Enter GitHub URL:</label>
        <div style="display: flex; align-items: center;">
          <input id="urlTextfield" v-model="inputUrl" style="width: 500px; height: 50px;"></input>
          <button class="button-6" style="width: 57px; height: 50px; margin-left: 3px; font-size: smaller;"
            @click="handleGithubURLSubmit(inputUrl), handleClick" :disabled="busy">
            <div v-if="busy" class="lds-spinner" style="align-items: center;">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
            <div v-else>Submit</div>
          </button>
        </div>
      </div>
    </div>

    <!-- Error message for invalid input -->
    <div v-if="invalidInput"
      style="color: red; margin-top: 2%; display: flex; justify-content: center; margin-bottom: 5%">Invalid input!
      Please enter a valid GitHub URL.</div>

    <!-- Repository list with sorting dropdown menu -->
    <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <h2 style="justify-content: center; display: inline-block; width: 250px; margin-bottom: 3%" for="repos">Tracked
          Repositories:</h2>
        <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by"
          class="w-full md:w-14rem" />
        <div id="repos" class="row" v-for="repo in sortedRepos">
          <router-link :to="{ path: '/repoinfo/' + encodeURIComponent(repo.url) + '/current' }"><button
              class="button-6">
              <span>
                <h2 style="margin-left: 0.3rem;">{{ repo.name }}</h2>
              </span>
              <span class="last-accessed">Semantic score: {{ repo.average_semantic.toFixed(2) }}</span>
              <span class="last-accessed">Last Accessed: {{ repo.updated_at }}</span>
            </button>
          </router-link>
          <button class="button-6"
            style="font-weight: 100; padding-inline: 1.1rem; width: 45px; margin-left: -8px; border-top-left-radius: 0; border-bottom-left-radius: 0;"
            @click="handleDeleteRequest(repo.id)">
            <div style="margin-bottom: 3px; font-weight: 100">x</div>
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/**
 * Styling for the header.
 */
header {
  line-height: 1.5;
}

/**
 * Styling for the loading spinner.
 */
.lds-spinner,
.lds-spinner div,
.lds-spinner div:after {
  box-sizing: border-box;
}

.lds-spinner {
  color: currentColor;
  display: inline-block;
  position: relative;
  width: 30px;
  height: 30px;
}

.lds-spinner div {
  transform-origin: 15px 15px;
  animation: lds-spinner 1.2s linear infinite;
}

.lds-spinner div:after {
  content: " ";
  display: block;
  position: absolute;
  top: 3.2px;
  left: 13.8px;
  width: 2.4px;
  height: 7.6px;
  border-radius: 20%;
  background: currentColor;
}

.lds-spinner div:nth-child(1) {
  transform: rotate(0deg);
  animation-delay: -1.1s;
}

.lds-spinner div:nth-child(2) {
  transform: rotate(30deg);
  animation-delay: -1s;
}

.lds-spinner div:nth-child(3) {
  transform: rotate(60deg);
  animation-delay: -0.9s;
}

.lds-spinner div:nth-child(4) {
  transform: rotate(90deg);
  animation-delay: -0.8s;
}

.lds-spinner div:nth-child(5) {
  transform: rotate(120deg);
  animation-delay: -0.7s;
}

.lds-spinner div:nth-child(6) {
  transform: rotate(150deg);
  animation-delay: -0.6s;
}

.lds-spinner div:nth-child(7) {
  transform: rotate(180deg);
  animation-delay: -0.5s;
}

.lds-spinner div:nth-child(8) {
  transform: rotate(210deg);
  animation-delay: -0.4s;
}

.lds-spinner div:nth-child(9) {
  transform: rotate(240deg);
  animation-delay: -0.3s;
}

.lds-spinner div:nth-child(10) {
  transform: rotate(270deg);
  animation-delay: -0.2s;
}

.lds-spinner div:nth-child(11) {
  transform: rotate(300deg);
  animation-delay: -0.1s;
}

.lds-spinner div:nth-child(12) {
  transform: rotate(330deg);
  animation-delay: 0s;
}

@keyframes lds-spinner {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}
</style>
