file sebelumnya dan
<template>
  <div class="min-h-screen flex bg-[#050505] font-manrope selection:bg-red-600/30 selection:text-white">
    
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden border-r border-white/5">
      <div
        class="absolute inset-0 bg-cover bg-center transition-transform duration-1000 hover:scale-105"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-black/20" />
      <div class="absolute inset-0 bg-gradient-to-tr from-red-950/40 via-transparent to-black/50" />
      
      <div class="relative z-10 flex flex-col justify-between p-16 text-white w-full h-full">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold tracking-[0.4em] uppercase text-red-500 font-oswald">Premium Quality</span>
        </div>
        
        <div class="space-y-4 max-w-md">
          <img
            src="@/assets/masashimura-logo.png"
            alt="Masashimura"
            class="w-72 object-contain select-none drop-shadow-[0_10px_30px_rgba(0,0,0,0.8)]"
            onerror="this.style.display='none'"
          />
          <div class="space-y-1">
            <h2 class="font-oswald text-2xl uppercase tracking-widest text-white">Admin ERP System</h2>
            <p class="text-white/50 text-xs font-light leading-relaxed">
              Infrastruktur manajemen internal, rekap finansial, kontrol stok, dan kasir POS terintegrasi Masashimura Bekasi.
            </p>
          </div>
        </div>

        <p class="text-[10px] text-white/20 font-mono">© 2026 Masashimura Corporation. All Rights Reserved.</p>
      </div>
    </div>

    <div class="w-full lg:w-1/2 flex items-center justify-center px-6 py-12 relative z-10 bg-gradient-to-b from-[#0a0a0a] to-[#050505] lg:from-transparent lg:to-transparent">
      <div class="w-full max-w-sm space-y-8">
        
        <div class="space-y-2">
          <h2 class="font-oswald text-4xl font-bold text-white uppercase tracking-tight">
            SISTEM LOGIN
          </h2>
          <p class="text-white/40 text-xs font-light">
            Masukkan kredensial otorisasi untuk masuk ke dalam ruang kendali sistem.
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div class="space-y-1.5">
            <label class="block text-[10px] uppercase tracking-widest text-white/40 font-bold">Username / ID Karyawan</label>
            <input
              v-model="formData.username"
              type="text"
              required
              autocomplete="username"
              :disabled="loading"
              class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-red-600 focus:bg-white/10 transition-all placeholder-white/10 text-sm font-mono disabled:opacity-50"
              placeholder="Masukkan username anda..."
            />
          </div>

          <div class="space-y-1.5">
            <label class="block text-[10px] uppercase tracking-widest text-white/40 font-bold">Kata Sandi (Password)</label>
            <div class="relative">
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                :disabled="loading"
                class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 pl-4 pr-12 outline-none focus:border-red-600 focus:bg-white/10 transition-all placeholder-white/10 text-sm font-mono disabled:opacity-50"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white transition-colors"
              >
                <component :is="showPassword ? EyeOff : Eye" size="16" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-red-600 hover:bg-red-500 disabled:bg-white/5 disabled:text-white/20 text-white font-oswald uppercase h-13 rounded-xl transition-all tracking-widest font-bold mt-2 text-xs flex justify-center items-center gap-2 cursor-pointer shadow-[0_4px_25px_rgba(220,38,38,0.15)]"
          >
            <span
              v-if="loading"
              class="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full"
            />
            {{ loading ? "MEMPROSES OTENTIKASI..." : "MASUK KE SISTEM" }}
          </button>
        </form>

        <div class="text-center pt-2">
          <button 
            @click="openForgotModal" 
            class="text-xs text-white/30 hover:text-red-400 font-medium transition-colors underline underline-offset-4 cursor-pointer"
          >
            Lupa Password Akun?
          </button>
        </div>

      </div>
    </div>

    <div v-if="isForgotModalOpen" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="bg-[#0f0f0f] border border-white/10 rounded-2xl w-full max-w-md p-6 sm:p-8 space-y-5 shadow-2xl">
        <div class="space-y-1">
          <h3 class="font-oswald text-xl uppercase tracking-wide text-white">Reset Password Mandiri</h3>
          <p class="text-white/40 text-xs leading-relaxed">
            Selagi lo hafal alamat email staff lo yang terdaftar, lo bisa langsung ubah password di bawah ini.
          </p>
        </div>

        <form @submit.prevent="handleSelfResetPassword" class="space-y-4 text-xs">
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Masukkan Email Akun Staff</label>
            <input 
              v-model="resetForm.email"
              type="email"
              required
              placeholder="contoh: kasir@masashimura.id"
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3 px-4 text-sm focus:outline-none focus:border-red-600 font-mono transition text-white"
            />
          </div>

          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Ganti Password Baru</label>
            <div class="relative">
              <input 
                v-model="resetForm.newPassword"
                :type="showResetPassword ? 'text' : 'password'"
                required
                placeholder="Ketik password baru minimal 6 karakter..."
                class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-4 pr-12 text-sm focus:outline-none focus:border-red-600 font-mono transition text-white"
              />
              <button 
                type="button" 
                @click="showResetPassword = !showResetPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white"
              >
                <component :is="showResetPassword ? EyeOff : Eye" size="16" />
              </button>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3 pt-2">
            <button 
              type="submit"
              :disabled="isResetting"
              class="bg-red-600 hover:bg-red-500 disabled:opacity-30 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition font-oswald cursor-pointer"
            >
              {{ isResetting ? 'Mengubah...' : 'Ganti Password' }}
            </button>
            <button 
              type="button"
              @click="isForgotModalOpen = false" 
              class="bg-white/5 hover:bg-white/10 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition font-oswald cursor-pointer"
            >
              Batalkan
            </button>
          </div>
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
import axios from "axios";

const router = useRouter();
const auth = useAuthStore();

const showPassword = ref(false);
const showResetPassword = ref(false);
const loading = ref(false);
const isResetting = ref(false);
const isForgotModalOpen = ref(false);

const formData = ref({ username: "", password: "" });

const resetForm = ref({
  email: "",
  newPassword: ""
});

const heroImage = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=2080";

const openForgotModal = () => {
  resetForm.value.email = "";
  resetForm.value.newPassword = "";
  showResetPassword.value = false;
  isForgotModalOpen.value = true;
};

const handleSubmit = async () => {
  loading.value = true;
  try {
    await auth.login({
      username: formData.value.username.trim(),
      password: formData.value.password,
    });

    toast.success(`Akses diberikan. Selamat datang kembali, ${auth.user?.name || "Admin"}!`);

    if (auth.isOwner || auth.isAdmin) {
      router.push("/admin");
    } else if (auth.isKasir) {
      router.push("/admin/orders");
    } else {
      router.push("/");
    }
  } catch (error) {
    console.error("Login Error:", error);
    toast.error(error.response?.data?.detail || "Email atau Password salah.");
  } finally {
    loading.value = false;
  }
};

// ⚡ EKSEKUSI API RESET PASSWORD INSTAN BERDASARKAN VERIFIKASI EMAIL DI DB Django
const handleSelfResetPassword = async () => {
  if (resetForm.value.newPassword.length < 6) {
    return toast.error("Password baru minimal kudu 6 karakter!");
  }

  isResetting.value = true;
  try {
    const payload = {
      email: resetForm.value.email.trim(),
      new_password: resetForm.value.newPassword
    };

    // Tembak endpoint kustom reset password instan di backend Django
    await axios.post("http://127.0.0.1:8000/api/auth/reset-password-instan/", payload);
    
    toast.success("Password baru berhasil diupdate di database! Silakan login.");
    isForgotModalOpen.value = false;
  } catch (error) {
    console.error("Reset Password Error:", error);
    toast.error(error.response?.data?.message || "Email gak terdaftar atau salah ketik!");
  } finally {
    isResetting.value = false;
  }
};
</script>