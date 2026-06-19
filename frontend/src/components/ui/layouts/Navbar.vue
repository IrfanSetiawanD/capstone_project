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
      <router-link to="/" class="flex items-center group">
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

        <div class="flex items-center gap-6 border-l border-white/10 pl-6">
          <template v-if="user">
            <span class="text-white/80 text-xs font-light">{{
              user.email
            }}</span>
            <button
              @click="handleLogout"
              class="text-red-400 hover:text-red-500 transition-colors"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="bg-red-600 text-black font-bold px-6 py-2 rounded-full hover:bg-white hover:text-black transition-colors"
            >
              Login
            </router-link>
          </template>
        </div>
      </div>

      <button
        class="md:hidden text-white p-2"
        @click="isOpen = !isOpen"
        aria-label="Toggle menu"
      >
        <component :is="isOpen ? X : MenuIcon" size="24" />
      </button>
    </div>

    <div
      v-if="isOpen"
      class="md:hidden bg-[#050505] border-b border-white/10 px-6 py-8 space-y-6 absolute w-full shadow-2xl"
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

      <div class="pt-4 border-t border-white/10">
        <button
          v-if="user"
          @click="handleLogout"
          class="text-red-400 font-bold text-lg"
        >
          Logout
        </button>
        <router-link
          v-else
          to="/login"
          class="block text-xl text-white"
          @click="isOpen = false"
          >Login</router-link
        >
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { Menu as MenuIcon, X } from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const isOpen = ref(false);
const isScrolled = ref(false);

const user = computed(() => auth.user);
const isAdminRoute = computed(() => route.path.startsWith("/admin"));

const navLinks = [
  { name: "Home", path: "/" },
  { name: "Menu", path: "/menu" },
  { name: "Kontak", path: "/contact" },
];

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

onMounted(() => window.addEventListener("scroll", handleScroll));
onUnmounted(() => window.removeEventListener("scroll", handleScroll));

const handleLogout = () => {
  auth.logout();
  router.push("/");
  isOpen.value = false;
};
</script>
