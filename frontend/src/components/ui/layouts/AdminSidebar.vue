<template>
  <aside
    class="sticky top-0 h-screen w-64 bg-[#0a0a0a] border-r border-white/5 flex flex-col shrink-0 text-white select-none font-inter"
  >
    <!-- Header Brand -->
    <div class="p-8">
      <h1 class="font-oswald text-2xl font-bold tracking-tight text-white">
        MASASHIMURA
      </h1>
      <p class="text-[10px] text-white/30 tracking-[0.2em] uppercase mt-1">
        Admin System
      </p>
    </div>

    <!-- Profil Mini Pengguna -->
    <div class="px-6 mb-6">
      <div
        class="bg-white/5 p-4 rounded-2xl border border-white/5 flex items-center gap-3"
      >
        <div
          class="w-8 h-8 rounded-full bg-red-600/20 flex items-center justify-center text-red-500 font-bold text-xs font-sora"
        >
          {{ user?.name?.charAt(0)?.toUpperCase() || "?" }}
        </div>
        <div class="min-w-0">
          <p class="text-xs font-semibold text-white/90 truncate">
            {{ user?.name || "Guest" }}
          </p>
          <p
            class="text-[9px] uppercase font-bold tracking-wider opacity-50 font-mono"
            :class="
              userRole === 'owner' ? 'text-amber-500' : 
              userRole === 'admin' ? 'text-blue-400' : 'text-emerald-400'
            "
          >
            {{ userRole || "Kasir" }}
          </p>
        </div>
      </div>
    </div>

    <!-- Navigasi Sidebar Bertingkat (Master & Sub-Master) -->
    <nav class="flex-1 px-4 space-y-3 overflow-y-auto scrollbar-none text-xs uppercase font-sora font-bold tracking-wider">
      
      <!-- MENU UTAMA / DASHBOARD (Selalu Muncul untuk Admin/Owner) -->
      <div v-if="['owner', 'admin'].includes(userRole)" class="space-y-1">
        <router-link
          to="/admin/"
          class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300"
          :class="isActive('/admin/') ? 'bg-white/5 text-white' : 'text-white/40 hover:text-white hover:bg-white/5'"
        >
          <LayoutDashboard size="16" :class="isActive('/admin/') ? 'text-red-500' : 'group-hover:text-white'" />
          <span class="text-sm font-medium normal-case font-inter font-normal tracking-normal">Dashboard Overview</span>
        </router-link>
      </div>

      <!-- KELOMPOK 1: MASTER OPERASIONAL TOKO (Owner, Admin, Kasir) -->
      <div class="space-y-1">
        <button
          type="button"
          @click="toggleGroup('operational')"
          class="group w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-white/[0.03] transition-colors"
        >
          <span class="flex items-center gap-2.5">
            <Zap size="15" class="text-amber-500/70" />
            <span class="text-[13px] font-bold text-zinc-300 tracking-wide normal-case font-inter">Operasional Toko</span>
          </span>
          <ChevronDown
            size="15"
            class="text-zinc-600 transition-transform duration-300 group-hover:text-zinc-400"
            :class="openGroups.operational ? 'rotate-180' : ''"
          />
        </button>
        <div
          class="overflow-hidden transition-all duration-300 ease-in-out"
          :class="openGroups.operational ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'"
        >
          <template v-for="link in operationalLinks" :key="link.to">
            <router-link
              v-if="link.roles.includes(userRole)"
              :to="link.to"
              class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300"
              :class="isActive(link.to) ? 'bg-white/5 text-white' : 'text-white/40 hover:text-white hover:bg-white/5'"
            >
              <component :is="link.icon" size="16" :class="isActive(link.to) ? 'text-red-500' : 'group-hover:text-white'" />
              <span class="text-sm font-medium normal-case font-inter font-normal tracking-normal">{{ link.label }}</span>
            </router-link>
          </template>
        </div>
      </div>

      <!-- KELOMPOK 2: MASTER MANAJEMEN DATA & CMS (Owner, Admin) -->
      <div v-if="['owner', 'admin'].includes(userRole)" class="space-y-1">
        <button
          type="button"
          @click="toggleGroup('dataManagement')"
          class="group w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-white/[0.03] transition-colors"
        >
          <span class="flex items-center gap-2.5">
            <FolderOpen size="15" class="text-sky-500/70" />
            <span class="text-[13px] font-bold text-zinc-300 tracking-wide normal-case font-inter">Data &amp; Konten CMS</span>
          </span>
          <ChevronDown
            size="15"
            class="text-zinc-600 transition-transform duration-300 group-hover:text-zinc-400"
            :class="openGroups.dataManagement ? 'rotate-180' : ''"
          />
        </button>
        <div
          class="overflow-hidden transition-all duration-300 ease-in-out"
          :class="openGroups.dataManagement ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'"
        >
          <template v-for="link in dataManagementLinks" :key="link.to">
            <router-link
              :to="link.to"
              class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300"
              :class="isActive(link.to) ? 'bg-white/5 text-white' : 'text-white/40 hover:text-white hover:bg-white/5'"
            >
              <component :is="link.icon" size="16" :class="isActive(link.to) ? 'text-red-500' : 'group-hover:text-white'" />
              <span class="text-sm font-medium normal-case font-inter font-normal tracking-normal">{{ link.label }}</span>
            </router-link>
          </template>
        </div>
      </div>

      <!-- KELOMPOK 3: MASTER PENGATURAN INTERNAL (Owner Khusus) -->
      <div v-if="userRole === 'owner'" class="space-y-1">
        <button
          type="button"
          @click="toggleGroup('internal')"
          class="group w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-white/[0.03] transition-colors"
        >
          <span class="flex items-center gap-2.5">
            <ShieldCheck size="15" class="text-red-500/70" />
            <span class="text-[13px] font-bold text-zinc-300 tracking-wide normal-case font-inter">Otoritas Internal</span>
          </span>
          <ChevronDown
            size="15"
            class="text-zinc-600 transition-transform duration-300 group-hover:text-zinc-400"
            :class="openGroups.internal ? 'rotate-180' : ''"
          />
        </button>
        <div
          class="overflow-hidden transition-all duration-300 ease-in-out"
          :class="openGroups.internal ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'"
        >
          <template v-for="link in internalLinks" :key="link.to">
            <router-link
              :to="link.to"
              class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300"
              :class="isActive(link.to) ? 'bg-white/5 text-white' : 'text-white/40 hover:text-white hover:bg-white/5'"
            >
              <component :is="link.icon" size="16" :class="isActive(link.to) ? 'text-red-500' : 'group-hover:text-white'" />
              <span class="text-sm font-medium normal-case font-inter font-normal tracking-normal">{{ link.label }}</span>
            </router-link>
          </template>
        </div>
      </div>

      <!-- KELOMPOK PENGGUNA UMUM (Semua Role) -->
      <div class="space-y-1 pt-2 border-t border-white/5">
        <router-link
          to="/admin/profile"
          class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300"
          :class="isActive('/admin/profile') ? 'bg-white/5 text-white' : 'text-white/40 hover:text-white hover:bg-white/5'"
        >
          <UserCheck size="16" :class="isActive('/admin/profile') ? 'text-red-500' : 'group-hover:text-white'" />
          <span class="text-sm font-medium normal-case font-inter font-normal tracking-normal">Profil Saya</span>
        </router-link>
      </div>

    </nav>

    <!-- Footer Tombol Keluar -->
    <div class="p-6 border-t border-white/5">
      <button
        @click="handleLogout"
        class="flex items-center gap-3 w-full px-4 py-3 text-white/30 hover:text-red-400 transition-all text-sm font-medium cursor-pointer"
      >
        <LogOut size="16" /> Keluar
      </button>
    </div>
  </aside>
</template>

<script setup>
import {
  LayoutDashboard,
  Users,
  Clock,
  Settings,
  LogOut,
  ShoppingCart,
  ChefHat,
  BarChart3,
  Wallet,
  UserPlus,
  UserCheck,
  Edit3, // Di-import dengan benar untuk edit-homepage
  ChevronDown, // Ikon indikator dropdown
  Zap, // Ikon header grup Operasional Toko
  FolderOpen, // Ikon header grup Data & Konten CMS
  ShieldCheck // Ikon header grup Otoritas Internal
} from "lucide-vue-next";
import { useAuthStore } from "@/stores/auth";
import { useRoute } from "vue-router";
import { computed, reactive, watch } from "vue";

const auth = useAuthStore();
const route = useRoute();

const user = computed(() => auth.user);
const userRole = computed(() => auth.user?.role?.toLowerCase() || 'kasir');

const isActive = (path) => route.path === path;
const handleLogout = () => auth.logout();

// ⚡ 1. Matriks Operasional Harian Kedai
const operationalLinks = [
  { to: "/admin/pos", icon: ShoppingCart, label: "New Order (POS)", roles: ["owner", "admin", "kasir"] },
  { to: "/admin/orders", icon: Clock, label: "Active Orders", roles: ["owner", "admin", "kasir"] },
];

// 📁 2. Matriks Manajemen Data Pelanggan & Konten CMS Website
const dataManagementLinks = [
  { to: "/admin/menus", icon: ChefHat, label: "Manage Menus" },
  { to: "/admin/reports", icon: BarChart3, label: "Menu Reports" },
  { to: "/admin/edit-homepage", icon: Edit3, label: "Edit Homepage Content" },
  { to: "/admin/customers", icon: Users, label: "Loyal Customers List" },
];

// ⚙️ 3. Matriks Otoritas Sensitif Internal Toko (Murni Owner Only)
const internalLinks = [
  { to: "/admin/finance", icon: Wallet, label: "Buku Kas & Keuangan" },
  { to: "/admin/registerinternal", icon: UserPlus, label: "Register Staff Baru" },
  { to: "/admin/settings", icon: Settings, label: "System Settings" },
];

// State buka/tutup tiap grup dropdown.
// Grup yang berisi link aktif saat ini otomatis terbuka di awal.
const allLinks = [
  ...operationalLinks.map((l) => ({ ...l, group: "operational" })),
  ...dataManagementLinks.map((l) => ({ ...l, group: "dataManagement" })),
  ...internalLinks.map((l) => ({ ...l, group: "internal" })),
];

const findActiveGroup = (path) => allLinks.find((l) => l.to === path)?.group;

const openGroups = reactive({
  operational: true, // default terbuka karena dipakai tiap hari (POS, Orders)
  dataManagement: findActiveGroup(route.path) === "dataManagement",
  internal: findActiveGroup(route.path) === "internal",
});

const toggleGroup = (key) => {
  openGroups[key] = !openGroups[key];
};

// Saat pindah halaman, auto-expand grup yang berisi halaman aktif
watch(
  () => route.path,
  (newPath) => {
    const group = findActiveGroup(newPath);
    if (group) openGroups[group] = true;
  }
);
</script>

<style scoped>
.scrollbar-none::-webkit-scrollbar { display: none; }
.scrollbar-none { -ms-overflow-style: none; scrollbar-width: none; }
</style>