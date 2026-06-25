<template>
  <div class="p-6 text-white max-w-7xl mx-auto">
    <h1 class="text-3xl font-oswald uppercase mb-8">Admin Dashboard</h1>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-20 text-white/30">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-red-500 mb-4"></div>
      <p class="text-xs font-oswald uppercase tracking-widest">Memuat data dashboard...</p>
    </div>

    <template v-else>
      <!-- ── 4 KARTU STATISTIK ── -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

        <!-- Total revenue hanya dari order yang sudah PAID -->
        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Total Revenue (Lunas)</p>
          <h2 class="text-2xl font-bold mt-2 font-mono text-emerald-400">
            {{ formatPrice(stats.total_revenue) }}
          </h2>
          <p class="text-white/20 text-[10px] mt-1">dari {{ stats.total_orders }} transaksi lunas</p>
        </div>

        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Total Pesanan</p>
          <h2 class="text-2xl font-bold mt-2">{{ stats.total_orders }}</h2>
          <p class="text-white/20 text-[10px] mt-1">{{ stats.completed_orders }} selesai</p>
        </div>

        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Menunggu Pembayaran</p>
          <h2 class="text-2xl font-bold mt-2 text-yellow-500">{{ stats.pending_orders }}</h2>
          <p class="text-white/20 text-[10px] mt-1">perlu diproses</p>
        </div>

        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Loyal Users</p>
          <h2 class="text-2xl font-bold mt-2 text-emerald-500">{{ stats.loyal_users }}</h2>
          <p class="text-white/20 text-[10px] mt-1">memenuhi syarat bulan ini</p>
        </div>

      </div>

      <!-- ── TOP 5 MENU ── -->
      <div class="bg-[#0a0a0a] rounded-2xl border border-white/5 overflow-hidden">
        <div class="p-6 border-b border-white/5">
          <h3 class="font-oswald uppercase text-white/40 text-xs tracking-widest">
            Top 5 Menu Terlaris (dari transaksi lunas)
          </h3>
        </div>

        <div v-if="stats.top_menus.length === 0" class="text-center text-white/20 py-12 text-sm">
          Belum ada data penjualan
        </div>

        <table v-else class="w-full text-left">
          <thead class="bg-white/[0.02] text-[10px] uppercase font-oswald tracking-widest text-white/30">
            <tr>
              <th class="px-6 py-4">#</th>
              <th class="px-6 py-4">Nama Menu</th>
              <th class="px-6 py-4 text-center">Jumlah Porsi</th>
              <th class="px-6 py-4 text-right">Total Omzet</th>
              <th class="px-6 py-4">Proporsi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/5">
            <tr
              v-for="(menu, index) in stats.top_menus"
              :key="menu.name"
              class="hover:bg-white/[0.02] transition-colors"
            >
              <td class="px-6 py-4 text-white/20 font-mono text-sm">{{ index + 1 }}</td>

              <td class="px-6 py-4 font-medium text-white">{{ menu.name }}</td>

              <td class="px-6 py-4 text-center">
                <span class="font-bold text-xl text-white font-mono">{{ menu.total_qty }}</span>
                <span class="text-white/30 text-xs ml-1">porsi</span>
              </td>

              <td class="px-6 py-4 text-right font-bold font-mono text-amber-400">
                {{ formatPrice(menu.total_revenue) }}
              </td>

              <td class="px-6 py-4 w-40">
                <div class="flex items-center gap-2">
                  <div class="flex-1 bg-white/5 h-1.5 rounded-full overflow-hidden">
                    <div
                      class="bg-red-600 h-full rounded-full transition-all duration-700"
                      :style="{ width: barWidth(menu.total_qty) + '%' }"
                    ></div>
                  </div>
                  <span class="text-white/20 text-[10px] font-mono w-8 text-right">
                    {{ barWidth(menu.total_qty) }}%
                  </span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api/client';

const loading = ref(true);

const stats = ref({
  total_revenue:    0,
  total_orders:     0,
  pending_orders:   0,
  completed_orders: 0,
  top_menus:        [],   // [{ name, total_qty, total_revenue }]
  loyal_users:      0,
});

// Bar width relatif terhadap menu dengan penjualan tertinggi
const barWidth = (qty) => {
  const max = Math.max(...stats.value.top_menus.map(m => m.total_qty), 1);
  return Math.round((qty / max) * 100);
};

const formatPrice = (value) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency', currency: 'IDR', minimumFractionDigits: 0,
  }).format(value || 0);

const fetchStats = async () => {
  loading.value = true;
  try {
    // URL sesuai urls.py: path("orders/stats/", DashboardStatsView.as_view())
    const { data } = await apiClient.get('/orders/stats/');
    stats.value = data;
  } catch (err) {
    console.error('Gagal load dashboard stats:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);
</script>