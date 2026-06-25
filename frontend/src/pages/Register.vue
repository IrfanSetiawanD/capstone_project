<template>
  <div class="p-4 sm:p-8 text-white max-w-2xl mx-auto w-full box-border">
    
    <div class="mb-8">
      <h1 class="font-oswald text-3xl sm:text-4xl uppercase tracking-tighter text-white">
        Register Staff Internal
      </h1>
      <p class="text-white/40 text-sm">Daftarkan akun karyawan baru (Admin/Kasir) untuk operasional Masashimura</p>
    </div>

    <div class="bg-[#0a0a0a] border border-white/5 rounded-3xl p-6 sm:p-8 shadow-2xl">
      <form @submit.prevent="handleInternalRegister" class="space-y-6">
        
        <div class="space-y-2">
          <label class="block text-[10px] uppercase tracking-widest font-bold text-white/70">Nama Lengkap Karyawan</label>
          <input
            v-model="formData.name"
            type="text"
            required
            :disabled="loading"
            class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-primary transition-all placeholder-white/20 disabled:opacity-50 text-sm"
            placeholder="Masukkan nama lengkap staff..."
          />
        </div>

        <div class="space-y-2">
          <label class="block text-[10px] uppercase tracking-widest font-bold text-white/70">Alamat Email Login</label>
          <input
            v-model="formData.email"
            type="email"
            required
            :disabled="loading"
            class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-primary transition-all placeholder-white/20 disabled:opacity-50 text-sm font-mono"
            placeholder="contoh: kasir.masashimura@id"
          />
        </div>

        <div class="space-y-2">
          <label class="block text-[10px] uppercase tracking-widest font-bold text-white/70">Role / Hak Akses Sistem</label>
          <select
            v-model="formData.role"
            required
            :disabled="loading"
            class="w-full bg-[#111] border border-white/10 text-white rounded-xl h-12 px-4 outline-none focus:border-primary transition-all disabled:opacity-50 text-sm"
          >
            <option value="kasir">🍳 Kasir / Staff Outlet Lapangan</option>
            <option value="admin">🛠️ Admin / Manajer Operasional</option>
          </select>
        </div>

        <div class="space-y-2">
          <label class="block text-[10px] uppercase tracking-widest font-bold text-white/70">Password Akun</label>
          <div class="relative">
            <input
              v-model="formData.password"
              :type="showPassword ? 'text' : 'password'"
              required
              :disabled="loading"
              class="w-full bg-white/5 border border-white/10 text-white rounded-xl h-12 pl-4 pr-12 outline-none focus:border-primary transition-all placeholder-white/20 disabled:opacity-50 text-sm font-mono"
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
          class="w-full bg-primary hover:bg-red-500 text-white font-oswald uppercase tracking-widest h-14 rounded-xl font-bold transition-all flex justify-center items-center gap-2 cursor-pointer disabled:cursor-not-allowed shadow-[0_4px_20px_rgba(220,38,38,0.15)] text-sm"
        >
          <span
            v-if="loading"
            class="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full"
          />
          {{ loading ? "MENDAFTARKAN STAFF..." : "BUAT AKUN KARYAWAN" }}
        </button>
      </form>
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { toast } from "vue-sonner";
import { Eye, EyeOff } from "lucide-vue-next";
import axios from "axios"; // Gunakan axios langsung agar konsisten dengan bypass backend kita

const loading = ref(false);
const showPassword = ref(false);

const formData = ref({
  name: "",
  email: "",
  password: "",
  role: "kasir", // Default role karyawan baru adalah kasir
});

// 🔥 KUNCI UTAMA: Alur Register Internal tanpa terpental log-out
const handleInternalRegister = async () => {
  loading.value = true;
  try {
    const payload = {
      username: formData.value.email, 
      email: formData.value.email,
      password: formData.value.password,
      full_name: formData.value.name,
      role: formData.value.role, // Payload role sukses dikirim ke Django backend
    };

    // Tembak endpoint register bawaan DB lokal Django lo
    await axios.post("http://127.0.0.1:8000/api/auth/register-internal/", payload);

    toast.success(`Akun ${formData.value.role.toUpperCase()} baru berhasil didaftarkan!`);
    
    // Reset Form murni agar Owner bisa langsung daftarin karyawan berikutnya tanpa mental ke login
    formData.value.name = "";
    formData.value.email = "";
    formData.value.password = "";
    formData.value.role = "kasir";
  } catch (error) {
    console.error("Internal Register Error:", error);
    toast.error(
      error.response?.data?.message || "Gagal mendaftarkan staff. Periksa koneksi backend."
    );
  } finally {
    loading.value = false;
  }
};
</script>