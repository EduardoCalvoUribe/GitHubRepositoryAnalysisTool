<template>
  <header>
    <RouterLink to="/repoinfo/${id}">Repository Information</RouterLink>
    <RouterLink style="margin-left: 2%" to="/prpage">Pull Requests</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commitpage">Commits</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commentpage">Comments</RouterLink>
  </header>

  <header>
    <div style="font-size: 180%; margin-top: 30px;">
      Repository Information
    </div>
  </header>

  <div style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px;" for="datePicker">Select date range:</label>
      <div id="datePicker" style="display: flex; align-items: flex-start;">
        <VueDatePicker v-model="selectedRange" range style="width: 500px; height: 50px;"></VueDatePicker>
        <button class="button-6" style="width: 57px; height: 38px; margin-left: 3px; font-size: smaller;" @click="handleDateSubmit(selectedRange)">Reload</button>
      </div>
    </div>
  </div>

  <div class="box-container">
    <div class="box" v-for="item in items" :key="item.id">
      <router-link :to="item.path">
        <button class="button-6" style="width: 150px; height: 100px; font-size: 100%;">{{item.text}}</button>
      </router-link>
    </div>
  </div>

  <div >
    <Dropdown v-model="selectedOption" :options="options" optionLabel="name" placeholder="Select an Option" class="w-full md:w-14rem" />
    <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by" class="w-full md:w-14rem" />
  </div>
  
  <div v-if="selectedOption && selectedOption.name === 'Pull Requests'" style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px; font-size: larger;" for="pullRequests">Pull Requests:</label>
      <div id="pullRequests" class="row" v-for="pullrequest in fakejson.repository.pull_requests">
        <router-link :to="{ path: '/prpage' }"><button class="button-6">
            <span><h2 style="margin-left: 0.3rem;">{{ pullrequest.id}}</h2></span>
            <span class="last-accessed">Author: {{ pullrequest.author }}</span>
            <span class="last-accessed">Semantic score: {{ pullrequest.author }}</span>
        </button></router-link>
      </div>
    </div>
  </div>

  <div v-else-if="selectedOption && selectedOption.name === 'Contributors'" style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px; font-size: larger;" for="users">Contributors:</label>
      <div id="users" class="row" v-for="user in fakejson.repository.contributors">
        <router-link :to="{ path: '/userpage' }"><button class="button-6">
            <span><h2 style="margin-left: 0.3rem;">{{ user }}</h2></span>
            <span class="last-accessed">Semantic score: {{ user }}</span>
        </button></router-link>
      </div>
    </div>
  </div>

  <div style="display: flex; justify-content: center; margin-top: 4%; height: 400px;">
    <BarChart :chartData="chartData" :chartOptions="chartOptions" />
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, onMounted } from 'vue';
import { fetchData } from '../fetchData.js'
import { useRoute } from 'vue-router';
import fakejson from '../test.json';
import BarChart from '../components/BarChart.vue';
import Dropdown from 'primevue/dropdown';
// import SelectButton from 'primevue/dropdown';

export default {
  components: {
    VueDatePicker, // datepicker component that lets user pick date range
    BarChart, // chart compoment that allows for displaying of charts
    Dropdown, // dropdown component which lets user selct option from dropdown menu
    // SelectButton,
  },

  setup() {
    const route = useRoute(); // allows for passage of variables from homepage to current page
    
    onMounted(async () => {
      const data = {'id': route.params.id}; // define data to be sent in postOptions, repo id in this case

      const postOptions = { // defines how data is sent to backend, POST request in this case
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };

      try {
          const response = await fetchData('http://127.0.0.1:8000/database/', postOptions); // send repo id to backend function through path 'database'
      } catch (error) {
          console.error('Error:', error);
      }
    })
  },

  data() {
    return {
      selectedOption: { name: 'Pull Requests'}, // view option user selects from dropdown menu, default set to pull requests
      options: [ // different possible view options
        { name: 'Pull Requests' },
        { name: 'Contributors' },
        // Add more options if needeed
      ],
      selectedSort: null, // sort option user selects from dropdown menu, default set to newest to oldest?
      sorts: [ // different possible sort options
        { name: 'Semantic Score Ascending' },
        { name: 'Semantic Score Descending' },
        { name: 'Date Oldest to Newest' },
        { name: 'Date Newest to Oldest' },
      ],
      fakejson, // temporary variable that loads in a fake json test file
      selectedRange: null, // date range that the user selects in date picker
      items: [ // items are the boxes with content being diplayed on the page§
        { id: 1, text: 'Number of Pull Requests: ' + fakejson.repository.number_of_pullrequests, path: '/prpage' },
        { id: 2, text: 'Number of Commits: ' + fakejson.repository.number_of_commits, path: '/commitpage' },
        { id: 3, text: 'Extra Repository Information' },
        // Add more items as needed
      ],
      chartData: { 
        labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
          {
            data: [0.4, 0.5, 0.5, 0.5, 0.2, 0.22, 0.2],
            backgroundColor: '#42A5F5'
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },

  methods: {
    async handleDateSubmit(range) {
      const data = {'date': range}; // define data to be sent in postOptions, date range in this case

      const postOptions = { // defines how data is sent to backend, POST request in this case
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };
     
      try {
        const response = await fetchData('', postOptions);  // send date range to backend through correct path that still needs to be created
      } catch (error) {
          console.error('Error:', error);
      }
    },

    async sortLists(items) {
      // TODO: implement sorting on relevant sorts
    }
  },
}
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.grid-item {
  background-color: #157eff4d;
  padding: 50px;
  text-align: center;
  border: 1px solid #ccc;
}

.box-container {
  display: flex;
  gap: 10px;
  justify-content: center;
  padding: 20px 0;
  text-align: center;
}

.box {
  flex: 1;
  padding: 20px;
  background-color: rgb(255, 255, 255);
  text-align: center;
  border: 1px solid #ffffff;
}
</style>