<template>
  <div class="flex h-screen bg-[#050505] overflow-hidden">
    <!-- Sidebar -->
    <AdminSidebar />

    <!-- Konten Utama -->
    <div class="flex-1 flex flex-col min-h-0">
      <main class="flex-1 p-8 md:p-12">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import AdminSidebar from '@/components/AdminSidebar.vue'
</script>

<style scoped>
.custom-scroll {
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.2) transparent;
}

.custom-scroll::-webkit-scrollbar {
  width: 6px;
}

.custom-scroll::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.25);
  border-radius: 3px;
}

.custom-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(255,255,255,0.4);
}
</style>