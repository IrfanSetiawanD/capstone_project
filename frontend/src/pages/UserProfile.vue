<template>
  <div class="max-w-4xl mx-auto p-4 sm:p-6 text-white box-border space-y-8">
    
    <!-- 👤 HEADER PROFIL -->
    <div class="mb-8">
      <h1 class="font-oswald text-4xl uppercase tracking-tighter text-white">
        My Profile
      </h1>
      <p class="text-white/40 text-sm font-light">
        Kelola kredensial login dan keamanan akun operasional lo
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
      
      <!-- CARD INFORMAI AKUN SAKTI -->
      <div class="md:col-span-1 bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 text-center space-y-4 shadow-xl">
        <div class="w-20 h-20 rounded-full bg-primary/10 border-2 border-primary/20 flex items-center justify-center text-3xl font-bold text-primary mx-auto font-oswald select-none">
          {{ userInitial }}
        </div>
        <div>
          <h3 class="font-bold text-lg text-white/90 truncate">{{ auth.user?.name || 'Staff Masashimura' }}</h3>
          <p class="text-xs text-white/40 font-mono mt-0.5 truncate">{{ auth.user?.email }}</p>
        </div>
        <div class="pt-2 border-t border-white/5">
          <span 
            class="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider font-mono"
            :class="
              userRole === 'owner' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
              userRole === 'admin' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
              'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
            "
          >
            👑 {{ userRole }}
          </span>
        </div>
      </div>

      <!-- FORM UPDATE DATA KREDENSIAL (USERNAME & PASSWORD) -->
      <div class="md:col-span-2 bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 sm:p-8 space-y-6 shadow-2xl">
        <h2 class="font-oswald text-xl uppercase tracking-wider text-red-500 border-b border-white/5 pb-3">
          Update Kredensial Akun
        </h2>

        <form @submit.prevent="handleUpdateProfile" class="space-y-5 text-xs">
          
          <!-- Input Email (Read-Only, tidak bisa diubah) -->
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Alamat Email</label>
            <div class="relative">
              <input 
                :value="auth.user?.email"
                type="email" 
                disabled
                readonly
                class="w-full bg-white/[0.02] border border-white/5 rounded-xl py-3.5 pl-4 pr-12 text-sm font-mono transition text-white/40 cursor-not-allowed"
              />
              <Lock size="14" class="absolute right-4 top-1/2 -translate-y-1/2 text-white/20" />
            </div>
            <p class="text-[10px] text-white/25 italic pt-0.5">
              Email terkunci dan tidak dapat diubah. Hubungi owner jika perlu mengganti email akun lo.
            </p>
          </div>

          <!-- Input Username (Bisa Diubah) -->
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Username</label>
            <input 
              v-model="profileForm.username"
              type="text" 
              required
              :disabled="isSaving"
              placeholder="Masukkan username baru lo..."
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3.5 px-4 text-sm focus:outline-none focus:border-red-600 font-mono transition text-white disabled:opacity-50"
            />
          </div>

          <p class="text-[11px] text-white/30 italic -mt-2">
            *Isi kolom di bawah ini jika lo hanya ingin mengganti password akun operasional.
          </p>

          <!-- Input Password Baru -->
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Password Baru</label>
            <div class="relative">
              <input 
                v-model="profileForm.newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                :disabled="isSaving"
                placeholder="Masukkan password baru jika ingin diganti..."
                class="w-full bg-white/5 border border-white/10 rounded-xl py-3.5 pl-4 pr-12 text-sm focus:outline-none focus:border-red-600 font-mono transition text-white disabled:opacity-50"
              />
              <button 
                type="button"
                @click="showNewPassword = !showNewPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors"
              >
                <component :is="showNewPassword ? EyeOff : Eye" size="16" />
              </button>
            </div>
          </div>

          <!-- Konfirmasi Password Baru -->
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Konfirmasi Password Baru</label>
            <div class="relative">
              <input 
                v-model="profileForm.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                :disabled="isSaving"
                placeholder="Ulangi password baru lo..."
                class="w-full bg-white/5 border border-white/10 rounded-xl py-3.5 pl-4 pr-12 text-sm focus:outline-none focus:border-red-600 font-mono transition text-white disabled:opacity-50"
              />
              <button 
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors"
              >
                <component :is="showConfirmPassword ? EyeOff : Eye" size="16" />
              </button>
            </div>
          </div>

          <!-- Tombol Submit Aksi -->
          <div class="flex justify-end pt-2">
            <button 
              type="submit"
              :disabled="isSaving"
              class="w-full sm:w-fit bg-red-600 hover:bg-red-500 text-white font-oswald uppercase px-8 py-3.5 rounded-xl text-xs font-bold tracking-widest transition disabled:opacity-50 cursor-pointer"
            >
              {{ isSaving ? 'Menyimpan...' : 'Simpan Kredensial Baru' }}
            </button>
          </div>

        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { Eye, EyeOff, Lock } from "lucide-vue-next";
import { toast } from "vue-sonner";
import axios from "axios";

const auth = useAuthStore();
const isSaving = ref(false);

const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

const profileForm = ref({
  username: "",
  newPassword: "",
  confirmPassword: ""
});

const userInitial = computed(() => {
  return auth.user?.name ? auth.user.name.trim().charAt(0).toUpperCase() : "?";
});

const userRole = computed(() => {
  return auth.user?.role?.toLowerCase() || "kasir";
});

// Load data awal username user aktif dari store/state auth bawaan
onMounted(() => {
  if (auth.user?.username) {
    profileForm.value.username = auth.user.username;
  }
});

// Aksi Update Kredensial Pengguna Ke Django DB Lokal
const handleUpdateProfile = async () => {
  // Validasi kecocokan password jika kasir berniat mengganti password
  if (profileForm.value.newPassword) {
    if (profileForm.value.newPassword.length < 6) {
      return toast.error("Password baru minimal harus 6 karakter!");
    }
    if (profileForm.value.newPassword !== profileForm.value.confirmPassword) {
      return toast.error("Konfirmasi password baru tidak cocok, Bal!");
    }
  }

  isSaving.value = true;
  try {
    const payload = {
      username: profileForm.value.username,
    };

    if (profileForm.value.newPassword) {
      payload.password = profileForm.value.newPassword;
    }

    // 1. Ambil token fresh dari localStorage
    const token = localStorage.getItem("token");

    // 2. Tembak endpoint API update profile dengan menyisipkan Authorization Header
    const response = await axios.put(
      "http://127.0.0.1:8000/api/auth/profile/update/", 
      payload,
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    );
    
    toast.success("Kredensial profil lo berhasil diperbarui!");
    
    // 3. 🔥 Sinkronisasi State: Update data di Pinia Store & localStorage biar live-sync
    if (response.data && response.data.user) {
      const updatedUser = {
        ...auth.user, // pertahankan token dan role lama yang sudah di-map
        username: response.data.user.username,
        name: response.data.user.name,
        email: response.data.user.email
      };
      
      auth.user = updatedUser;
      localStorage.setItem("user", JSON.stringify(updatedUser));
    }
    
    // Bersihkan form password setelah mutasi data di DB sukses
    profileForm.value.newPassword = "";
    profileForm.value.confirmPassword = "";
  } catch (error) {
    print(error);
    toast.error(
      error.response?.data?.username?.[0] || 
      error.response?.data?.non_field_errors?.[0] || 
      "Gagal memperbarui profil ke database."
    );
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
/* Pastikan input numeric apa pun bersih tanpa spin button */
.no-spinner::-webkit-outer-spin-button,
.no-spinner::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.no-spinner {
  -moz-appearance: textfield;
}
</style>