import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-light-green/theme.css'
import Dropdown from 'primevue/dropdown';
// import SelectButton from 'primevue/selectbutton';

const app = createApp(App)

app.use(router)
app.component('VueDatePicker', VueDatePicker);

app.use(PrimeVue)
app.component('Dropdown', Dropdown);
// app.component('SelectButton', SelectButton);

app.mount('#app')
