<template>
  <div class="min-h-screen flex">
    <!-- Left Side - Image -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <div
        class="absolute inset-0 bg-cover bg-center"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div class="absolute inset-0 bg-gradient-to-br from-primary/80 to-background/90" />
      
      <div class="relative z-10 flex flex-col justify-center px-12 text-white">
        <img
          src="@/assets/masashimura-logo.png"
          alt="Masashimura"
          class="w-[18rem] md:w-[26rem] lg:w-[32rem] mx-auto select-none mb-6"
        />
        <p class="text-xl text-white/90 text-center">
          Daftar akun admin Masashimura
        </p>
      </div>
    </div>

    <!-- Right Side - Register Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-md">
        <div class="mb-8">
          <h2 class="font-oswald text-4xl font-bold text-white mb-2">REGISTER</h2>
          <p class="text-white/70">Buat akun admin baru</p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-white/90 mb-2">Nama Lengkap</label>
            <input
              v-model="formData.name"
              type="text"
              required
              class="w-full bg-black/20 border border-white/10 focus:border-primary/50 text-white placeholder:text-white/30 rounded-md h-12 px-4 outline-none"
              placeholder="Nama Admin"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white/90 mb-2">Email</label>
            <input
              v-model="formData.email"
              type="email"
              required
              class="w-full bg-black/20 border border-white/10 focus:border-primary/50 text-white placeholder:text-white/30 rounded-md h-12 px-4 outline-none"
              placeholder="admin@masashimura.id"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white/90 mb-2">Password</label>
            <input
              v-model="formData.password"
              type="password"
              required
              class="w-full bg-black/20 border border-white/10 focus:border-primary/50 text-white placeholder:text-white/30 rounded-md h-12 px-4 outline-none"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-primary text-white hover:bg-primary/90 font-oswald uppercase tracking-wider py-3 rounded-sm shadow-neo-yellow hover:translate-y-[2px] hover:shadow-neo-yellow-hover transition-all disabled:opacity-50"
          >
            {{ loading ? 'Mendaftar...' : 'Daftar' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-white/70">
            Sudah punya akun? 
            <router-link to="/login" class="text-accent hover:text-accent/80 font-medium">
              Login di sini
            </router-link>
          </p>
        </div>

        <div class="mt-4 text-center">
          <router-link to="/" class="text-sm text-white/50 hover:text-white/80">
            ← Kembali ke Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()

const formData = ref({
  name: '',
  email: '',
  password: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true

  try {
    // TODO: Ganti dengan API register kamu nanti
    console.log('Register data:', formData.value)
    
    toast.success('Akun admin berhasil dibuat!')
    router.push('/login')   // setelah register, arahkan ke login
  } catch (error) {
    toast.error('Gagal mendaftar. Silakan coba lagi.')
  } finally {
    loading.value = false
  }
}

const heroImage = 'https://images.unsplash.com/photo-1759922221495-78755ac90d70?crop=entropy&cs=srgb&fm=jpg&q=85'
</script>