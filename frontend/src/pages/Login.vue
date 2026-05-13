<template>
  <div class="min-h-screen flex bg-[#050505]">
    <!-- Left Side - Hero -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <div
        class="absolute inset-0 bg-cover bg-center"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div class="absolute inset-0 bg-gradient-to-br from-red-600/80 to-black/90" />
      <div class="relative z-10 flex flex-col justify-center px-12 text-white text-center">
        <img src="@/assets/masashimura-logo.png" alt="Masashimura" class="w-[32rem] mx-auto mb-6" />
        <p class="text-xl text-white/90">Sistem Manajemen Admin Masashimura</p>
      </div>
    </div>

    <!-- Right Side - Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-md">
        <div class="mb-8">
          <h2 class="font-oswald text-4xl font-bold text-white mb-2">ADMIN LOGIN</h2>
          <p class="text-white/70">Masuk ke dashboard admin Masashimura</p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-white/90 mb-2">Username / Email</label>
            <input
              v-model="formData.username"
              type="text"
              required
              class="w-full bg-white/5 border border-white/10 text-white rounded-md h-12 px-4 outline-none focus:border-red-500"
              placeholder="owner atau email"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white/90 mb-2">Password</label>
            <div class="relative">
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full bg-white/5 border border-white/10 text-white rounded-md h-12 px-4 outline-none focus:border-red-500"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-white/50"
              >
                <component :is="showPassword ? EyeOff : Eye" size="20" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-red-600 hover:bg-red-500 text-white font-oswald uppercase py-3.5 rounded-sm transition-all disabled:opacity-50"
          >
            {{ loading ? 'MEMPROSES...' : 'MASUK KE DASHBOARD' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast } from 'vue-sonner'
import { Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const showPassword = ref(false)
const loading = ref(false)

const formData = ref({
  username: '',
  password: ''
})

const heroImage = 'https://images.unsplash.com/photo-1759922221495-78755ac90d70?crop=entropy&cs=srgb&fm=jpg&q=85'

const handleSubmit = async () => {
  loading.value = true

  try {
    await auth.login({
      username: formData.value.username,
      password: formData.value.password
    })

    toast.success(`Selamat datang, ${auth.user?.name}!`)

    await nextTick()
    const redirect = route.query.redirect || '/admin'

    // Redirect paling kuat
    await router.replace(redirect)

    // Fallback super kuat
    setTimeout(() => {
      if (window.location.pathname !== redirect) {
        window.location.href = redirect
      }
    }, 800)

  } catch (error) {
    toast.error(error.response?.data?.detail || "Login gagal")
  } finally {
    loading.value = false
  }
}
</script>