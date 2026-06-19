<template>
  <aside
    class="sticky top-0 h-screen w-64 bg-[#0a0a0a] border-r border-white/5 flex flex-col shrink-0 text-white"
  >
    <div class="p-8">
      <h1 class="font-oswald text-2xl font-bold tracking-tight text-white">
        MASASHIMURA
      </h1>
      <p class="text-[10px] text-white/30 tracking-[0.2em] uppercase mt-1">
        Admin System
      </p>
    </div>

    <div class="px-6 mb-6">
      <div
        class="bg-white/5 p-4 rounded-2xl border border-white/5 flex items-center gap-3"
      >
        <div
          class="w-8 h-8 rounded-full bg-red-600/20 flex items-center justify-center text-red-500 font-bold text-xs"
        >
          {{ user?.name?.charAt(0)?.toUpperCase() || "?" }}
        </div>
        <div class="min-w-0">
          <p class="text-xs font-semibold text-white/90 truncate">
            {{ user?.name || "Guest" }}
          </p>
          <p
            class="text-[9px] uppercase font-bold tracking-wider opacity-50"
            :class="isOwner ? 'text-amber-500' : 'text-blue-400'"
          >
            {{ user?.role || "Staff" }}
          </p>
        </div>
      </div>
    </div>

    <nav class="flex-1 px-4 space-y-1 overflow-y-auto">
      <template v-for="link in navLinks" :key="link.to">
        <router-link
          v-if="!link.adminOnly || isOwner"
          :to="link.to"
          class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300"
          :class="
            isActive(link.to)
              ? 'bg-white/5 text-white'
              : 'text-white/40 hover:text-white hover:bg-white/5'
          "
        >
          <component
            :is="link.icon"
            size="18"
            :class="
              isActive(link.to) ? 'text-red-500' : 'group-hover:text-white'
            "
          />
          <span class="text-sm font-medium">{{ link.label }}</span>
        </router-link>
      </template>
    </nav>

    <div class="p-6 border-t border-white/5">
      <button
        @click="handleLogout"
        class="flex items-center gap-3 w-full px-4 py-3 text-white/30 hover:text-red-400 transition-all text-sm font-medium"
      >
        <LogOut size="18" /> Keluar
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
} from "lucide-vue-next";
import { useAuthStore } from "@/stores/auth";
import { useRoute } from "vue-router";
import { computed } from "vue";

const auth = useAuthStore();
const route = useRoute();

const user = computed(() => auth.user);
const isOwner = computed(() => auth.role === "owner");

const isActive = (path) => route.path === path;
const handleLogout = () => auth.logout();

const navLinks = [
  { to: "/admin", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/admin/orders", icon: Clock, label: "Active Orders" },
  { to: "/admin/pos", icon: ShoppingCart, label: "New Order" },
  { to: "/admin/menus", icon: ChefHat, label: "Manage Menus" },
  { to: "/admin/reports", icon: BarChart3, label: "Menu Reports" },
  { to: "/admin/customers", icon: Users, label: "Loyal Customers" },
  { to: "/admin/settings", icon: Settings, label: "Settings", adminOnly: true },
];
</script>
