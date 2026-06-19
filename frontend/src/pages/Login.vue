<template>
  <div class="min-h-screen flex bg-[#050505] font-manrope">
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <div
        class="absolute inset-0 bg-cover bg-center transition-all duration-700 hover:scale-105"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div
        class="absolute inset-0 bg-gradient-to-br from-red-900/90 to-black/95"
      />
      <div
        class="relative z-10 flex flex-col justify-center items-center px-12 text-white text-center"
      >
        <img
          src="@/assets/masashimura-logo.png"
          alt="Masashimura"
          class="w-80 mx-auto mb-8 drop-shadow-2xl"
        />
        <div class="space-y-2">
          <h2 class="font-oswald text-3xl uppercase tracking-widest">
            Admin Portal
          </h2>
          <p class="text-white/60 font-light">
            Sistem Manajemen Bisnis Masashimura Bekasi
          </p>
        </div>
      </div>
    </div>

    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-sm">
        <div class="mb-10">
          <h2
            class="font-oswald text-4xl font-bold text-white mb-2 uppercase tracking-tight"
          >
            Login
          </h2>
          <p class="text-white/50">
            Masukkan kredensial untuk mengakses sistem
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label
              class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-bold"
              >Username</label
            >
            <input
              v-model="formData.username"
              type="text"
              required
              autocomplete="username"
              class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-red-600 focus:bg-white/10 transition-all"
              placeholder="Username admin"
            />
          </div>

          <div>
            <label
              class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-bold"
              >Password</label
            >
            <div class="relative">
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-red-600 focus:bg-white/10 transition-all"
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
            class="w-full bg-red-600 hover:bg-red-700 text-white font-oswald uppercase py-4 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed tracking-widest font-bold mt-4"
          >
            {{ loading ? "MEMPROSES..." : "MASUK KE SISTEM" }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { toast } from "vue-sonner";
import { Eye, EyeOff } from "lucide-vue-next";

const router = useRouter();
const auth = useAuthStore();

const showPassword = ref(false);
const loading = ref(false);
const formData = ref({ username: "", password: "" });

const heroImage =
  "https://images.unsplash.com/photo-1759922221495-78755ac90d70?q=80&w=2070";

const handleSubmit = async () => {
  loading.value = true;

  try {
    await auth.login({
      username: formData.value.username.trim(),
      password: formData.value.password,
    });

    toast.success(`Selamat datang kembali, ${auth.user?.name || "Admin"}!`);

    // Redirect logic
    if (auth.isOwner || auth.isAdmin) {
      router.push("/admin");
    } else if (auth.isKasir) {
      router.push("/admin/orders");
    } else {
      router.push("/");
    }
  } catch (error) {
    toast.error(
      error.response?.data?.detail ||
        "Login gagal, silakan periksa kredensial Anda.",
    );
  } finally {
    loading.value = false;
  }
};
</script>
