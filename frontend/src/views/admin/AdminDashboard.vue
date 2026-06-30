<template>
  <div class="dashboard-root">
    <!-- HEADER -->
    <div class="dash-header">
      <div>
        <p class="dash-eyebrow">Masashimura</p>
        <h1 class="dash-title">Admin Dashboard</h1>
      </div>
      <div class="dash-live">
        <span class="live-dot"></span>
        <span class="live-label">Live</span>
      </div>
    </div>

    <!-- FILTER BAR -->
    <div class="filter-bar">
      <div class="date-inputs">
        <div class="date-field">
          <label class="date-label">Dari</label>
          <input v-model="dateFrom" type="date" class="date-input" @change="onDateChange" />
        </div>
        <div class="date-sep">—</div>
        <div class="date-field">
          <label class="date-label">Sampai</label>
          <input v-model="dateTo" type="date" class="date-input" @change="onDateChange" />
        </div>
      </div>

      <div class="shortcuts">
        <button
          v-for="sc in shortcuts"
          :key="sc.label"
          @click="applyShortcut(sc)"
          class="shortcut-btn"
          :class="{ active: activeShortcut === sc.label }"
        >
          {{ sc.label }}
        </button>
      </div>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Memuat data...</p>
    </div>

    <template v-else>
      <!-- STAT CARDS -->
      <div class="stat-grid">

        <div class="stat-card accent-green">
          <div class="stat-top">
            <span class="stat-label">Total Revenue</span>
            <span class="stat-badge">Lunas</span>
          </div>
          <div class="stat-value">{{ formatPrice(stats.total_revenue) }}</div>
          <div class="stat-sub">{{ stats.total_orders }} transaksi · {{ activeDateLabel }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <span class="stat-label">Total Pesanan</span>
          </div>
          <div class="stat-value">{{ stats.total_orders }}</div>
          <div class="stat-sub">{{ stats.completed_orders }} selesai · {{ activeDateLabel }}</div>
        </div>

        <div class="stat-card accent-amber">
          <div class="stat-top">
            <span class="stat-label">Menunggu Pembayaran</span>
          </div>
          <div class="stat-value">{{ stats.pending_orders }}</div>
          <div class="stat-sub">pesanan perlu diproses</div>
        </div>

        <div class="stat-card accent-blue">
          <div class="stat-top">
            <span class="stat-label">Loyal Users</span>
            <span class="stat-badge">Bulan Ini</span>
          </div>
          <div class="stat-value">{{ stats.loyal_users }}</div>
          <div class="stat-sub">
            {{ stats.loyal_users > 0 ? 'memenuhi syarat' : 'belum ada user loyal' }}
          </div>
        </div>

      </div>

      <!-- TOP MENU TABLE -->
      <div class="table-card">
        <div class="table-header">
          <div>
            <h3 class="table-title">Top 5 Menu Terlaris</h3>
            <p class="table-sub">Berdasarkan transaksi lunas · {{ activeDateLabel }}</p>
          </div>
        </div>

        <div v-if="stats.top_menus.length === 0" class="empty-state">
          <div class="empty-icon">🍱</div>
          <p class="empty-text">Belum ada data penjualan di periode ini</p>
          <p class="empty-hint">Coba ubah rentang tanggal di atas</p>
        </div>

        <div v-else class="table-wrap">
          <table class="menu-table">
            <thead>
              <tr>
                <th class="th-rank">#</th>
                <th>Nama Menu</th>
                <th class="th-center">Porsi Terjual</th>
                <th class="th-right">Omzet</th>
                <th class="th-bar">Proporsi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(menu, index) in stats.top_menus" :key="menu.name" class="menu-row">
                <td class="td-rank">
                  <span :class="['rank-badge', index === 0 ? 'rank-gold' : index === 1 ? 'rank-silver' : index === 2 ? 'rank-bronze' : 'rank-default']">
                    {{ index + 1 }}
                  </span>
                </td>
                <td class="td-name">{{ menu.name }}</td>
                <td class="td-center">
                  <span class="qty-val">{{ menu.total_qty }}</span>
                  <span class="qty-unit">porsi</span>
                </td>
                <td class="td-right td-revenue">{{ formatPrice(menu.total_revenue) }}</td>
                <td class="td-bar">
                  <div class="bar-track">
                    <div class="bar-fill" :style="{ width: barWidth(menu.total_qty) + '%' }"></div>
                  </div>
                  <span class="bar-pct">{{ barWidth(menu.total_qty) }}%</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import apiClient from '@/api/client';

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

function onDateChange() {
  activeShortcut.value = '';
  fetchStats();
}

const activeDateLabel = computed(() => {
  if (dateFrom.value === dateTo.value) return formatDate(dateFrom.value);
  return `${formatDate(dateFrom.value)} – ${formatDate(dateTo.value)}`;
});

const fetchStats = async () => {
  loading.value = true;
  try {
    const { data } = await apiClient.get('/orders/stats/', {
      params: { date_from: dateFrom.value, date_to: dateTo.value },
    });
    stats.value = data;
  } catch (err) {
    console.error('Gagal load dashboard stats:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);

function today() { return new Date().toISOString().slice(0, 10); }
function daysAgo(n) { const d = new Date(); d.setDate(d.getDate() - n); return d.toISOString().slice(0, 10); }
function startOfMonth() { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`; }
function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso + 'T00:00:00').toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' });
}
const barWidth = (qty) => {
  const max = Math.max(...stats.value.top_menus.map(m => m.total_qty), 1);
  return Math.round((qty / max) * 100);
};
const formatPrice = (value) =>
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(value || 0);
</script>

<style scoped>
/* ── Root ─────────────────────────────────────────────────────────── */
.dashboard-root {
  min-height: 100vh;
  background: #080808;
  color: #fff;
  padding: 2rem 1.5rem;
  font-family: 'Inter', sans-serif;
  max-width: 1280px;
  margin: 0 auto;
}

/* ── Header ──────────────────────────────────────────────────────── */
.dash-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.dash-eyebrow {
  font-family: 'Oswald', sans-serif;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #dc2626;
  margin-bottom: 0.3rem;
}
.dash-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #fff;
  margin: 0;
}
.dash-live {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.8rem;
  background: rgba(34,197,94,0.08);
  border: 1px solid rgba(34,197,94,0.2);
  border-radius: 100px;
}
.live-dot {
  width: 6px; height: 6px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;
}
.live-label {
  font-size: 0.65rem;
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #22c55e;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ── Filter Bar ───────────────────────────────────────────────────── */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem 1.25rem;
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
}
.date-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.date-field {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.date-label {
  font-size: 0.6rem;
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.25);
}
.date-input {
  background: transparent;
  border: none;
  outline: none;
  color: #fff;
  font-size: 0.85rem;
  font-family: 'Inter', monospace;
  cursor: pointer;
  min-width: 130px;
  color-scheme: dark;
}
.date-input::-webkit-calendar-picker-indicator { filter: invert(0.4); cursor: pointer; }
.date-sep { color: rgba(255,255,255,0.15); font-size: 0.9rem; }

.shortcuts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-left: auto;
}
.shortcut-btn {
  padding: 0.35rem 0.9rem;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: transparent;
  color: rgba(255,255,255,0.4);
  font-family: 'Oswald', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.18s ease;
}
.shortcut-btn:hover {
  border-color: rgba(255,255,255,0.25);
  color: rgba(255,255,255,0.75);
}
.shortcut-btn.active {
  background: #dc2626;
  border-color: #dc2626;
  color: #fff;
}

/* ── Loading ─────────────────────────────────────────────────────── */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 6rem 2rem;
  color: rgba(255,255,255,0.25);
  font-size: 0.75rem;
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.15em;
  text-transform: uppercase;
}
.spinner {
  width: 32px; height: 32px;
  border: 2px solid rgba(255,255,255,0.08);
  border-top-color: #dc2626;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Stat Grid ───────────────────────────────────────────────────── */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
@media (max-width: 1024px) { .stat-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px)  { .stat-grid { grid-template-columns: 1fr; } }

.stat-card {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 1.4rem 1.5rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s;
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: rgba(255,255,255,0.04);
}
.stat-card.accent-green::before { background: #22c55e; }
.stat-card.accent-amber::before { background: #f59e0b; }
.stat-card.accent-blue::before  { background: #3b82f6; }

.stat-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}
.stat-label {
  font-family: 'Oswald', sans-serif;
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.35);
}
.stat-badge {
  font-size: 0.55rem;
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.15rem 0.5rem;
  border-radius: 100px;
  border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.3);
}
.stat-value {
  font-family: 'Inter', monospace;
  font-size: 1.6rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.1;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}
.accent-green .stat-value { color: #4ade80; }
.accent-amber .stat-value { color: #fbbf24; }
.accent-blue  .stat-value { color: #60a5fa; }

.stat-sub {
  font-size: 0.7rem;
  color: rgba(255,255,255,0.2);
  font-family: 'Inter', sans-serif;
}

/* ── Table Card ──────────────────────────────────────────────────── */
.table-card {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  overflow: hidden;
}
.table-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.table-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #fff;
  margin: 0 0 0.25rem;
}
.table-sub {
  font-size: 0.7rem;
  color: rgba(255,255,255,0.25);
  font-family: 'Inter', sans-serif;
  margin: 0;
}

/* Empty state */
.empty-state {
  padding: 4rem 2rem;
  text-align: center;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.empty-text {
  color: rgba(255,255,255,0.3);
  font-size: 0.85rem;
  margin: 0 0 0.3rem;
}
.empty-hint {
  color: rgba(255,255,255,0.15);
  font-size: 0.72rem;
  margin: 0;
}

/* Table */
.table-wrap { overflow-x: auto; }
.menu-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}
.menu-table thead tr {
  background: rgba(255,255,255,0.02);
}
.menu-table th {
  padding: 0.75rem 1.5rem;
  font-family: 'Oswald', sans-serif;
  font-size: 0.6rem;
  font-weight: 400;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.25);
  text-align: left;
  white-space: nowrap;
}
.th-center { text-align: center; }
.th-right  { text-align: right; }
.th-bar    { min-width: 160px; }

.menu-row {
  border-top: 1px solid rgba(255,255,255,0.04);
  transition: background 0.15s;
}
.menu-row:hover { background: rgba(255,255,255,0.02); }

.menu-table td {
  padding: 1rem 1.5rem;
  font-size: 0.875rem;
  vertical-align: middle;
}
.td-rank { width: 56px; }
.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px; height: 28px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  font-family: 'Inter', monospace;
}
.rank-gold   { background: rgba(251,191,36,0.15); color: #fbbf24; }
.rank-silver { background: rgba(156,163,175,0.12); color: #9ca3af; }
.rank-bronze { background: rgba(180,83,9,0.15);  color: #d97706; }
.rank-default{ background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.3); }

.td-name { font-weight: 500; color: #fff; }

.td-center { text-align: center; }
.qty-val { font-weight: 700; font-family: monospace; font-size: 1rem; }
.qty-unit { font-size: 0.7rem; color: rgba(255,255,255,0.3); margin-left: 0.25rem; }

.td-right { text-align: right; }
.td-revenue { font-family: monospace; font-weight: 700; color: #fbbf24; }

.td-bar {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.bar-track {
  flex: 1;
  background: rgba(255,255,255,0.06);
  height: 4px;
  border-radius: 99px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #dc2626, #ef4444);
  border-radius: 99px;
  transition: width 0.7s ease;
}
.bar-pct {
  font-size: 0.65rem;
  font-family: monospace;
  color: rgba(255,255,255,0.25);
  min-width: 2.5rem;
  text-align: right;
}

/* ── Responsive tweaks ───────────────────────────────────────────── */
@media (max-width: 768px) {
  .dashboard-root { padding: 1.25rem 1rem; }
  .dash-title { font-size: 1.4rem; }
  .filter-bar { flex-direction: column; align-items: flex-start; }
  .shortcuts { margin-left: 0; }
  .table-header { flex-direction: column; gap: 0.25rem; }
}
@media (max-width: 480px) {
  .stat-value { font-size: 1.3rem; }
  .dash-live { display: none; }
}
</style>