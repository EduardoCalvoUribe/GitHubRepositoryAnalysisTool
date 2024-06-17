<script>
import { ref, onMounted, computed, watch } from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import { fetchData } from '../fetchData.js';
import { useRoute, useRouter } from 'vue-router';
import { state } from '../repoPackage.js';
import Chart from '../components/Chart.vue';
import Dropdown from 'primevue/dropdown';
import CheckBoxList from '../components/CheckBoxList.vue';
import { getGradientColor } from '../colorUtils.js';

export default {
  components: {
    VueDatePicker,
    Chart,
    Dropdown,
    CheckBoxList,
  },

  setup() {
    /**
     * @constant {Route} route - The current route object.
     */
    const route = useRoute();

    /**
     * @constant {Router} router - The router instance.
     */
    const router = useRouter();

    /**
     * @constant {Ref<Array>} selectedUsers - The selected users.
     */
    const selectedUsers = ref([]);

    /**
     * @constant {Ref<Object>} selectedSort - The selected sorting option: 'Date Newest to Oldest'.
     */
    const selectedSort = ref({ name: 'Date Newest to Oldest' });

    /**
     * @constant {Ref<String>} selectedStat - The selected statistic of the selected pull request.
     */
    const selectedStat = ref('pullrequests');

    /**
     * @constant {Ref<null|Array>} selectedRange - The selected date range.
     */
    const selectedRange = ref(null);

    /**
     * @constant {Ref<Array>} sorts - The available sorting options.
     */
    const sorts = ref([
      { name: 'Date Oldest to Newest' },
      { name: 'Date Newest to Oldest' },
      { name: 'Semantic Score Ascending' },
      { name: 'Semantic Score Descending' },
    ]);

    /**
     * @constant {Ref<Boolean>} isZoomedIn - Whether the chart is zoomed in.
     */
    const isZoomedIn = ref(false);

    /**
     * @constant {Ref<null|Number>} zoomedYear - The zoomed-in year.
     */
    const zoomedYear = ref(null);

    /**
     * @constant {Ref<null|Number>} zoomedMonth - The zoomed-in month.
     */
    const zoomedMonth = ref(null);

    /**
    * @constant {Ref<Boolean>} isBar - Whether the chart is in bar mode.
    */
    const isBar = ref(true);

    /**
     * @constant {Object} chartModes - The available chart modes.
     * @property {Object} pullrequests - Configuration for the pull requests chart mode.
     * @property {String} pullrequests.title - Title for the pull requests chart mode.
     * @property {Boolean} pullrequests.isBar - Whether the pull requests chart is in bar mode.
     * @property {Object} commits - Configuration for the commits chart mode.
     * @property {String} commits.title - Title for the commits chart mode.
     * @property {Boolean} commits.isBar - Whether the commits chart is in bar mode.
     * @property {Object} semantic - Configuration for the semantic score chart mode.
     * @property {String} semantic.title - Title for the semantic score chart mode.
     * @property {Boolean} semantic.isBar - Whether the semantic score chart is in bar mode.
     */
    const chartModes = {
      pullrequests: { title: 'Number of Pull Requests', isBar: true },
      commits: { title: 'Number of Commits', isBar: true },
      semantic: { title: 'Average Semantic Score for Commit Messages', isBar: false },
    };

    /**
     * Navigates back to the previous page.
     * @function goBack
     */
    const goBack = () => {
      router.go(-1); // Go back to the previous page
    };

    /**
    * Asynchronously updates the URL based on the provided date and updates the selectedRange.
    * 
    * @param {String|null} date - The date or date range to be used for updating the URL. 
    *                             Can be 'homepage' for the home page or null to reset the date.
    */
    const getPackage = async (date) => {
      const oldurl = route.path;
      let newUrl = "";
      if (
        (oldurl.includes("current") && (date == "homepage" || date == null)) ||
        (!oldurl.includes("current") && date == null)
      ) {
        // reset url and date
        newUrl = oldurl.split("/").slice(0, -1).join("/") + "/current";
        selectedRange.value = null;
      } else if (date == "homepage") {
        // get date from url
        const parts = oldurl.split("/");
        let date = decodeURIComponent(parts[parts.length - 1]);
        const dates = date.split(" - ");
        selectedRange.value = [new Date(dates[0]), new Date(dates[1])];
        newUrl = oldurl.split("/").slice(0, -1).join("/") + "/" + encodeURIComponent(date);
        date = dates;
      } else {
        // get date from date picker
        const dates = date;
        selectedRange.value = date;
        const start_date = selectedRange.value[0].toISOString();
        const end_date = selectedRange.value[1].toISOString();
        date = [start_date, end_date];
        newUrl = oldurl.split("/").slice(0, -1).join("/") + "/" + encodeURIComponent(start_date + " - " + end_date);
      }
      router.push(newUrl);

      /**
      * @constant {Object} data_send - The data to be sent in the POST request.
      * @property {String} data_send.url - The decoded URL from the route parameters.
      * @property {Array|null} data_send.date - The selected date range.
      */
      const data_send = {
        url: decodeURIComponent(route.params.url),
        date: selectedRange.value,
      };

      /**
       * @constant {Object} postOptions - The options for the POST request.
       * @property {String} postOptions.method - The HTTP method, set to 'POST'.
       * @property {Object} postOptions.headers - The headers for the request.
       * @property {String} postOptions.headers['Content-Type'] - The content type, set to 'application/json'.
       * @property {String} postOptions.body - The stringified JSON body of the request.
       */
      const postOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_send),
      };
      try {
        const response = await fetchData('http://127.0.0.1:8000/package', postOptions);
        state.githubResponse = response;
      } catch (error) {
        console.error('Error:', error);
      }
    };

    /**
   * Filters pull requests based on the selected users.
   * 
   * @param {Array} pullRequests - The list of pull requests to filter.
   * @param {Array} users - The list of selected users to filter by.
   * @returns {Array} The filtered list of pull requests.
   */
    const filterPullRequests = (pullRequests, users) => {
      return users.length > 0
        ? pullRequests.filter(pr => users.includes(pr.user))
        : pullRequests;
    };

    /**
   * Filters commits by the selected users from the given pull requests.
   * 
   * @param {Array} pullRequests - The list of pull requests to filter commits from.
   * @param {Array} users - The list of selected users to filter by.
   * @returns {Array} The filtered list of commits.
   */
    const filterCommits = (pullRequests, users) => {
      return users.length > 0
        ? pullRequests.flatMap(pr => {
          return pr.commits || [];
        }).filter(commit => commit && users.includes(commit.user))
        : pullRequests.flatMap(pr => pr.commits || []);
    };

    /**
   * Sorts a list by date.
   * 
   * @param {Array} list - The list to be sorted.
   * @param {Object} choice - The sorting choice object.
   * @param {String} choice.name - The name of the sorting option.
   * @returns {Array} The sorted list.
   */
    const sortListsDate = (list, choice) => {
      if (choice.name === 'Date Oldest to Newest') {
        return list.sort((a, b) => new Date(a.date) - new Date(b.date));
      } else {
        return list.sort((a, b) => new Date(b.date) - new Date(a.date));
      }
    };

    /**
   * Sorts a list by semantic score.
   * 
   * @param {Array} list - The list to be sorted.
   * @param {Object} choice - The sorting choice object.
   * @param {String} choice.name - The name of the sorting option.
   * @returns {Array} The sorted list.
   */
    const sortListsScore = (list, choice) => {
      if (choice.name === 'Semantic Score Ascending') {
        return list.sort((a, b) => a.average_semantic - b.average_semantic);
      } else {
        return list.sort((a, b) => b.average_semantic - a.average_semantic);
      }
    };

    /**
    * A computed property for sorted pull requests based on selected sort and users.
    * 
    * @computed
    * @returns {Array} The sorted and filtered list of pull requests.
    */
    const sortedPullRequests = computed(() => {
      if (!state.githubResponse) return [];
      let filteredList = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value);
      //Check which sorting option is selected. 
      if (selectedSort.value.name.includes('Date')) {
        return sortListsDate(filteredList, selectedSort.value);
      } else {
        return sortListsScore(filteredList, selectedSort.value);
      }
    });

    /**
   * A computed property for the count of sorted pull requests.
   * 
   * @computed
   * @returns {Number} The count of sorted pull requests.
   */
    const pullRequestCount = computed(() => {
      return sortedPullRequests.value.length;
    });

    /**
   * A computed property to format the updated date of the repository.
   * 
   * @computed
   * @returns {String} The formatted updated date of the repository, or 'Loading...' if not available.
   */
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

    /**
   * A computed property that returns a list of unique users from the pull requests.
   * 
   * @computed
   * @returns {Array} The list of unique users.
   */
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

    /**
   * Handles the selected users and updates the chart data.
   * 
   * @param {Array} selected - The list of selected users.
   */
    const handleSelectedUsers = (selected) => {
      selectedUsers.value = selected;
      updateChartData();
    };

    /**
   * Chart options for the chart component.
   * 
   * @constant {Object} chartOptions - The configuration object for the chart.
   * @property {Boolean} chartOptions.responsive - Indicates if the chart is responsive.
   * @property {Boolean} chartOptions.maintainAspectRatio - Indicates if the aspect ratio should be maintained.
   * @property {Object} chartOptions.scales - The scales configuration for the chart.
   * @property {Object} chartOptions.scales.y - The y-axis configuration.
   * @property {Boolean} chartOptions.scales.y.beginAtZero - Indicates if the y-axis should begin at zero.
   * @property {Object} chartOptions.plugins - The plugins configuration for the chart.
   * @property {Object} chartOptions.plugins.legend - The legend configuration.
   * @property {Boolean} chartOptions.plugins.legend.display - Indicates if the legend should be displayed.
   * @property {Object} chartOptions.plugins.title - The title configuration.
   * @property {Boolean} chartOptions.plugins.title.display - Indicates if the title should be displayed.
   * @property {String} chartOptions.plugins.title.text - The title text.
   * @property {Object} chartOptions.plugins.title.font - The font configuration for the title.
   * @property {Number} chartOptions.plugins.title.font.size - The font size for the title.
   */
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

    /**
   * A computed property that calculates the count of pull requests per month for the chart.
   * 
   * @computed
   * @returns {Object} The count of pull requests per month.
   */
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

    /**
   * A computed property that calculates the commit count per month for the chart.
   * 
   * @computed
   * @returns {Object} An object containing month labels and commit counts.
   * @returns {Array} returns.labels - The labels for each month.
   * @returns {Array} returns.data - The count of commits for each month.
   */
    const commitsRange = computed(() => {
      let minDate = new Date(); // Set to a future date
      let maxDate = new Date(0); // Set to a past date
      const counts = {}; // Stores the count of commits per month

      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        // Filter commits based on selected users and flatten the commit arrays from pull requests
        const filteredCommits = filterCommits(state.githubResponse.Repo.pull_requests, selectedUsers.value);
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

    /**
   * A computed property that calculates the average semantic score per month for the chart.
   * 
   * @computed
   * @returns {Object} An object containing month labels and average semantic scores.
   * @returns {Array} returns.labels - The labels for each month.
   * @returns {Array} returns.data - The average semantic scores for each month.
   */
    const semanticRange = computed(() => {
      let minDate = new Date(); // Set to a future date
      let maxDate = new Date(0); // Set to a past date
      const counts = {}; // Stores the sum and count of semantic scores per month

      if (state.githubResponse && state.githubResponse.Repo.pull_requests) {
        // Filter commits based on selected users and flatten the commit arrays from the pull requests
        const filteredCommits = filterCommits(state.githubResponse.Repo.pull_requests, selectedUsers.value);
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

    /**
   * Updates the chart data based on the selected stat and zoom level.
   */
    const updateChartData = () => {
      if (isZoomedIn.value && zoomedYear.value && zoomedMonth.value) {
        handleBarClick({ label: `${zoomedYear.value}-${zoomedMonth.value.toString().padStart(2, '0')}` });
      } else {
        const mode = chartModes[selectedStat.value];
        if (selectedStat.value === 'commits') {
          updateChart(commitsRange, mode.title, mode.isBar);
        } else if (selectedStat.value === 'semantic') {
          updateChart(semanticRange, mode.title, mode.isBar);
        } else {
          updateChart(pullRequestsRange, mode.title, mode.isBar);
        }
      }
    };

    /**
   * Updates the chart with new data based on a new range.
   * 
   * @param {Object} range - The computed property representing the data range.
   * @param {String} title - The title to display on the chart.
   * @param {Boolean} bar - Indicates if the chart should display as a bar chart.
   */
    const updateChart = (range, title, bar) => {
      const data = range.value;
      chartOptions.value.plugins.title.text = title;
      isBar.value = bar;
      chartData.value = {
        labels: data.labels,
        datasets: [{
          data: data.data,
          backgroundColor: '#42A5F5'
        }]
      };
    };

    /**
   * Handles the clicking of the chart bars.
   * 
   * @param {Object} label - The label object containing the clicked label information.
   * @param {String} label.label - The label text representing the clicked bar.
   */
    const handleBarClick = (label) => {
      const [year, month] = label.label.split('-').map(Number); // Extract year and month from the label

      let filteredData;

      if (selectedStat.value === 'commits' || selectedStat.value === 'semantic') {
        // If "commits" or "semantic" is selected, filter commits for the selected month
        filteredData = filterCommits(state.githubResponse.Repo.pull_requests, selectedUsers.value).filter(commit => {
          if (!commit || !commit.date) return false;
          const date = new Date(commit.date);
          return date.getFullYear() === year && date.getMonth() + 1 === month;
        });
      } else {
        // Otherwise, filter pull requests for the selected month
        filteredData = filterPullRequests(state.githubResponse.Repo.pull_requests, selectedUsers.value).filter(pr => {
          if (!pr || !pr.date) return false;
          const date = new Date(pr.date);
          return date.getFullYear() === year && date.getMonth() + 1 === month;
        });
      }

      const counts = {};
      filteredData.forEach(item => {
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

      // Determine the title and isBar flag based on the selected stat
      const mode = chartModes[selectedStat.value];

      // Call updateChart with the processed data
      updateChart({ value: { labels, data } }, mode.title, mode.isBar);

      isZoomedIn.value = true;
      zoomedYear.value = year;
      zoomedMonth.value = month;
    };

    /**
    * Resets the chart to the monthly data. 
    */
    const resetChartView = () => {
      const mode = chartModes[selectedStat.value];
      let data;
      if (selectedStat.value === 'commits') {
        data = commitsRange.value;
      } else if (selectedStat.value === 'semantic') {
        data = semanticRange.value;
      } else {
        data = pullRequestsRange.value;
      }
      updateChart({ value: { labels: data.labels, data: data.data } }, mode.title, mode.isBar);

      isZoomedIn.value = false;
      zoomedYear.value = null;
      zoomedMonth.value = null;
    };

    /**
   * Sets the labels of the chart to the labels from the pull request data. 
   */
    const chartData = ref({
      labels: pullRequestsRange.value.labels,
      datasets: [{
        data: pullRequestsRange.value.data,
        backgroundColor: '#42A5F5'
      }]
    });

    /**
   * Sets color of the semantic score box in rgb values based on the semantic score.  
   */
    const scoreColor = computed(() => {
      const score = state.githubResponse ? state.githubResponse.Repo.average_semantic : 0;
      return {
        border: `5px solid ${getGradientColor(score, 10)}`,
        padding: '10px',
        paddingTop: '8px',
      };
    });

    /**
  * Calls updateChartData() everytime selectedUsers or selectedStat changes. 
  */
    watch([selectedUsers, selectedStat], () => {
      updateChartData();
    });

    /**
  * Calls a pachage when the page loads. 
  */
    onMounted(async () => {
      await getPackage("homepage");
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
      isBar,
      goBack,
      selectedRange,
      scoreColor
    }
  },

  data() {
    return {
      selectedOption: { name: 'Pull Requests' },
      options: [
        { name: 'Pull Requests' },
        { name: 'Contributors' },
      ],
    }
  },

  /**
* Handles the routing using a specific pull request user. 
* 
* @param {user} user - The user that the page should be redirected to. 
*/
  methods: {
    goToUserPage(user) {
      this.$router.push({ path: '/userpage', query: { selectedUser: user } });
    }
  }
}
</script>

<template>
  <!-- Header for the page that shows the repository name and when it was last updated. -->
  <header>
    <div v-if="state.githubResponse" style="margin-top: 50px">
      <div style="font-size: 240%; margin-bottom: 20px;"> {{ state.githubResponse.Repo.name }} </div>
      <a :href="state.githubResponse.Repo.url" target="_blank" style="margin-bottom: 5px"> URL: {{
        state.githubResponse.Repo.url }} </a>
      <div style="font-size: 90%; margin-left: 3px; margin-top: 6px;"> Last Updated: {{ formattedDate }} </div>
    </div>
  </header>

  <!-- The date package and the button to reload the data based on the picked date range. -->
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
      <div :style="scoreColor" class="stat-container">
        Average Semantic Score: {{ state.githubResponse.Repo.average_semantic ?
          state.githubResponse.Repo.average_semantic.toFixed(2) : 'N/A' }}/100
      </div>
    </div>
  </div>

  <!-- The chart info per semantic score, commit or pull request and the button to reset the chart view. -->
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
      <button class="button-6" v-if="isZoomedIn" @click="resetChartView"
        style="position: absolute; bottom: 10px; right: 10px; margin-top: 20px; width: 40px; height: 40px; justify-content: center; vertical-align: center; font-size: larger;">
      <</button>
    </div>

    <!-- Chart displaying the chart data and users. -->
    <Chart style="flex: 1; max-width: 1000px" @bar-click="handleBarClick" :chartData="chartData"
      :chartOptions="chartOptions" :isBar="isBar" />

    <div style="margin-left: 40px; margin-top: 50px;">
      <CheckBoxList :usernames="userList" @update:selected="handleSelectedUsers" />
    </div>
  </div>

  <!-- Drop down menu with options for the user to select their sort option. -->
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
                  <h3 style="margin-left: 0.3rem;">{{ pullrequest.title }}</h3>
                </span>
                <div class="pr-details">
                  <span class="last-accessed">Author: {{ pullrequest.user }}</span>
                  <span class="last-accessed">Semantic score: {{ pullrequest.average_semantic.toFixed(2) }}</span>
                  <span class="last-accessed">Date: {{ pullrequest.date.split('T')[0] }}</span>
                </div>
              </button></router-link>
          </div>
        </div>
      </div>
      <div v-else-if="selectedOption && selectedOption.name === 'Contributors' && state.githubResponse"
        style=" display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <h1 style="justify-content: center; display: inline-block; width: 250px; margin-bottom: 10px;" for="users">
            Contributors</h1>
          <div id="users" class="row" v-for="user in userList">
            <button style="margin-top: 7px;" class="button-6" @click="goToUserPage(user)">
              <span>
                <h2 style="margin-left: 0.3rem;">{{ user }}</h2>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Back button to go to previous page -->
  <button @click="goBack" class="button-6" style="width: 50px; height: 50px; font-size: 90%;">Back</button>
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

.pr-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-left: 0.3rem;
}

.pr-details span {
  width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.last-accessed {
  min-width: 140px;
  text-align: left;
}
</style>
