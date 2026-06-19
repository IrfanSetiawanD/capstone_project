import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "Home", component: () => import("../pages/Home.vue") },
    {
      path: "/login",
      name: "Login",
      component: () => import("../pages/Login.vue"),
    },
    {
      path: "/register",
      name: "Register",
      component: () => import("../pages/Register.vue"),
    },
    {
      path: "/menu",
      name: "Menu",
      component: () => import("../pages/Menu.vue"),
    },
    {
      path: "/contact",
      name: "Contact",
      component: () => import("../pages/Contact.vue"),
    },

    // Admin Group Routes
    {
      path: "/admin",
      component: () => import("../layouts/AdminLayout.vue"),
      meta: { requiresAuth: true },
      children: [
        {
          path: "",
          name: "AdminDashboard",
          component: () => import("../views/admin/AdminDashboard.vue"),
        },
        {
          path: "menus",
          name: "ManageMenus",
          component: () => import("../views/admin/ManageMenus.vue"),
        },
        {
          path: "orders",
          name: "ActiveOrders",
          // Mengarah ke file tabel pesanan yang benar
          component: () => import("../views/admin/ActiveOrders.vue"),
        },
        {
          path: "reports",
          name: "OrderReports",
          // Mengarah ke file statistik/laporan
          component: () => import("../pages/OrderReports.vue"),
        },
        {
          path: "pos",
          name: "NewOrder",
          component: () => import("../pages/NewOrder.vue"),
        },
        {
          path: "customers",
          name: "LoyalCustomers",
          component: () => import("../pages/LoyalCustomers.vue"),
        },
        {
          path: "settings",
          name: "AdminSettings",
          component: () => import("../views/admin/AdminSettings.vue"),
          meta: { roles: ["owner"] },
        },
      ],
    },
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

// Auth Guard
router.beforeEach((to) => {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("role");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) return { name: "Login" };

    // Proteksi role pelanggan agar tidak masuk ke area admin
    if (userRole === "pelanggan") return { name: "Menu" };

    // Proteksi rute khusus owner
    if (to.meta.roles && !to.meta.roles.includes(userRole))
      return { name: "AdminDashboard" };
  }

  // Mencegah user yang sudah login mengakses halaman auth
  if ((to.name === "Login" || to.name === "Register") && token)
    return { name: "AdminDashboard" };

  return true;
});

export default router;
