<template>
  <div class="min-h-screen bg-[#050505]">
    <template v-if="!isAdminRoute">
      <Navbar />
      <router-view />
      <Footer />
    </template>

    <AdminLayout v-else>
      <router-view />
    </AdminLayout>

    <Toaster position="top-center" rich-colors />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import AdminLayout from './layouts/AdminLayout.vue'
import { Toaster } from 'vue-sonner'

const route = useRoute()
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
</script>