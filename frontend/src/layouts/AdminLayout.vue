<template>
  <div
    class="min-h-screen bg-[#050505] text-white font-manrope antialiased flex"
  >
    <AdminSidebar />

    <div class="flex-1 min-h-screen flex flex-col min-w-0">
      <main class="flex-grow px-8 py-10 w-full">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
/**
 * Path import disesuaikan dengan struktur folder:
 * src/components/ui/layout/AdminSidebar.vue
 */
import AdminSidebar from "@/components/ui/layouts/AdminSidebar.vue";
</script>
