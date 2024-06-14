<script>
import { ref, onMounted, computed } from 'vue';
import { fetchData } from '../fetchData.js';

export default {
  setup() {
    const repoInfo = ref(null);
    const selectedSort = ref({ name: 'Date Newest to Oldest' });
    const sorts = [
      { name: 'Date Oldest to Newest' },
      { name: 'Date Newest to Oldest' },
    ];

    onMounted(async () => {
      try {
        const info = await fetchData('http://127.0.0.1:8000/home');
        if (info) {
          repoInfo.value = info;
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });

    const sortListsDate = (list, choice) => {
      if (choice.name === 'Date Oldest to Newest') {
        return list.sort((a, b) => new Date(a.updated_at) - new Date(b.updated_at));
      } else {
        return list.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
      }
    };

    const sortedRepos = computed(() => {
      if (!repoInfo.value) return [];
      return sortListsDate(repoInfo.value.Repos, selectedSort.value);
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
      invalidInput: false,
      busy: false,
      inputUrl: '', // Added inputUrl to data to bind with v-model
    };
  },
  methods: {
    methods: {
  handleClick() {
    this.busy = true
    // Do something that takes some time
    setTimeout(() => { this.busy = false }, 2000) // Match this duration to the spinner's duration
  }
},

    async checkInput(str) {
      const regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-]+(?:\.git)?\/?$/;
      return regex.test(str);
    },

    async handleGithubURLSubmit(inputUrl) {
      console.log('entered function');
      this.invalidInput = false;

      if (!(await this.checkInput(inputUrl))) {
        this.invalidInput = true;
        return;
      }

      const data = { url: inputUrl };
      const postOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };

      try {
        console.log('entered try');
        this.busy = true; // Start the spinner
        const response = await fetchData('http://127.0.0.1:8000/all/', postOptions);
        if (response) {
          this.repoInfo = response;
          console.log('reload');
        }
        this.inputUrl = '';
      } catch (error) {
        console.error('Error:', error);
      } finally {
        this.busy = false; // Stop the spinner
      }
    },

    async handleDeleteRequest(repo) {
      const data = { url: repo };
      const postOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };

      try {
        const response = await fetchData('http://127.0.0.1:8000/delete/', postOptions);
        if (response) {
          this.repoInfo = response;
          console.log('reload');
        }
        console.log('delete reload');
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>

<template>
  <header>
    <div style="font-size: 180%; margin-top: 30px;">
      Repository Analysis Tool
    </div>
  </header>

  <main>
    <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <label style="display: inline-block; width: 250px;" for="urlTextfield">Enter GitHub URL:</label>
        <div style="display: flex; align-items: center;">
          <input id="urlTextfield" v-model="inputUrl" style="width: 500px; height: 50px;"></input>
          <button class="button-6" style="width: 57px; height: 50px; margin-left: 3px; font-size: smaller;"
            @click="handleGithubURLSubmit(inputUrl), handleClick"
            :disabled="busy">
            <div v-if="busy" class="lds-spinner">
              <div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div>
            </div>
            <div v-else>Submit</div>
          </button>
        </div>
      </div>
    </div>

    <div v-if="invalidInput" style="color: red; margin-top: 2%; display: flex; justify-content: center; margin-bottom: 5%">Invalid input! Please enter a valid GitHub URL.</div>

    <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
      <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <h2 style="justify-content: center; display: inline-block; width: 250px; margin-bottom: 3%" for="repos">Tracked Repositories:</h2>
        <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by" class="w-full md:w-14rem" />
        <div id="repos" class="row" v-for="repo in sortedRepos" :key="repo.id">
          <router-link :to="{ path: '/repoinfo/' + encodeURIComponent(repo.url) }">
            <button class="button-6">
              <span><h2 style="margin-left: 0.3rem;">{{ repo.name }}</h2></span>
              <span class="last-accessed">Last Accessed: {{ repo.updated_at }}</span>
            </button>
          </router-link>
          <button class="button-6" style="font-weight: 100; padding-inline: 1.1rem; width: 45px; margin-left: -8px; border-top-left-radius: 0; border-bottom-left-radius: 0;" @click="handleDeleteRequest(repo.id)">
            <div style="margin-bottom: 3px; font-weight: 100">x</div>
          </button>
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
