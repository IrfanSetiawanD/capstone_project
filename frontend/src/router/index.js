// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: () => import('../pages/Home.vue') },
    { path: '/login', name: 'Login', component: () => import('../pages/Login.vue') },
    { path: '/menu', name: 'Menu', component: () => import('../pages/Menu.vue') },
    { path: '/contact', name: 'Contact', component: () => import('../pages/Contact.vue') },

    // ADMIN AREA - Semua admin/owner boleh masuk
    {
      path: '/admin',
      component: () => import('../layouts/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'AdminDashboard', component: () => import('../pages/AdminDashboard.vue') },
        { path: 'customers', name: 'LoyalCustomers', component: () => import('../pages/LoyalCustomers.vue') },
        { path: 'orders', name: 'OrderReports', component: () => import('../pages/OrderReports.vue') },
        { 
          path: 'settings', 
          name: 'AdminSettings', 
          component: () => import('../pages/AdminSettings.vue'),
          meta: { requiresOwner: true } 
        },
      ]
    }
  ]
})

// Navigation Guard yang sangat simpel
router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (auth.loading) {
    await new Promise(r => setTimeout(r, 100))
  }

  const isLoggedIn = !!auth.user

  // Harus login untuk masuk /admin
  if (to.path.startsWith('/admin') && !isLoggedIn) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  // Hanya Owner yang boleh ke Settings
  if (to.meta.requiresOwner && !auth.isOwner) {
    return { name: 'AdminDashboard' }
  }

  // Jika sudah login tapi ke halaman login
  if (to.path === '/login' && isLoggedIn) {
    return { name: 'AdminDashboard' }
  }
})

export default router