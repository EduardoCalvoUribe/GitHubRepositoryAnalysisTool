<template>
  <header>
    <div style="font-size: 180%;">
      Repository Information
    </div>
  </header>

  <header>
    <div style="font-size: 180%; justify-content: left;" >
      
    </div>
  </header>


  <div style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px;" for="datePicker" >Select date range:</label>
      <div id="datePicker" style="display: flex; align-items: flex-start;"> 
        <VueDatePicker v-model="selectedRange" range style="width: 500px; height: 50px;" ></VueDatePicker>
        <button class="button-6" style="width: 57px; height: 38px; margin-left: 3px; font-size: smaller;" @click="handleDateSubmit(selectedRange)" >Reload</button>
      </div>
    </div>
  </div> 

  <div class="grid-container">
    <div class="grid-item" v-for="item in items" :key="item.id">
      <router-link :to="item.path">{{ item.text }}</router-link>
    </div>
  </div>

  <div style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px; font-size: larger;" for="pullRequests" >Pull Requests:</label>
      <div id="pullRequests"class="row" v-for="pullrequest in pullRequestInfo">
        <router-link :to="{ path: '/prpage' }"><button class="button-6">
            <span><h2 style="margin-left: 0.3rem;">{{ pullrequest.title }}</h2></span>
            <span class="last-accessed">Author: {{ pullrequest.author }}</span>
        </button></router-link>
      </div> 
    </div>
  </div> 
</template>
  
<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, onMounted } from 'vue';
import { fetchData } from '../fetchData.js'

export default {
  components: {
    VueDatePicker
  },

  setup() {
    const pullRequestInfo = ref([
      {
          "title": "pull request 1",
          "author": "Bob"
      },
      {
          "title": "pull request 2",
          "author": "Janet"
      },
      {
          "title": "pull request 3",
          "author": "Alice"
      },
      {
          "title": "pull request 4",
          "author": "David"
      },
    ]);

    onMounted(async () => {

      const data = {'id': repoId};

      const postOptions = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };

      try {
          const response = await fetchData('http://127.0.0.1:8000/github/github-pulls/'.concat(inputUrl), postOptions);
          this.githubResponse = '<p><h5>Data from Backend:</h5><br>' + JSON.stringify(response) + '</p>';
      } catch (error) {
          console.error('Error:', error);
      }
    })

    return { pullRequestInfo };
  },

  data() {
    return {
      selectedRange: null,
      items: [
        { id: 1, text: 'Number of Pull Requests', path: '/prpage' },
        { id: 2, text: 'Number of Commits', path: '/commitpage' },
        { id: 3, text: 'Extra Repository Information' },
        // Add more items as needed
      ]
    }
  },

  methods: {
    async handleDateSubmit(range) {
      // update selected date range when input is given
      // this.selectedRange = range;
      console.log('entered function')

      const data = {'date': range};

      const postOptions = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };
      // send date range to backend through correct path that still needs to be created
      try {
        console.log('entered try')
        const response = await fetchData('', postOptions);
      } catch (error) {
          console.error('Error:', error);
      }
    },
  },
}
</script>
  
<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Adjust the number of columns as needed */
  gap: 10px; /* Spacing between grid items */
}

.grid-item {
  background-color: #157eff4d; /* Background color for grid items */
  padding: 50px; /* Padding inside grid items */
  text-align: center; /* Centering text inside grid items */
  border: 1px solid #ccc; /* Border for grid items */
}
</style>
  