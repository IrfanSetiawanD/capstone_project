<template>
  <aside class="fixed inset-y-0 left-0 w-64 bg-[#0a0a0a] border-r border-white/5 flex flex-col z-50">
    <!-- Header -->
    <div class="p-8 border-b border-white/10">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-red-600 rounded-2xl flex items-center justify-center text-white font-bold text-2xl">
          M
        </div>
        <div>
          <h1 class="font-oswald text-2xl font-bold tracking-tight">MASASHIMURA</h1>
          <p class="text-[10px] text-white/40 -mt-1">ADMIN PANEL</p>
        </div>
      </div>
    </div>

    <!-- User Info -->
    <div class="px-6 py-4 border-b border-white/10">
      <p class="text-sm font-medium">{{ user?.name || 'Admin' }}</p>
      <p class="text-[10px] text-white/50 capitalize">{{ user?.role || 'staff' }}</p>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-6 space-y-1">
      <router-link 
        to="/admin" 
        class="nav-link"
        :class="{ active: isActive('/admin') }"
      >
        <LayoutDashboard size="18" />
        <span>Dashboard</span>
      </router-link>

      <router-link 
        to="/admin/customers" 
        class="nav-link"
        :class="{ active: isActive('/admin/customers') }"
      >
        <Users size="18" />
        <span>Loyal Customers</span>
      </router-link>

      <router-link 
        to="/admin/orders" 
        class="nav-link"
        :class="{ active: isActive('/admin/orders') }"
      >
        <ClipboardList size="18" />
        <span>Order Reports</span>
      </router-link>

      <!-- Hanya Owner yang bisa melihat Settings -->
      <router-link 
        v-if="isOwner"
        to="/admin/settings" 
        class="nav-link"
        :class="{ active: isActive('/admin/settings') }"
      >
        <Settings size="18" />
        <span>Settings</span>
      </router-link>
    </nav>

    <div v-if="isOwner">
  <button @click="openCreateUserModal">
    + Tambah User Baru (Admin/Owner)
  </button>
</div>

    <!-- Logout -->
    <div class="p-6 border-t border-white/5 mt-auto">
      <button
        @click="handleLogout"
        class="flex items-center gap-3 w-full p-3 hover:bg-red-500/10 text-red-400 hover:text-red-500 rounded-2xl transition-all font-medium text-sm"
      >
        <LogOut size="18" />
        Keluar Sistem
      </button>
    </div>
  </aside>
</template>

<script setup>
import { LayoutDashboard, Users, ClipboardList, Settings, LogOut } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

// Computed dari store (lebih bersih)
const user = computed(() => auth.user)
const isOwner = computed(() => auth.isOwner)   // ← pakai yang sudah ada di store

// Helper untuk cek active route (lebih scalable)
const isActive = (path) => {
  return route.path === path
}

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  color: #9ca3af;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: white;
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.25);
  position: relative;
}

.nav-link.active::before {
  content: '';
  position: absolute;
  left: -6px;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 36px;
  background: #ef4444;
  border-top-right-radius: 9999px;
  border-bottom-right-radius: 9999px;
}
</style>