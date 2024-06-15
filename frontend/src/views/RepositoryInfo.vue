<script>
import { ref, onMounted, computed, watchEffect } from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { fetchData } from '../fetchData.js'
import { useRoute } from 'vue-router';
import { state } from '../repoPackage.js';
import fakejson from '../test.json';
import Chart from '../components/Chart.vue';
import Dropdown from 'primevue/dropdown';
import CheckBoxList from '../components/CheckBoxList.vue';
// import SelectButton from 'primevue/dropdown';

export default {
  components: {
    VueDatePicker, // datepicker component that lets user pick date range
    Chart, // chart compoment that allows for displaying of charts
    Dropdown, // dropdown component which lets user selct option from dropdown menu
    CheckBoxList // checkbox component that allows selection of users
  },

  setup() {
    const route = useRoute();
    const selectedUsers = ref([]); // list of users that user selects from checkbox list
    const selectedSort = ref({ name: 'Date Newest to Oldest' }); // sort option user selects from dropdown menu, default set to newest to oldest?
    const sorts = ref([ // different possible sort options
        // { name: 'Semantic Score Ascending' },
        // { name: 'Semantic Score Descending' },
        { name: 'Date Oldest to Newest' },
        { name: 'Date Newest to Oldest' },
      ]);
    const isZoomedIn = ref(false); // boolean to check if user is in day view or month view

    const getPackage = async (date) => {
      const data = {
        'url': decodeURIComponent(route.params.url),
        'date': date
      }; // define data to be sent in postOptions, repo url in this case
      // console.log(data, "url?");
      // console.log(route)
      
      const postOptions = { // defines how data is sent to backend, POST request in this case
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };
      // console.log("in")
      try {      
          const response = await fetchData('http://127.0.0.1:8000/package', postOptions); // send repo id to backend function through path 'database'
          // console.log("received")
          state.githubResponse = response;
          console.log(state.githubResponse);
      } catch (error) {
          console.error('Error:', error);
      }
    }

    const sortListsDate = (list, choice) => {
      if (choice.name == 'Date Oldest to Newest') {
        const sorted_list = list.sort((a,b) => new Date(a.date) - new Date(b.date));
        console.log(list);
        return sorted_list;
      } else {
        const sorted_list = list.sort((a,b) => new Date(b.date) - new Date(a.date));
        console.log(list);
        return sorted_list;
      }
    };

    const sortListsScore = (list, choice) => {
      if (choice.name == 'Semantic Score Ascending') {
        const sorted_list = list.sort((a,b) => new Date(a.date) - new Date(b.date));
        return sorted_list;
      } else {
        const sorted_list = list.sort((a,b) => new Date(b.date) - new Date(a.date));
        return sorted_list;
      }
    };

    const sortedPullRequests = computed(() => {
      if (!state.githubResponse) return [];
      else if (selectedSort.value.name.includes('Date')) {
        return sortListsDate(state.githubResponse.Repo.pull_requests, selectedSort.value);
      } else {
        return sortListsScore(state.githubResponse.Repo.pull_requests, selectedSort.value);
      }
    });

    const pullRequestCount = computed(() => {
      return sortedPullRequests.value.length;
    });

    const formattedDate = computed(() => {
      if (!state.githubResponse || !state.githubResponse.Repo.updated_at) {
        return 'Loading...';
      }
      const date = new Date(state.githubResponse.Repo.updated_at);
      const formatter = new Intl.DateTimeFormat('en-GB', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
      });
      return formatter.format(date);
    });

    
    const userList = computed(() => { // List of contributors is extracted from the pull requests
      if (!state.githubResponse || !state.githubResponse.Repo.pull_requests) {
        return [];  // Return an empty array if there are no pull requests
      }
      
      const users = new Set();
      state.githubResponse.Repo.pull_requests.forEach(pr => {
        users.add(pr.user); // Add each user
      });

      return Array.from(users);  // Convert Set back to Array
    });

    const handleSelectedUsers = (selected) => { // Function to handle selected users from checkbox list
      selectedUsers.value = selected;
      console.log("Selected users:", selectedUsers.value);
      // You can now use selectedUsers to filter or display specific data
    };

    const chartOptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: 'Test',
          font: {
            size: 20
          }
        }
      }
    });

    const pullRequestsRange = computed(() => {
      let minDate = new Date();
      let maxDate = new Date(0);
      const counts = {};
      
      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        state.githubResponse.Repo.pull_requests.forEach(pr => {
          const date = new Date(pr.date); 
          minDate = date < minDate ? date : minDate;
          maxDate = date > maxDate ? date : maxDate;
          const monthKey = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0');
          counts[monthKey] = counts[monthKey] ? counts[monthKey] + 1 : 1;
        });
      }

      // Generate all months between minDate and maxDate
      const labels = [];
      const data = [];
      for (let d = new Date(minDate); d <= maxDate; d.setMonth(d.getMonth() + 1)) {
        const key = d.getFullYear() + '-' + (d.getMonth() + 1).toString().padStart(2, '0');
        labels.push(key);
        data.push(counts[key] || 0);
      }

      return { labels, data };
    });

    const handleBarClick = (label) => {
      console.log(`Clicked on bar: ${label}`);

      // Extract year and month from the label
      const [year, month] = label['label'].split('-').map(Number);

      // Filter the pull requests for the selected month
      const selectedMonthData = state.githubResponse.Repo.pull_requests.filter(pr => {
        const date = new Date(pr.date);
        return date.getFullYear() === year && date.getMonth() + 1 === month;
      });

      // Group the pull requests by day
      const counts = {};
      selectedMonthData.forEach(pr => {
        const date = new Date(pr.date);
        const day = date.getDate();
        counts[day] = (counts[day] || 0) + 1;
      });

      // Generate labels for each day of the month
      const daysInMonth = new Date(year, month, 0).getDate(); // Get the number of days in the month
      const labels = [];
      const data = [];
      for (let day = 1; day <= daysInMonth; day++) {
        labels.push(`${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`);
        data.push(counts[day] || 0); // Push count or 0 if no pull requests on that day
      }

      chartData.value = {
        labels,
        datasets: [{
          data,
          backgroundColor: '#42A5F5'
        }]
      };

      isZoomedIn.value = true;
    };

    const resetChartView = () => {
      chartData.value = {
        labels: pullRequestsRange.value.labels,
        datasets: [{
          data: pullRequestsRange.value.data,
          backgroundColor: '#42A5F5'
        }]
      };

      isZoomedIn.value = false;
    };

    const chartData = ref({
      labels: pullRequestsRange.value.labels,
      datasets: [{
        data: pullRequestsRange.value.data,
        backgroundColor: '#42A5F5'
      }]
    });

    watchEffect(() => {
      chartData.value = {
        labels: pullRequestsRange.value.labels,
        datasets: [{
          data: pullRequestsRange.value.data,
          backgroundColor: '#42A5F5'
        }]
      };
    });

    onMounted(async () => {
      await getPackage('');
    });

    
    return {
      getPackage,
      state,
      sortedPullRequests,
      selectedSort,
      sorts,
      route,
      pullRequestCount,
      formattedDate,
      userList,
      selectedUsers,
      handleSelectedUsers,
      chartOptions,
      chartData,
      handleBarClick,
      resetChartView,
      isZoomedIn,
    }
  },

  data() {
    // console.log(githubResponse.value)
    return {
      // githubResponse: null,
      selectedOption: { name: 'Pull Requests'}, // view option user selects from dropdown menu, default set to pull requests
      options: [ // different possible view options
        { name: 'Pull Requests' },
        { name: 'Contributors' },
        // Add more options if needeed
      ],
      selectedRange: null, // date range that the user selects in date picker
      items: [ // items are the boxes with content being diplayed on the page§
        { id: 1, text: 'Number of Pull Requests: ' + fakejson.repository.number_of_commits, path: '/prpage' },
        { id: 2, text: 'Number of Commits: ' + fakejson.repository.number_of_commits, path: '/commitpage' },
        { id: 3, text: 'Extra Repository Information' },
        // Add more items as needed
      ],
      
    }
  },
}
</script>

<template>
  <!-- <header>
    <RouterLink to="/repoinfo/${url}">Repository Information</RouterLink>
    <RouterLink style="margin-left: 2%" to="/prpage">Pull Requests</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commitpage">Commits</RouterLink>
    <RouterLink style="margin-left: 2%" to="/commentpage">Comments</RouterLink>
  </header> -->

  <header>
    <div v-if="state.githubResponse" style="margin-top: 50px">
      <div style="font-size: 240%; margin-bottom: 20px;"> {{ state.githubResponse.Repo.name }} </div>
      <a :href="state.githubResponse.Repo.url" target="_blank" style="margin-bottom: 5px"> URL: {{ state.githubResponse.Repo.url }} </a>
      <div style="font-size: 90%; margin-left: 3px; margin-top: 6px;"> Last Updated: {{ formattedDate }} </div>
    </div>  
  </header>

  <!-- DATE PICKER -->
  <div style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px;" for="datePicker">Select date range:</label>
      <div id="datePicker" style="display: flex; align-items: flex-start;">
        <VueDatePicker v-model="selectedRange" range style="width: 300px; height: 50px;"></VueDatePicker>
        <button class="button-6" style="width: 57px; height: 38px; margin-left: 3px; font-size: smaller;" @click="getPackage(selectedRange)">Reload</button>
      </div>
    </div>
  </div>

  <!-- GRAPH -->
  <div style="display: flex; justify-content: space-evenly; margin-top: 4%; height: 500px; max-width: 100%;">
    
    <div style="margin-right: 10px; margin-top: 70px; min-width: 160px; position: relative">
      <div>
        <input type="radio" id="semantic" name="stat" value="semantic">
        <label style="margin-left: 5px;" for="semantic">Semantic Score</label>
      </div>
      <div>
        <input type="radio" id="engagement" name="stat" value="engagement">
        <label style="margin-left: 5px;" for="engagement">Engagement Score</label>
      </div>
      <div>
        <input type="radio" id="commits" name="stat" value="commits">
        <label style="margin-left: 5px;" for="commits">Commits</label>
      </div>
      <div>   
        <input type="radio" id="pullrequests" name="stat" value="pullrequests" checked>
        <label style="margin-left: 5px;" for="pullrequests">Pull Requests</label>
      </div>
      <button class="button-6" v-if="isZoomedIn" @click="resetChartView" style="position: absolute; bottom: 10px; right: 10px; margin-top: 20px; width: 40px; height: 40px; justify-content: center; vertical-align: center; font-size: larger;"><</button>
    </div>

    <Chart style="flex: 1; max-width: 1000px" 
      @bar-click="handleBarClick" 
      :chartData="chartData" 
      :chartOptions="chartOptions" 
      :isBar="true"
    />

    <div style="margin-left: 40px; margin-top: 50px;">
      <CheckBoxList :usernames="userList" @update:selected="handleSelectedUsers"/>
    </div>
    
  </div>

  <!-- PULL REQUESTS and CONTRIBUTORS -->
  <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <div style="margin-bottom: 25px;">
        <Dropdown v-model="selectedOption" :options="options" optionLabel="name" placeholder="Select an Option" class="w-full md:w-14rem" style="margin-right: 10px;" />
        <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by" class="w-full md:w-14rem" />
      </div>
      <div v-if="selectedOption && selectedOption.name === 'Pull Requests' && state.githubResponse" style=" display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <h1 style="justify-content: center; display: inline-block; width: 250px;" for="pullRequests">Pull Requests</h1>
          <div style="margin-top: 10px; justify-content: center;">
            Total Pull Requests: {{ pullRequestCount }}
          </div>
          <div id="pullRequests" class="row" v-for="pullrequest in sortedPullRequests">
            <router-link :to="{ path: '/prpage/' + encodeURIComponent(pullrequest.url) }"><button class="button-6">
                <span><h2 style="margin-left: 0.3rem;">{{ pullrequest.title}}</h2></span>
                <span class="last-accessed">Author: {{ pullrequest.user }}</span>
                <span class="last-accessed">Date {{ pullrequest.date }}</span>
            </button></router-link>
          </div>
        </div>
      </div>
      <div v-else-if="selectedOption && selectedOption.name === 'Contributors' && state.githubResponse" style=" display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <h1 style="justify-content: center; display: inline-block; width: 250px;" for="users">Contributors</h1>
          <div id="users" class="row" v-for="user in userList">
            <router-link :to="{ path: '/userpage' }"><button class="button-6">
                <span><h2 style="margin-left: 0.3rem;">{{ user }}</h2></span>
                <!-- <span class="last-accessed">Semantic score: {{ user }}</span> -->
            </button></router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- BACK BUTTON -->
  <router-link :to="{path: '/' }">
        <button class="button-6" style="width: 50px; height: 50px; font-size: 90%;">Back</button>
    </router-link>
</template>

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
