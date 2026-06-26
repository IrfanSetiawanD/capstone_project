<template>
  <div class="p-6 text-white max-w-7xl mx-auto">
    <h1 class="text-3xl font-oswald uppercase mb-8">Admin Dashboard</h1>

    <!-- DATE FILTER -->
    <div class="flex flex-wrap items-center gap-3 mb-8">
      <div class="flex items-center gap-2 bg-[#0a0a0a] border border-white/10 rounded-xl px-4 py-2">
        <span class="text-white/30 text-xs uppercase tracking-widest font-oswald">Dari</span>
        <input
          v-model="dateFrom"
          type="date"
          class="bg-transparent text-white text-sm outline-none"
          @change="onDateChange"
        />
      </div>
      <div class="flex items-center gap-2 bg-[#0a0a0a] border border-white/10 rounded-xl px-4 py-2">
        <span class="text-white/30 text-xs uppercase tracking-widest font-oswald">Sampai</span>
        <input
          v-model="dateTo"
          type="date"
          class="bg-transparent text-white text-sm outline-none"
          @change="onDateChange"
        />
      </div>

      <!-- Shortcut buttons -->
      <button
        v-for="sc in shortcuts"
        :key="sc.label"
        @click="applyShortcut(sc)"
        class="px-4 py-2 rounded-xl text-xs font-oswald uppercase tracking-widest border transition-colors"
        :class="activeShortcut === sc.label
          ? 'bg-red-600 border-red-600 text-white'
          : 'bg-[#0a0a0a] border-white/10 text-white/40 hover:border-white/30 hover:text-white/70'"
      >
        {{ sc.label }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-20 text-white/30">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-red-500 mb-4"></div>
      <p class="text-xs font-oswald uppercase tracking-widest">Memuat data dashboard...</p>
    </div>

    <template v-else>
      <!-- 4 KARTU STATISTIK -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Total Revenue (Lunas)</p>
          <h2 class="text-2xl font-bold mt-2 font-mono text-emerald-400">
            {{ formatPrice(stats.total_revenue) }}
          </h2>
          <p class="text-white/20 text-[10px] mt-1">dari {{ stats.total_orders }} transaksi lunas</p>
          <p class="text-white/20 text-[10px] mt-0.5 font-mono">{{ activeDateLabel }}</p>
        </div>

        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Total Pesanan</p>
          <h2 class="text-2xl font-bold mt-2">{{ stats.total_orders }}</h2>
          <p class="text-white/20 text-[10px] mt-1">{{ stats.completed_orders }} selesai</p>
          <p class="text-white/20 text-[10px] mt-0.5 font-mono">{{ activeDateLabel }}</p>
        </div>

        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Menunggu Pembayaran</p>
          <h2 class="text-2xl font-bold mt-2 text-yellow-500">{{ stats.pending_orders }}</h2>
          <p class="text-white/20 text-[10px] mt-1">perlu diproses</p>
          <p class="text-white/20 text-[10px] mt-0.5 font-mono">{{ activeDateLabel }}</p>
        </div>

        <!-- Loyal Users: TIDAK ikut filter tanggal -->
        <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5">
          <p class="text-white/40 text-xs uppercase tracking-widest">Loyal Users</p>
          <h2
            class="text-2xl font-bold mt-2"
            :class="stats.loyal_users > 0 ? 'text-emerald-500' : 'text-white/20'"
          >
            {{ stats.loyal_users }}
          </h2>
          <p class="text-white/20 text-[10px] mt-1">memenuhi syarat bulan ini</p>
          <p v-if="stats.loyal_users === 0" class="text-white/20 text-[10px] mt-0.5">
            belum ada user loyal
          </p>
        </div>

      </div>

      <!-- TOP 5 MENU -->
      <div class="bg-[#0a0a0a] rounded-2xl border border-white/5 overflow-hidden">
        <div class="p-6 border-b border-white/5 flex items-center justify-between">
          <h3 class="font-oswald uppercase text-white/40 text-xs tracking-widest">
            Top 5 Menu Terlaris (dari transaksi lunas)
          </h3>
          <span class="text-white/20 text-[10px] font-mono">{{ activeDateLabel }}</span>
        </div>

        <div v-if="stats.top_menus.length === 0" class="text-center text-white/20 py-12 text-sm">
          Belum ada data penjualan di periode ini
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
import { ref, computed, onMounted } from 'vue';
import apiClient from '@/api/client';

// ── State ──────────────────────────────────────────────────────────
const loading        = ref(true);
const dateFrom       = ref(today());
const dateTo         = ref(today());
const activeShortcut = ref('Hari Ini');

const stats = ref({
  total_revenue:    0,
  total_orders:     0,
  pending_orders:   0,
  completed_orders: 0,
  top_menus:        [],
  loyal_users:      0,
});

// ── Shortcuts ───────────────────────────────────────────────────────
const shortcuts = [
  { label: 'Hari Ini',  from: () => today(),       to: () => today() },
  { label: 'Kemarin',   from: () => daysAgo(1),     to: () => daysAgo(1) },
  { label: '7 Hari',    from: () => daysAgo(6),     to: () => today() },
  { label: 'Bulan Ini', from: () => startOfMonth(), to: () => today() },
];

function applyShortcut(sc) {
  activeShortcut.value = sc.label;
  dateFrom.value = sc.from();
  dateTo.value   = sc.to();
  fetchStats();
}

// Reset shortcut aktif kalau user ganti manual lewat input
function onDateChange() {
  activeShortcut.value = '';
  fetchStats();
}

// ── Label periode aktif ─────────────────────────────────────────────
const activeDateLabel = computed(() => {
  if (dateFrom.value === dateTo.value) return formatDate(dateFrom.value);
  return `${formatDate(dateFrom.value)} – ${formatDate(dateTo.value)}`;
});

// ── Fetch ───────────────────────────────────────────────────────────
const fetchStats = async () => {
  loading.value = true;
  try {
    const { data } = await apiClient.get('/orders/stats/', {
      params: {
        date_from: dateFrom.value,
        date_to:   dateTo.value,
      },
    });
    stats.value = data;
  } catch (err) {
    console.error('Gagal load dashboard stats:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);

// ── Helpers ─────────────────────────────────────────────────────────
function today() {
  return new Date().toISOString().slice(0, 10);
}
function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().slice(0, 10);
}
function startOfMonth() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`;
}
function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso + 'T00:00:00').toLocaleDateString('id-ID', {
    day: '2-digit', month: 'short', year: 'numeric',
  });
}
const barWidth = (qty) => {
  const max = Math.max(...stats.value.top_menus.map(m => m.total_qty), 1);
  return Math.round((qty / max) * 100);
};
const formatPrice = (value) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency', currency: 'IDR', minimumFractionDigits: 0,
  }).format(value || 0);
</script>