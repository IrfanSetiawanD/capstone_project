<template>
  <nav
    v-if="!isAdminRoute"
    :class="[
      'fixed top-0 w-full z-50 transition-all duration-300',
      isScrolled || isOpen
        ? 'bg-[#050505]/95 backdrop-blur-md border-b border-white/10 py-3'
        : 'bg-transparent py-5',
    ]"
  >
    <div
      class="max-w-7xl mx-auto px-6 md:px-12 flex justify-between items-center"
    >
      <router-link to="/" class="flex items-center group" @click="isOpen = false">
        <img
          src="@/assets/masashimura-logo.png"
          alt="Logo Masashimura"
          class="transition-all duration-300 object-contain w-[140px] md:w-[180px]"
        />
      </router-link>

      <div
        class="hidden md:flex items-center space-x-8 text-sm font-medium tracking-widest uppercase font-oswald"
      >
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="text-white/80 hover:text-red-500 transition-colors"
        >
          {{ link.name }}
        </router-link>
      </div>

      <button
        class="md:hidden text-white p-2 cursor-pointer"
        @click="isOpen = !isOpen"
        aria-label="Toggle menu"
      >
        <component :is="isOpen ? X : MenuIcon" size="24" />
      </button>
    </div>

    <div
      v-if="isOpen"
      class="md:hidden bg-[#050505] border-b border-white/10 px-6 py-8 space-y-6 absolute w-full shadow-2xl transition-all duration-300"
    >
      <router-link
        v-for="link in navLinks"
        :key="link.path"
        :to="link.path"
        class="block text-xl font-medium text-white hover:text-red-500"
        @click="isOpen = false"
      >
        {{ link.name }}
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { Menu as MenuIcon, X } from "lucide-vue-next";

const route = useRoute();

const isOpen = ref(false);
const isScrolled = ref(false);

const isAdminRoute = computed(() => route.path.startsWith("/admin"));

const navLinks = [
  { name: "Home", path: "/" },
  { name: "Menu", path: "/menu" },
  { name: "Kontak", path: "/contact" },
];

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

// Pasang scroll listener pasif agar scrolling halaman depan kedai terasa super smooth di HP
onMounted(() => window.addEventListener("scroll", handleScroll, { passive: true }));
onUnmounted(() => window.removeEventListener("scroll", handleScroll));
</script>