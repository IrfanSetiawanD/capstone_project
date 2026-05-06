<template>
  <div class="flex min-h-screen bg-[#050505] text-white">
    <AdminSidebar />

    <main class="flex-1 ml-64 p-8 md:p-12 font-manrope overflow-x-hidden">
      <div class="max-w-4xl mx-auto">
        
        <div class="mb-12">
          <h1 class="font-oswald text-5xl uppercase italic tracking-tighter">System Settings</h1>
          <p class="text-white/40 text-sm font-light">Konfigurasi variabel bisnis Masashimura</p>
        </div>

        <div class="space-y-8">
          <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-8 hover:border-primary/20 transition-all duration-300">
            <h2 class="font-oswald text-xl uppercase tracking-wider mb-6 text-primary flex items-center gap-2">
              <Star size="20" /> Aturan Loyalitas
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <label class="block text-[10px] uppercase text-white/40 mb-3 tracking-widest">Min. Pesanan (Bulan)</label>
                <input v-model="settings.min_orders" type="number" class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 focus:border-primary outline-none transition-all text-white" />
              </div>
              <div>
                <label class="block text-[10px] uppercase text-white/40 mb-3 tracking-widest">Persentase Diskon (%)</label>
                <input v-model="settings.discount_percent" type="number" class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 focus:border-primary outline-none transition-all text-white" />
              </div>
            </div>
          </div>

          <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-8 hover:border-primary/20 transition-all duration-300">
            <h2 class="font-oswald text-xl uppercase tracking-wider mb-6 text-primary flex items-center gap-2">
              <Phone size="20" /> Jalur Pesanan (WhatsApp)
            </h2>
            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-3 tracking-widest">Nomor WA Admin</label>
              <input v-model="settings.admin_whatsapp" type="text" class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 focus:border-primary outline-none transition-all text-white" placeholder="628..." />
              <p class="text-[10px] text-white/20 mt-3 italic">*Gunakan format 62 (tanpa + atau 0)</p>
            </div>
          </div>

          <div class="flex justify-end pt-4">
            <button 
              @click="saveSettings" 
              class="bg-primary text-white font-oswald uppercase px-12 py-4 rounded-sm shadow-neo-red hover:translate-y-[-2px] hover:bg-white hover:text-black transition-all tracking-[0.2em] font-bold text-sm"
            >
              Simpan Perubahan
            </button>
          </div>
        </div>

        <!-- Buat Akun Baru - Hanya Owner -->
        <div v-if="auth.isOwner" class="mt-12 pt-8 border-t border-white/10">
          <button
            @click="showCreateModal = true"
            class="bg-white/10 hover:bg-white/20 px-8 py-4 rounded-2xl flex items-center gap-3 text-lg font-medium transition-all"
          >
            <span class="text-2xl">+</span> 
            Buat Akun Baru (Admin / Owner)
          </button>
        </div>

        <!-- Modal Create User -->
        <CreateUserModal
          v-model:open="showCreateModal"
          @created="handleUserCreated"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AdminSidebar from '@/components/AdminSidebar.vue'
import CreateUserModal from '@/components/CreateUserModal.vue'
import { Star, Phone } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const auth = useAuthStore()
const showCreateModal = ref(false)

const settings = ref({
  min_orders: 10,
  discount_percent: 10,
  admin_whatsapp: '6285773615870'
})

const saveSettings = () => {
  toast.success('Konfigurasi sistem berhasil diperbarui!')
  // TODO: Simpan ke backend nanti
}

const handleUserCreated = () => {
  toast.success('Akun baru berhasil dibuat!')
  // Bisa tambah refresh list user nanti
}
</script>