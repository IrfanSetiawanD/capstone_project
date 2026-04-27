import { createApp } from "vue";
import { createPinia } from "pinia"; // 1. Import Pinia
import App from "./App.vue";
import router from "./router";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "bootstrap/dist/css/bootstrap.min.css";
// Opsional: Import JS Bootstrap agar Navbar toggler berfungsi
import "bootstrap/dist/js/bootstrap.bundle.min.js";

const app = createApp(App);
const pinia = createPinia(); // 2. Buat instance Pinia

app.use(pinia);
app.use(router);
app.use(Toast);

app.mount("#app");
