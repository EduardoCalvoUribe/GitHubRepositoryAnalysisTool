import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueGridLayout from 'vue-grid-layout';

const app = createApp(App)

app.use(router)

app.mount('#app')
