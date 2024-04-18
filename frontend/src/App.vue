<script>
import { ref, onMounted } from 'vue';
import { fetchData } from './fetchData.js'

import Badge from './components/Badge.vue';
import BaseSlider from './components/BaseSlider.vue';
import CustomControls from './views/components/CustomControls.vue';
import BaseButton from './components/BaseButton.vue';
import BaseInput from './components/BaseInput.vue';

export default {
  components: {
    Badge,
    BaseSlider,
    CustomControls,
    BaseButton,
    BaseInput
  },
  setup() {
    const repoInfo = ref([
        {
            "name": "repo hahahah",
            "last_accessed": "2022-01-01"
        },
        {
            "name": "repo2",
            "last_accessed": "2022-01-02"
        },
        {
            "name": "repo3",
            "last_accessed": "2022-01-03"
        },
        {
            "name": "repo4",
            "last_accessed": "2022-01-04"
        },
    ]);

    onMounted(async () => {
      try {
        // Fetches json data from specified URL using our fetchData function (will be our backend endpoints)
        // const json_response = await fetchData('http://127.0.0.1:8000/github/user');
        // const fake_response = await fetchData('http://jsonplaceholder.typicode.com/posts/1');

        // Selects first div with specified id (such as 'github_request')
        // const fakeDiv = document.getElementById('fake_request');

        // Inserts content of json into that div in whatever specified format
        // fakeDiv.innerHTML = '<pre>' + JSON.stringify(fake_response, null, 2) + '</pre>';
        

        // this.tableContent = '<p>Test content for tableContent</p>';
        // this.githubResponse = '<p>Test content for githubResponse</p>';
        // getTrackedRepositories();
      } catch (error) {
        console.error('Error:', error)
      }

      // const githubURL = ref('');

      // return { githubURL };

    });

    return { repoInfo };
  },
  // TODO: Fix githubURL, it's just empty. Input is not correctly retrieved from Input Box.
  data() {
    return {
      githubURL: '',
      tableContent: '',
      githubResponse: ''
    }
  },
  methods: {
    async handleGithubURLSubmit() {
      //var githubURL = document.getElementById('githubURL').value;
      console.log('handleGithubURLSubmit called') 
      console.log(this.githubURL)
      const data = {'url': this.githubURL};

      const postOptions = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      };

      try {
          // https://github.com/IntersectMBO/plutus
          // TODO: Instead of cocatenating, extract from POST options (postOptions.body?). Also modify urls.py for this
          const response = await fetchData('http://127.0.0.1:8000/github/github-pulls/'.concat(githubURL), postOptions);
          // const response = await fetch(url, postOptions);
          // const json = await response.json();
          this.githubResponse = '<p><h5>Data from Backend:</h5><br>' + JSON.stringify(response) + '</p>';

      } catch (error) {
          console.error('Error:', error);
      }
    },
  }
};
</script>


<template>
  <header>
    <div style="font-size: 180%;">
      Repository Analysis Tool
    </div>
  </header>

  <main>
    <div style="margin-top: 4%; display: flex; justify-content: center;">
      <div style="display: flex;">
        <BaseInput style="width: 140%; margin: 0 auto;" label="Enter GitHub URL" v-model="githubURL"></BaseInput>
        <BaseButton type="primary" size="sm" style="height: 50px; margin-left: 100px; margin-top: 8%;" @click="handleGithubURLSubmit">Submit</BaseButton>
      </div>
    </div>

    <!-- id="github_request" -->
    <div style="margin-top: 10%;" v-html="githubResponse" ></div> 


    <!-- <br><br>
    <h5>Fake Request:</h5>
    <div id="fake_request"></div>
    <br><br> -->

    
    <!-- <Badge type="primary" rounded>Primary</Badge>
    <Badge type="info" rounded>Info</Badge>
    <Badge type="danger" rounded>Danger</Badge>
    <Badge type="default" rounded>Default</Badge>
    <Badge type="warning" rounded>Warning</Badge>
    <Badge type="success" rounded>Success</Badge>
    
    <BaseSlider value=10 disabled="" type="primary" ></BaseSlider> -->

    
  <div class="container ct-example-row" v-for="repo in repoInfo">
    <div class="row">
      <div class="col-2">
        <span><base-button style="width: 300%; margin-left: 202px" outline type="secondary" size = "lg">{{ repo.name }}</base-button></span>
      </div>
      <div class="col-1">
        <span><base-button style=" margin-left: 465px" size="lg" type="secondary" disabled>{{ repo.last_accessed }}</base-button></span>
      </div>
      <div class="col-3">
        <span><base-button style="margin-left: 487px; height: 100%" type="primary" icon="ni ni-fat-remove"></base-button></span>
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
