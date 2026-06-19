<template>
  <div class="min-h-screen flex bg-[#050505] font-manrope">
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <div
        class="absolute inset-0 bg-cover bg-center transition-transform duration-700 hover:scale-105"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div
        class="absolute inset-0 bg-gradient-to-br from-primary/80 to-black/95"
      />
      <div
        class="relative z-10 flex flex-col justify-center px-12 text-white w-full text-center"
      >
        <img
          src="@/assets/masashimura-logo.png"
          alt="Masashimura"
          class="w-[28rem] mx-auto select-none mb-6"
        />
        <p
          class="text-xl text-white/80 font-light tracking-wide uppercase font-oswald"
        >
          Sistem Manajemen Admin Masashimura
        </p>
      </div>
    </div>

    <div
      class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12 relative z-10"
    >
      <div
        class="w-full max-w-md bg-[#0a0a0a] lg:bg-transparent border border-white/5 lg:border-none p-8 lg:p-0 rounded-2xl shadow-2xl lg:shadow-none"
      >
        <div class="mb-8">
          <h2
            class="font-oswald text-4xl font-bold text-white mb-2 tracking-tight uppercase"
          >
            REGISTER
          </h2>
          <p class="text-white/40 text-sm font-light">
            Buat akun admin baru untuk manajemen sistem
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label
              class="block text-[10px] uppercase tracking-widest font-bold text-white/70 mb-2"
              >Nama Lengkap</label
            >
            <input
              v-model="formData.name"
              type="text"
              required
              :disabled="loading"
              class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-primary transition-all placeholder-white/20 disabled:opacity-50"
              placeholder="Nama Lengkap Admin"
            />
          </div>

          <div>
            <label
              class="block text-[10px] uppercase tracking-widest font-bold text-white/70 mb-2"
              >Email</label
            >
            <input
              v-model="formData.email"
              type="email"
              required
              :disabled="loading"
              class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-primary transition-all placeholder-white/20 disabled:opacity-50"
              placeholder="admin@masashimura.id"
            />
          </div>

          <div>
            <label
              class="block text-[10px] uppercase tracking-widest font-bold text-white/70 mb-2"
              >Password</label
            >
            <div class="relative">
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                :disabled="loading"
                class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 pl-4 pr-12 outline-none focus:border-primary transition-all placeholder-white/20 disabled:opacity-50"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors"
              >
                <component :is="showPassword ? EyeOff : Eye" size="18" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-primary text-white hover:bg-red-500 font-oswald uppercase tracking-widest py-4 rounded-xl font-bold transition-all flex justify-center items-center gap-2 cursor-pointer disabled:cursor-not-allowed shadow-[0_4px_20px_rgba(220,38,38,0.15)]"
          >
            <span
              v-if="loading"
              class="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full"
            />
            {{ loading ? "MENDAFTAR..." : "DAFTAR SEKARANG" }}
          </button>
        </form>

        <div class="mt-8 text-center space-y-3">
          <p class="text-white/40 text-sm font-light">
            Sudah punya akun?
            <router-link
              to="/login"
              class="text-primary hover:text-red-400 font-medium ml-1 transition-colors"
            >
              Login di sini
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { toast } from "vue-sonner";
import { Eye, EyeOff } from "lucide-vue-next";
import { authAPI } from "@/api"; // Pastikan authAPI sudah terkonfigurasi

const router = useRouter();
const loading = ref(false);
const showPassword = ref(false);

const formData = ref({
  name: "",
  email: "",
  password: "",
});

const heroImage =
  "https://images.unsplash.com/photo-1759922221495-78755ac90d70?crop=entropy&cs=srgb&fm=jpg&q=85";

const handleSubmit = async () => {
  loading.value = true;
  try {
    // Memanggil API register yang sudah didefinisikan di src/api/index.js
    await authAPI.register({
      username: formData.value.email, // Django biasanya butuh username/email
      email: formData.value.email,
      password: formData.value.password,
      full_name: formData.value.name,
    });

    toast.success("Akun admin berhasil dibuat!");
    router.push("/login");
  } catch (error) {
    console.error("Register Error:", error);
    toast.error(
      error.response?.data?.message || "Gagal mendaftar. Silakan coba lagi.",
    );
  } finally {
    loading.value = false;
  }
};
</script>
