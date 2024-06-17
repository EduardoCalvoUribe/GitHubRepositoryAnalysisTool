import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import PrimeVue from "primevue/config";
import "primevue/resources/themes/aura-light-green/theme.css";
import Dropdown from "primevue/dropdown";
// Create app.
const app = createApp(App);

// Allow web app to use Vue router.
app.use(router);
// Allow web app to use Vue datepicker.
app.component("VueDatePicker", VueDatePicker);
// Allow web app to use PrimeVue.
app.use(PrimeVue);
// Allow web app to use dropdown menu.
app.component("Dropdown", Dropdown);

// Mount app.
app.mount("#app");
