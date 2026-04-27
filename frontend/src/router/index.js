import { createRouter, createWebHistory } from "vue-router";

import Home from "../pages/Home.vue";
import Menu from "../pages/Menu.vue";
import Cart from "../pages/Cart.vue";
import Dashboard from "../pages/Dashboard.vue";
import Contact from "../pages/Contact.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/menu", component: Menu },
  { path: "/cart", component: Cart },
  { path: "/dashboard", component: Dashboard },
  { path: "/contact", component: Contact },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
