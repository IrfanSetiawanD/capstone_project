<template>
  <div class="max-w-4xl mx-auto p-4">
    <div class="mb-12">
      <h1 class="font-oswald text-5xl uppercase italic tracking-tighter">
        System Settings
      </h1>
      <p class="text-white/40 text-sm font-light">
        Konfigurasi variabel bisnis Masashimura
      </p>
    </div>

    <div class="space-y-8">
      <div
        class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-8 transition-all duration-300"
      >
        <h2
          class="font-oswald text-xl uppercase tracking-wider mb-6 text-red-500 flex items-center gap-2"
        >
          <Star size="20" /> Aturan Loyalitas
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <label
              class="block text-[10px] uppercase text-white/40 mb-3 tracking-widest"
              >Min. Pesanan (Bulan)</label
            >
            <input
              v-model="settings.min_orders"
              type="number"
              class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 focus:border-red-600 outline-none transition-all text-white"
            />
          </div>
          <div>
            <label
              class="block text-[10px] uppercase text-white/40 mb-3 tracking-widest"
              >Persentase Diskon (%)</label
            >
            <input
              v-model="settings.discount_percent"
              type="number"
              class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 focus:border-red-600 outline-none transition-all text-white"
            />
          </div>
        </div>
      </div>

      <div
        class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-8 transition-all duration-300"
      >
        <h2
          class="font-oswald text-xl uppercase tracking-wider mb-6 text-red-500 flex items-center gap-2"
        >
          <Phone size="20" /> Jalur Pesanan (WhatsApp)
        </h2>
        <div>
          <label
            class="block text-[10px] uppercase text-white/40 mb-3 tracking-widest"
            >Nomor WA Admin</label
          >
          <input
            v-model="settings.admin_whatsapp"
            type="text"
            class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 focus:border-red-600 outline-none transition-all text-white"
            placeholder="628..."
          />
          <p class="text-[10px] text-white/20 mt-3 italic">
            *Gunakan format 62 (tanpa + atau 0)
          </p>
        </div>
      </div>

      <div class="flex justify-end pt-4">
        <button
          @click="saveSettings"
          :disabled="isSaving"
          class="bg-red-600 text-white font-oswald uppercase px-12 py-4 rounded-xl shadow-xl hover:bg-red-500 transition-all tracking-[0.2em] font-bold text-sm disabled:opacity-50"
        >
          {{ isSaving ? "Menyimpan..." : "Simpan Perubahan" }}
        </button>
      </div>
    </div>

    <div
      v-if="auth.user?.role === 'owner'"
      class="mt-12 pt-8 border-t border-white/10"
    >
      <button
        @click="showCreateModal = true"
        class="bg-white/5 hover:bg-white/10 px-8 py-4 rounded-2xl flex items-center gap-3 text-lg font-medium transition-all border border-dashed border-white/10"
      >
        <span class="text-2xl text-red-500">+</span> Buat Akun Baru (Admin /
        Owner)
      </button>
    </div>

    <CreateUserModal
      v-model:open="showCreateModal"
      @created="handleUserCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import CreateUserModal from "@/components/CreateUserModal.vue";
import { Star, Phone } from "lucide-vue-next";
import { toast } from "vue-sonner";
// import { settingsAPI } from "@/api"; // Import API Anda di sini

const auth = useAuthStore();
const showCreateModal = ref(false);
const isSaving = ref(false);

const settings = ref({
  min_orders: 0,
  discount_percent: 0,
  admin_whatsapp: "",
});

const fetchSettings = async () => {
  // Tambahkan logic fetch data dari API
  // const res = await settingsAPI.get();
  // settings.value = res.data;
};

const saveSettings = async () => {
  isSaving.value = true;
  try {
    // await settingsAPI.update(settings.value);
    toast.success("Konfigurasi sistem berhasil diperbarui!");
  } catch (err) {
    toast.error("Gagal memperbarui konfigurasi");
  } finally {
    isSaving.value = false;
  }
};

const handleUserCreated = () => {
  toast.success("Akun baru berhasil dibuat!");
};

onMounted(fetchSettings);
</script>
