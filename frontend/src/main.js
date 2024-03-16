import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Argon from '@/plugins/argon-kit'

const vue_app = createApp(App)
vue_app.use(Argon);
vue_app.mount('#app')
