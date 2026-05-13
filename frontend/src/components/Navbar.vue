<template>
  <!-- Navbar hanya muncul jika BUKAN halaman Admin Login -->
  <nav 
    v-if="!isAdminRoute"
    :class="[
      'fixed top-0 w-full z-50 transition-all duration-300',
      isScrolled 
        ? 'bg-[#0F172A]/80 backdrop-blur-md border-b border-white/10 py-3' 
        : 'bg-transparent py-5'
    ]"
  >
    <div class="max-w-7xl mx-auto px-6 md:px-12 flex justify-between items-center">
      <!-- Logo -->
      <router-link to="/" class="flex items-center group">
        <img 
          src="@/assets/masashimura-logo.png" 
          alt="Logo Masashimura"
          :class="[
            'transition-all duration-300 object-contain',
            isScrolled ? 'w-[150px]' : 'w-[180px]'
          ]"
        />
      </router-link>

      <!-- Desktop Menu -->
      <div class="hidden md:flex items-center space-x-8 text-sm font-medium tracking-widest uppercase">
        <router-link 
          v-for="link in navLinks" 
          :key="link.path"
          :to="link.path"
          class="text-white/80 hover:text-primary transition-colors"
        >
          {{ link.name }}
        </router-link>

        <!-- Auth Section -->
        <div class="flex items-center gap-6 border-l border-white/10 pl-6">
          <template v-if="user">
            <span class="text-white/80 text-sm">{{ user.email }}</span>
            <button 
              @click="handleLogout"
              class="text-red-400 hover:text-red-500 font-medium transition-colors"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <router-link 
              to="/login" 
              class="bg-primary text-[#0F172A] font-bold px-6 py-2 rounded-full hover:bg-white transition-colors"
            >
              Login
            </router-link>
          </template>
        </div>
      </div>

      <!-- Mobile Menu Button -->
      <button class="md:hidden text-white" @click="isOpen = !isOpen">
        <component :is="isOpen ? X : MenuIcon" size="24" />
      </button>
    </div>

    <!-- Mobile Menu -->
    <div v-if="isOpen" class="md:hidden bg-[#0F172A] border-b border-white/10 px-6 py-8 space-y-6">
      <!-- Nav Links Mobile -->
      <router-link 
        v-for="link in navLinks" 
        :key="link.path"
        :to="link.path"
        class="block text-xl font-medium text-white"
        @click="isOpen = false"
      >
        {{ link.name }}
      </router-link>

      <!-- Auth Mobile -->
      <div class="pt-4 border-t border-white/10">
        <template v-if="user">
          <button @click="handleLogoutMobile" class="text-red-400 font-bold text-lg">
            Logout
          </button>
        </template>
        <template v-else>
          <router-link 
            to="/login" 
            class="block text-xl text-white"
            @click="isOpen = false"
          >
            Login
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Menu as MenuIcon, X } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isOpen = ref(false)
const isScrolled = ref(false)

const user = computed(() => auth.user)

const isAdminRoute = computed(() => {
  return route.path.startsWith('/admin')
})

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Menu', path: '/menu' },
  { name: 'Kontak', path: '/contact' },
]

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleLogout = () => {
  auth.logout()
  router.push('/')
}

const handleLogoutMobile = () => {
  handleLogout()
  isOpen.value = false
}
</script>