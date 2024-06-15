<script>
import { ref, onMounted, computed } from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { fetchData } from '../fetchData.js'
import { useRouter } from 'vue-router';
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
    const route = useRoute(); // allows for passage of variables from homepage to current page
    const router = useRouter();
    const selectedRange = ref(null);
    const selectedUsers = ref([]);
    //const repoUrl = ({'url': decodeURIComponent(route.params.url)}).url;
    // console.log(repoUrl, "url?")
    // const postOptions = { // defines how data is sent to backend, POST request in this case
    //       method: 'POST',
    //       headers: {
    //           'Content-Type': 'application/json',
    //       },
    //       body: JSON.stringify(repoUrl),
    //   };
    // const response = await fetchData('http://127.0.0.1:8000/package', postOptions); // send repo id to backend function through path 'database'
    // console.log("received")
    // githubResponse.value = response;

    const selectedSort = ref({ name: 'Date Newest to Oldest' }); // sort option user selects from dropdown menu, default set to newest to oldest?
    const sorts = ref([ // different possible sort options
      { name: 'Semantic Score Ascending' },
      { name: 'Semantic Score Descending' },
      { name: 'Date Oldest to Newest' },
      { name: 'Date Newest to Oldest' },
    ]);


    const getPackage = async (date) => {
      const oldurl = route.path;
      let newUrl = ""
      console.log(date, oldurl.includes("current"))
      if ((oldurl.includes("current") && (date == "" || date == null)) || (!oldurl.includes("current") && date == null)) { // reset url and date
        newUrl = (oldurl.split("/")).slice(0, -1).join("/") + "/current"
        selectedRange.value = null;
      } else if (date == "") { // get date from url
        const parts = oldurl.split("/");
        const date = decodeURIComponent(parts[parts.length - 1]);
        const dates = date.split(" - ");
        selectedRange.value = [new Date(dates[0]), new Date(dates[1])];
        console.log([new Date(dates[0]), new Date(dates[1])])
        newUrl = (oldurl.split("/")).slice(0, -1).join("/") + "/" + encodeURIComponent(date);
      } else { // get date from date picker
        const dates = date
        selectedRange.value = date
        console.log(selectedRange.value[0], selectedRange.value[1], "dates")
        const start_date = selectedRange.value[0].toISOString()
        const end_date = selectedRange.value[1].toISOString()
        newUrl = (oldurl.split("/")).slice(0, -1).join("/") + "/" + encodeURIComponent(start_date + " - " + end_date);
      }
      router.push(newUrl);


      const data = {
        'url': decodeURIComponent(route.params.url),
        'date': selectedRange.value
      };

      const postOptions = { // defines how data is sent to backend, POST request in this case
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };
      // try {
      const response = await fetchData('http://127.0.0.1:8000/package', postOptions); // send repo id to backend function through path 'database'

      state.githubResponse = response;
      console.log(state.githubResponse);
    }

    const sortListsDate = (list, choice) => {
      if (choice.name == 'Date Oldest to Newest') {
        return list.sort((a, b) => new Date(a.date) - new Date(b.date));
      } else return list.sort((a, b) => new Date(b.date) - new Date(a.date));
    };

    const sortListsScore = (list, choice) => {
      if (choice.name == 'Semantic Score Ascending') {
        return list.sort((a, b) => (a.average_semantic) - (b.average_semantic));
      } else {
        return list.sort((a, b) => (b.average_semantic) - (a.average_semantic));
      }
    };

    const sortedPullRequests = computed(() => {
      if (!state.githubResponse) return [];
      else if (selectedSort.value.name.includes('Date')) {
        return sortListsDate(state.githubResponse.Repo.pull_requests, selectedSort.value);
      } else return sortListsScore(state.githubResponse.Repo.pull_requests, selectedSort.value);
    });

    const sortedUsers = computed(() => {
      if (!state.githubResponse) return [];
      return sortListsScore(state.githubResponse.Repo.pull_requests, selectedSort.value);
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

    const chartData = ref({
      labels: pullRequestsRange.value.labels,
      datasets: [{
        data: pullRequestsRange.value.data,
        backgroundColor: '#42A5F5'
      }]
    });

    onMounted(async () => {
      await getPackage("");
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
      selectedRange,
    }
  },

  data() {
    return {
      selectedOption: { name: 'Pull Requests' }, // view option user selects from dropdown menu, default set to pull requests
      options: [ // different possible view options
        { name: 'Pull Requests' },
        { name: 'Contributors' },
        // Add more options if needeed
      ],
      items: [ // items are the boxes with content being diplayed on the page§
        { id: 1, text: 'Number of Pull Requests: ' + fakejson.repository.number_of_commits, path: '/prpage' },
        { id: 2, text: 'Number of Commits: ' + fakejson.repository.number_of_commits, path: '/commitpage' },
        { id: 3, text: 'Extra Repository Information' },
        // Add more items as needed
      ],
    }
  },

  computed: {
    buttonColor() {
      return {
        backgroundColor: this.getGradientColor(state.githubResponse.Repo.average_semantic)
      }
    }
  },

  methods: {
    getGradientColor(score) {
      const startColor = { r: 255, g: 0, b: 0 }; // Red
      const endColor = { r: 0, g: 255, b: 0 }; // Green

      const r = Math.round(startColor.r + (endColor.r - startColor.r) * score);
      const g = Math.round(startColor.g + (endColor.g - startColor.g) * score);
      const b = Math.round(startColor.b + (endColor.b - startColor.b) * score);

      return `rgb(${r}, ${g}, ${b})`;
    }
  }
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
      <a :href="state.githubResponse.Repo.url" target="_blank" style="margin-bottom: 5px"> URL: {{
        state.githubResponse.Repo.url }} </a>
      <div style="font-size: 90%; margin-left: 3px; margin-top: 6px;"> Last Updated: {{ formattedDate }} </div>
    </div>
  </header>

  <!-- DATE PICKER -->
  <div style="margin-top: 4%; display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <label style="justify-content: center; display: inline-block; width: 250px;" for="datePicker">Select date
        range:</label>
      <div id="datePicker" style="display: flex; align-items: flex-start;">
        <VueDatePicker v-model="selectedRange" range style="width: 500px; height: 50px;"></VueDatePicker>
        <button class="button-6" style="width: 57px; height: 38px; margin-left: 3px; font-size: smaller;"
          @click="getPackage(selectedRange)">Reload</button>
      </div>
    </div>
  </div>

  <!-- INFO BOXES -->
  <div v-if="state.githubResponse" class="grid-container-2">
    <div class="info-section">
      <div class="stat-container">
        Number of Commits: {{ state.githubResponse.Repo.total_commit_count ?
          state.githubResponse.Repo.total_commit_count : 'N/A' }}
      </div>
    </div>

    <div class="info-section">
      <div class="stat-container">
        Number of Comments: {{ state.githubResponse.Repo.total_comment_count ?
          state.githubResponse.Repo.total_comment_count : 'N/A' }}
      </div>
    </div>

    <div class="info-section">
      <div :style="buttonColor" class="stat-container">
        Average Semantic Score: {{ state.githubResponse.Repo.average_semantic ?
          state.githubResponse.Repo.average_semantic.toFixed(2) : 'N/A' }}
      </div>
    </div>
  </div>

  <!-- GRAPH -->
  <div style="display: flex; justify-content: space-evenly; margin-top: 4%; height: 500px; max-width: 80%;">

    <div style="margin-right: 40px;">
      <div>
        <input type="radio" id="semantic" name="stat" value="semantic">
        <label for="semantic">Semantic Score</label>
      </div>
      <div>
        <input type="radio" id="engagement" name="stat" value="engagement">
        <label for="engagement">Engagement Score</label>
      </div>
      <div>
        <input type="radio" id="commits" name="stat" value="commits">
        <label for="commits">Commits</label>
      </div>
      <div>
        <input type="radio" id="pullrequests" name="stat" value="pullrequests">
        <label for="pullrequests">Pull Requests</label>
      </div>
    </div>

    <Chart :chartData="chartData" :chartOptions="chartOptions" />

    <div style="margin-left: 20px; ">
      <CheckBoxList :usernames="userList" @update:selected="handleSelectedUsers" />
    </div>

  </div>

  <!-- PULL REQUESTS and CONTRIBUTORS -->
  <div style="margin-top: 4%; display: flex; justify-content: center; margin-bottom: 5%;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <div style="margin-bottom: 25px;">
        <Dropdown v-model="selectedOption" :options="options" optionLabel="name" placeholder="Select an Option"
          class="w-full md:w-14rem" style="margin-right: 10px;" />
        <Dropdown v-model="selectedSort" :options="sorts" optionLabel="name" placeholder="Sort by"
          class="w-full md:w-14rem" />
      </div>
      <div v-if="selectedOption && selectedOption.name === 'Pull Requests' && state.githubResponse"
        style=" display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <h1 style="justify-content: center; display: inline-block; width: 250px;" for="pullRequests">Pull Requests
          </h1>
          <div style="margin-top: 10px; justify-content: center;">
            Total Pull Requests: {{ pullRequestCount }}
          </div>
          <div id="pullRequests" class="row" v-for="pullrequest in sortedPullRequests">
            <router-link :to="{ path: '/prpage/' + encodeURIComponent(pullrequest.url) }"><button class="button-6">
                <span>
                  <h2 style="margin-left: 0.3rem;">{{ pullrequest.title }}</h2>
                </span>
                <span class="last-accessed">Author: {{ pullrequest.user }}</span>
                <span class="last-accessed">Semantic score: {{ pullrequest.average_semantic.toFixed(2) }}</span>
                <span class="last-accessed">Date {{ pullrequest.date }}</span>
              </button></router-link>
          </div>
        </div>
      </div>
      <div v-else-if="selectedOption && selectedOption.name === 'Contributors' && state.githubResponse"
        style=" display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <h1 style="justify-content: center; display: inline-block; width: 250px;" for="users">Contributors</h1>
          <div id="users" class="row" v-for="pullrequest in state.githubResponse.Repo.pull_requests">
            <router-link :to="{ path: '/userpage' }"><button class="button-6">
                <span>
                  <h2 style="margin-left: 0.3rem;">{{ pullrequest.user }}</h2>
                </span>
                <span class="last-accessed">Semantic score:</span>
              </button></router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div style="display: flex; justify-content: center; margin-top: 4%; height: 400px;">
    <BarChart :chartData="chartData" :chartOptions="chartOptions" />
  </div>
  <button class="button-6" style="width: 50px; height: 50px; justify-content: center; font-size: 90%;"
    @click="$router.go(-1)">
    Back
  </button>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.grid-container-2 {
  display: flex;
  grid-template-columns: repeat(3, 1fr);
  align-items: center;
  justify-content: space-evenly;
  gap: 10px;
  padding: 10px;
}

.stat-container {
  background-color: white;
  border: 1px solid #157eff4d;
  border-radius: 5px;
  width: 100%;
  height: 50px;
  width: 300px;
  margin-top: 20px;
  justify-content: center;
  text-align: center;
  padding: 4%;
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
