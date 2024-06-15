<script>
import { ref, onMounted, computed, watchEffect } from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import { fetchData } from '../fetchData.js';
import { useRoute } from 'vue-router';
import { state } from '../repoPackage.js';
import Chart from '../components/Chart.vue';
import Dropdown from 'primevue/dropdown';
import CheckBoxList from '../components/CheckBoxList.vue';

export default {
  components: {
    VueDatePicker,
    Chart,
    Dropdown,
    CheckBoxList,
  },

  setup() {
    const route = useRoute();
    const selectedUsers = ref([]);
    const selectedSort = ref({ name: 'Date Newest to Oldest' });
    const selectedStat = ref('pullrequests');
    const sorts = ref([
      { name: 'Date Oldest to Newest' },
      { name: 'Date Newest to Oldest' },
    ]);
    const isZoomedIn = ref(false);
    const zoomedYear = ref(null);
    const zoomedMonth = ref(null);

    // Fetch data from backend
    const getPackage = async (date) => {
      const data = {
        'url': decodeURIComponent(route.params.url),
        'date': date
      };
      
      const postOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };
      try {
        const response = await fetchData('http://127.0.0.1:8000/package', postOptions);
        state.githubResponse = response;
        console.log(state.githubResponse);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    // Filter pull requests by selected users
    const filterPullRequests = (pullRequests, users) => {
      return users.length > 0
        ? pullRequests.filter(pr => users.includes(pr.user))
        : pullRequests;
    };

    // Sort list by date
    const sortListsDate = (list, choice) => {
      if (choice.name === 'Date Oldest to Newest') {
        return list.sort((a, b) => new Date(a.date) - new Date(b.date));
      } else {
        return list.sort((a, b) => new Date(b.date) - new Date(a.date));
      }
    };

    // Sort list by semantic score
    const sortListsScore = (list, choice) => {
      if (choice.name === 'Semantic Score Ascending') {
        return list.sort((a, b) => a.pr_title_semantic - b.pr_title_semantic);
      } else {
        return list.sort((a, b) => b.pr_title_semantic - a.pr_title_semantic);
      }
    };

    // Computed property for sorted pull requests
    const sortedPullRequests = computed(() => {
      if (!state.githubResponse) return [];
      let filteredList = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value);
      if (selectedSort.value.name.includes('Date')) {
        return sortListsDate(filteredList, selectedSort.value);
      } else {
        return sortListsScore(filteredList, selectedSort.value);
      }
    });

    // Count of pull requests
    const pullRequestCount = computed(() => {
      return sortedPullRequests.value.length;
    });

    // Format the updated date
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

    // List of users
    const userList = computed(() => {
      if (!state.githubResponse || !state.githubResponse.Repo.pull_requests) {
        return [];
      }
      const users = new Set();
      state.githubResponse.Repo.pull_requests.forEach(pr => {
        users.add(pr.user);
      });
      return Array.from(users);
    });

    // Handle selected users
    const handleSelectedUsers = (selected) => {
      selectedUsers.value = selected;
      console.log("Selected users:", selectedUsers.value);
      updateChartData();
    };

    // Chart options
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

    // Computes the pull request count per month for the chart
    const pullRequestsRange = computed(() => {
      let minDate = new Date(); // Set to a future date
      let maxDate = new Date(0); // Set to a past date
      const counts = {}; // Stores the count of pull requests per month

      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        // Filter pull requests based on selected users
        const filteredPullRequests = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value);
        filteredPullRequests.forEach(pr => {
          const date = new Date(pr.date);
          minDate = date < minDate ? date : minDate; // Update if PR date is earlier
          maxDate = date > maxDate ? date : maxDate; // Update if PR date is later
          const monthKey = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0'); // (YYYY-MM), per month key
          
          // Increment the pull request count for the month or initialize to 1 if no data
          counts[monthKey] = counts[monthKey] ? counts[monthKey] + 1 : 1;
        });
      }

      const labels = []; // Month labels
      const data = []; // Pull request counts
      for (let d = new Date(minDate); d <= maxDate; d.setMonth(d.getMonth() + 1)) {
        const key = d.getFullYear() + '-' + (d.getMonth() + 1).toString().padStart(2, '0');
        labels.push(key); // Add month label to labels array
        data.push(counts[key] || 0); // Add pull request count or 0 if no data
      }

      return { labels, data };
    });

    // Computes the commit count per month for the chart
    const commitsRange = computed(() => {
      let minDate = new Date(); // Set to a future date
      let maxDate = new Date(0); // Set to a past date
      const counts = {}; // Stores the count of commits per month

      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        // Filter commits based on selected users and flatten the commit arrays from pull requests
        const filteredCommits = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value).flatMap(pr => pr.commits);
        filteredCommits.forEach(commit => {
          const date = new Date(commit.date);
          minDate = date < minDate ? date : minDate; // Update minDate if the commit date is earlier
          maxDate = date > maxDate ? date : maxDate; // Update maxDate if the commit date is later
          const monthKey = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0'); // (YYYY-MM), per month key
          
          // Increment the commit count for the month (or initialize to 1 if no data)
          counts[monthKey] = counts[monthKey] ? counts[monthKey] + 1 : 1; 
        });
      }

      const labels = []; // Month labels
      const data = []; // Commit counts
      for (let d = new Date(minDate); d <= maxDate; d.setMonth(d.getMonth() + 1)) {
        const key = d.getFullYear() + '-' + (d.getMonth() + 1).toString().padStart(2, '0');
        labels.push(key); // Add month label to labels array
        data.push(counts[key] || 0); // Add commit count or 0 if no data
      }

      return { labels, data };
    });

    // Computes the average semantic score per month for the chart
    const semanticRange = computed(() => {
      let minDate = new Date(); // Set to a future date
      let maxDate = new Date(0); // Set to a past date
      const counts = {}; // Stores the sum and count of semantic scores per month

      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        // Filter commits based on selected users and flatten the commit arrays from the pull requests
        const filteredCommits = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value).flatMap(pr => pr.commits);
        filteredCommits.forEach(commit => {
          const date = new Date(commit.date);
          minDate = date < minDate ? date : minDate; // Update minDate if the commit date is earlier
          maxDate = date > maxDate ? date : maxDate; // Update maxDate if the commit date is later
          const monthKey = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0'); // (YYYY-MM), per month key
          
          // Computes the sum and count of semantic scores for each month
          if (!counts[monthKey]) {
            counts[monthKey] = { sum: 0, count: 0 };
          }
          counts[monthKey].sum += commit.semantic_score;
          counts[monthKey].count += 1;
        });
      }

      const labels = []; // Month labels
      const data = []; // Average semantic scores
      for (let d = new Date(minDate); d <= maxDate; d.setMonth(d.getMonth() + 1)) {
        const key = d.getFullYear() + '-' + (d.getMonth() + 1).toString().padStart(2, '0');
        labels.push(key); // Add month label to labels array
        data.push(counts[key] ? (counts[key].sum / counts[key].count) : 0); // Calculate average score or 0 if no data
      }

      return { labels, data };
    });

    // Updates the chart data based on the selected stat and zoom level
    const updateChartData = () => {
      if (isZoomedIn.value && zoomedYear.value && zoomedMonth.value) {
        handleBarClick({ label: `${zoomedYear.value}-${zoomedMonth.value.toString().padStart(2, '0')}` });
      } else {
        let data;
        if (selectedStat.value === 'commits') {
          data = commitsRange.value;
        } else if (selectedStat.value === 'semantic') {
          data = semanticRange.value;
        } else {
          data = pullRequestsRange.value;
        }
        chartData.value = {
          labels: data.labels,
          datasets: [{
            data: data.data,
            backgroundColor: '#42A5F5'
          }]
        };
      }
    };

    // Handles the clicking of the chart bars
    const handleBarClick = (label) => {
      console.log(`Clicked on bar: ${label}`);
      const [year, month] = label.label.split('-').map(Number); // Extract year and month from the label

      const filteredPullRequests = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value);

      let selectedMonthData;
      if (selectedStat.value === 'commits') {
        // If "commits" is selected, filter commits for the selected month
        selectedMonthData = filteredPullRequests.flatMap(pr => pr.commits).filter(commit => {
          const date = new Date(commit.date);
          return date.getFullYear() === year && date.getMonth() + 1 === month;
        });
      } else if (selectedStat.value === 'semantic') {
        // If "semantic" is selected, filter commits for the selected month
        selectedMonthData = filteredPullRequests.flatMap(pr => pr.commits).filter(commit => {
          const date = new Date(commit.date);
          return date.getFullYear() === year && date.getMonth() + 1 === month;
        });
      } else {
        // Otherwise, filter pull requests for the selected month
        selectedMonthData = filteredPullRequests.filter(pr => {
          const date = new Date(pr.date);
          return date.getFullYear() === year && date.getMonth() + 1 === month;
        });
      }

      const counts = {};
      selectedMonthData.forEach(item => {
        const date = new Date(item.date);
        const day = date.getDate(); // Get the day of the month
        if (selectedStat.value === 'semantic') {
          // If "semantic" is selected, calculate the sum and count of semantic scores
          if (!counts[day]) {
            counts[day] = { sum: 0, count: 0 };
          }
          counts[day].sum += item.semantic_score;
          counts[day].count += 1;
        } else {
          // Otherwise, increment the count for the day
          counts[day] = (counts[day] || 0) + 1;
        }
      });

      const daysInMonth = new Date(year, month, 0).getDate(); // Get the number of days in the month
      const labels = [];
      const data = [];
      for (let day = 1; day <= daysInMonth; day++) {
        labels.push(`${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`);
        if (selectedStat.value === 'semantic') {
          // Calculate average semantic score or 0 if no data
          data.push(counts[day] ? (counts[day].sum / counts[day].count) : 0);
        } else {
          // Add count or 0 if no data
          data.push(counts[day] || 0);
        }
      }

      chartData.value = {
        labels,
        datasets: [{
          data,
          backgroundColor: '#42A5F5'
        }]
      };

      isZoomedIn.value = true;
      zoomedYear.value = year;
      zoomedMonth.value = month;
    };

    // Reset chart view to monthly data
    const resetChartView = () => {
      let data;
      if (selectedStat.value === 'commits') {
        data = commitsRange.value;
      } else if (selectedStat.value === 'semantic') {
        data = semanticRange.value;
      } else {
        data = pullRequestsRange.value;
      }
      chartData.value = {
        labels: data.labels,
        datasets: [{
          data: data.data,
          backgroundColor: '#42A5F5'
        }]
      };

      isZoomedIn.value = false;
      zoomedYear.value = null;
      zoomedMonth.value = null;
    };

    const chartData = ref({
      labels: pullRequestsRange.value.labels,
      datasets: [{
        data: pullRequestsRange.value.data,
        backgroundColor: '#42A5F5'
      }]
    });

    watchEffect(() => {
      updateChartData();
    });

    onMounted(async () => {
      await getPackage('');
    });

    return {
      getPackage,
      state,
      sortedPullRequests,
      selectedSort,
      selectedStat,
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
    return {
      selectedOption: { name: 'Pull Requests'},
      options: [
        { name: 'Pull Requests' },
        { name: 'Contributors' },
      ],
      selectedRange: null,
    }
  },
}
</script>

<template>
  <header>
    <div v-if="state.githubResponse" style="margin-top: 50px">
      <div style="font-size: 240%; margin-bottom: 20px;"> {{ state.githubResponse.Repo.name }} </div>
      <a :href="state.githubResponse.Repo.url" target="_blank" style="margin-bottom: 5px"> URL: {{ state.githubResponse.Repo.url }} </a>
      <div style="font-size: 90%; margin-left: 3px; margin-top: 6px;"> Last Updated: {{ formattedDate }} </div>
    </div>  
  </header>

  <div style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px;" for="datePicker">Select date range:</label>
      <div id="datePicker" style="display: flex; align-items: flex-start;">
        <VueDatePicker v-model="selectedRange" range style="width: 300px; height: 50px;"></VueDatePicker>
        <button class="button-6" style="width: 57px; height: 38px; margin-left: 3px; font-size: smaller;" @click="getPackage(selectedRange)">Reload</button>
      </div>
    </div>
  </div>

  <div style="display: flex; justify-content: space-evenly; margin-top: 4%; height: 500px; max-width: 100%;">
    
    <div style="margin-right: 10px; margin-top: 70px; min-width: 160px; position: relative">
      <div>
        <input type="radio" id="semantic" name="stat" value="semantic" v-model="selectedStat">
        <label style="margin-left: 5px;" for="semantic">Semantic Score</label>
      </div>
      <div>
        <input type="radio" id="commits" name="stat" value="commits" v-model="selectedStat">
        <label style="margin-left: 5px;" for="commits">Commits</label>
      </div>
      <div>   
        <input type="radio" id="pullrequests" name="stat" value="pullrequests" v-model="selectedStat" checked>
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
            </button></router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

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
