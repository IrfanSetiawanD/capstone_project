<template>
  <div class="flex min-h-screen bg-[#050505] text-white">
    <AdminSidebar />

    <main class="flex-1 ml-64 p-8 md:p-12 overflow-x-hidden font-manrope">
      <div class="max-w-7xl mx-auto">
        
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
          <div>
            <h1 class="font-oswald text-5xl uppercase italic tracking-tighter">Loyal Customers</h1>
            <p class="text-white/40 text-sm font-light mt-1">
              Pelanggan setia • Minimal 10 pesanan & Rp 100.000 dalam 1 bulan
            </p>
          </div>
          
          <button
            @click="refreshData"
            class="px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl flex items-center gap-2 text-sm transition-all"
          >
            <span>🔄</span> Refresh Data
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loyalty.loading" class="text-center py-20 bg-[#0a0a0a] border border-white/5 rounded-2xl">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-red-500 mb-4"></div>
          <p class="text-white/40 font-oswald uppercase tracking-widest text-xs">Mengambil data dari Django...</p>
        </div>

        <!-- Table -->
        <div v-else class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead class="bg-white/[0.02] border-b border-white/5 text-[10px] uppercase font-oswald tracking-[0.2em] text-white/30">
                <tr>
                  <th class="px-8 py-6">Nomor Telepon</th>
                  <th class="px-8 py-6">Periode</th>
                  <th class="px-8 py-6 text-center">Jumlah Pesanan</th>
                  <th class="px-8 py-6 text-right">Total Belanja</th>
                  <th class="px-8 py-6 text-center">Status</th>
                  <th class="px-8 py-6 text-center">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr v-for="customer in loyalty.loyalCustomers" :key="customer.phone" 
                    class="hover:bg-white/[0.01] transition-colors">
                  <td class="px-8 py-5 font-bold font-oswald tracking-wider">
                    {{ customer.phone }}
                  </td>
                  <td class="px-8 py-5 text-white/40 text-sm">
                    {{ customer.month || '-' }}
                  </td>
                  <td class="px-8 py-5 text-center">
                    <span class="text-xl font-bold">{{ customer.order_count || 0 }}</span>
                  </td>
                  <td class="px-8 py-5 text-right font-bold text-lg text-red-400">
                    {{ formatPrice(customer.total_spent) }}
                  </td>
                  <td class="px-8 py-5 text-center">
                    <span 
                      :class="customer.is_loyal 
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' 
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'"
                      class="inline-block px-5 py-1.5 text-xs rounded-full font-bold uppercase tracking-widest"
                    >
                      {{ customer.is_loyal ? 'LOYAL MEMBER' : 'REGULAR' }}
                    </span>
                  </td>
                  <td class="px-8 py-5 text-center">
                    <button 
                      @click="giveSpecialPrice(customer)"
                      :disabled="!customer.is_loyal"
                      class="px-6 py-2.5 text-xs font-bold uppercase tracking-widest rounded-xl transition-all
                             bg-red-600 hover:bg-red-500 disabled:bg-white/5 disabled:text-white/30"
                    >
                      Beri Harga Khusus
                    </button>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="loyalty.loyalCustomers.length === 0">
                  <td colspan="6" class="px-8 py-24 text-center text-white/30">
                    <p class="text-lg">Belum ada pelanggan loyal</p>
                    <p class="text-sm mt-2">Data akan muncul setelah ada transaksi yang memenuhi syarat</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import AdminSidebar from '@/components/AdminSidebar.vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useLoyaltyStore } from '@/stores/loyalty'
import { toast } from 'vue-sonner'

const auth = useAuthStore()
const loyalty = useLoyaltyStore()
const router = useRouter()

const formatPrice = (price) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price || 0)
}

const giveSpecialPrice = (customer) => {
  toast.success(`Harga khusus diaktifkan untuk ${customer.phone}`)
}

const refreshData = () => {
  loyalty.fetchLoyalCustomers()
}

// FIXED: Izinkan BOTH admin DAN owner
onMounted(() => {
  if (!auth.user) {
    router.push('/login')
    return
  }

  // Tidak perlu cek role ketat di sini (router guard sudah handle)
  loyalty.fetchLoyalCustomers()
})
</script>