<template>
  <div class="min-h-screen bg-[#050505]">
    <template v-if="!isAdminRoute">
      <Navbar />
      <router-view />
      <Footer />
    </template>

    <template v-else>
      <router-view />
    </template>

    <Toaster position="top-center" rich-colors />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Toaster } from "vue-sonner";

// Pastikan path import merujuk langsung ke file .vue, bukan index.js
import Navbar from "@/components/ui/layouts/Navbar.vue";
import Footer from "@/components/ui/layouts/Footer.vue";

const route = useRoute();

// Mengecek apakah user sedang berada di halaman yang diawali dengan /admin
const isAdminRoute = computed(() => route.path.startsWith("/admin"));
</script>
