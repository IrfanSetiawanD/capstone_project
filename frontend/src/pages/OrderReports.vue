<template>
  <div class="w-full">
    <div class="max-w-7xl mx-auto pb-24">

      <!-- ═══ HEADER ════════════════════════════════════════════════════ -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-6">
        <div>
          <p class="text-white/20 text-[10px] font-oswald uppercase tracking-[0.2em] mb-2">Masashimura · Admin</p>
          <h1 class="font-oswald text-5xl uppercase italic tracking-tighter text-red-600 leading-none">
            Order Reports
          </h1>
          <p class="text-white/35 text-sm font-light mt-2">
            Analisis omzet, performa menu, dan pelanggan
          </p>
        </div>

        <button
          v-if="activeGroup !== 'lifetime'"
          @click="exportDocument('pdf')"
          :disabled="loading"
          class="flex items-center gap-2 bg-white/5 border border-white/10 px-5 py-3 rounded-xl text-[10px] font-oswald uppercase tracking-widest hover:bg-white/10 transition-all text-white shrink-0 disabled:opacity-40"
        >
          <Download :size="13" class="text-red-500" />
          Export PDF
        </button>
      </div>

      <!-- ═══ FILTER BAR ════════════════════════════════════════════════ -->
      <div class="bg-[#0d0d0d] border border-white/8 rounded-2xl p-1.5 mb-8 flex flex-wrap gap-1">

        <!-- Group tabs -->
        <div class="flex gap-1 flex-1 min-w-[260px]">
          <button
            v-for="g in groups"
            :key="g.value"
            @click="selectGroup(g.value)"
            :class="[
              'flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-[11px] font-oswald uppercase tracking-widest transition-all duration-200',
              activeGroup === g.value
                ? 'bg-red-600 text-white shadow-lg shadow-red-900/30'
                : 'text-white/30 hover:text-white/60 hover:bg-white/5'
            ]"
          >
            <component :is="g.icon" :size="12" />
            {{ g.label }}
          </button>
        </div>

        <!-- Divider -->
        <div class="w-px bg-white/8 my-1 hidden sm:block"></div>

        <!-- Sub-filter: Mingguan -->
        <template v-if="activeGroup === 'weekly'">
          <div class="flex items-center gap-1 px-1">
            <button
              v-for="w in weekOptions"
              :key="w.value"
              @click="activeWeek = w.value; fetch()"
              :class="[
                'px-4 py-3 rounded-xl text-[10px] font-oswald uppercase tracking-widest transition-all',
                activeWeek === w.value ? 'bg-white/10 text-white' : 'text-white/30 hover:text-white/50'
              ]"
            >
              {{ w.label }}
            </button>
          </div>
        </template>

        <!-- Sub-filter: Bulanan -->
        <template v-if="activeGroup === 'monthly'">
          <div class="flex items-center gap-2 px-2">
            <select
              v-model.number="activeMonth"
              @change="fetch()"
              class="bg-transparent border border-white/10 rounded-lg px-3 py-2.5 text-[11px] font-oswald uppercase tracking-widest outline-none focus:border-red-600 text-white cursor-pointer"
            >
              <option v-for="m in 12" :key="m" :value="m" class="bg-[#111]">{{ monthName(m) }}</option>
            </select>
            <select
              v-model.number="activeYear"
              @change="fetch()"
              class="bg-transparent border border-white/10 rounded-lg px-3 py-2.5 text-[11px] font-oswald uppercase tracking-widest outline-none focus:border-red-600 text-white cursor-pointer"
            >
              <option v-for="y in yearOptions" :key="y" :value="y" class="bg-[#111]">{{ y }}</option>
            </select>
          </div>
        </template>

        <!-- Sub-filter: Tahunan -->
        <template v-if="activeGroup === 'yearly'">
          <div class="flex items-center gap-1 px-1">
            <button
              v-for="y in yearOptions"
              :key="y"
              @click="activeYear = y; fetch()"
              :class="[
                'px-4 py-3 rounded-xl text-[11px] font-oswald uppercase tracking-widest transition-all',
                activeYear === y ? 'bg-white/10 text-white' : 'text-white/30 hover:text-white/50'
              ]"
            >
              {{ y }}
            </button>
          </div>
        </template>

        <!-- Sub-filter: Lifetime — just a label -->
        <template v-if="activeGroup === 'lifetime'">
          <div class="flex items-center px-4">
            <span class="text-white/20 text-[10px] font-oswald uppercase tracking-widest">Semua waktu</span>
          </div>
        </template>
      </div>

      <!-- ═══ PERIOD BADGE ══════════════════════════════════════════════ -->
      <div class="flex items-center gap-3 mb-8">
        <div class="h-px flex-1 bg-white/5"></div>
        <span class="text-white/20 text-[10px] font-oswald uppercase tracking-[0.25em] whitespace-nowrap">
          {{ periodLabel }}
        </span>
        <div class="h-px flex-1 bg-white/5"></div>
      </div>

      <!-- ═══ LOADING ═══════════════════════════════════════════════════ -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-32 gap-4">
        <div class="w-8 h-8 border-2 border-red-600/30 border-t-red-600 rounded-full animate-spin"></div>
        <p class="text-white/20 text-xs font-oswald uppercase tracking-widest">Memuat data laporan...</p>
      </div>

      <!-- ═══ CONTENT ═══════════════════════════════════════════════════ -->
      <template v-else-if="report">

        <!-- 1. KPI STATS -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard icon="DollarSign" color="red"     label="Total Omzet"          :value="formatRp(report.stats.total_omzet)"          :sub="vsLabel" />
          <StatCard icon="ShoppingBag" color="amber"  label="Total Transaksi"       :value="report.stats.total_transaksi.toLocaleString('id-ID')" />
          <StatCard icon="TrendingUp"  color="emerald" label="Rata-rata Transaksi"  :value="formatRp(report.stats.rata_rata_transaksi)" />
          <StatCard icon="Utensils"    color="sky"    label="Menu Aktif"            :value="report.stats.menu_aktif" />
        </div>

        <!-- 2. TREND CHARTS -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-5">
          <RCard title="Omzet" :subtitle="trendSubtitle" icon="TrendingUp" accent="red">
            <Bar :data="omzetData" :options="barOpts('#dc2626')" />
          </RCard>
          <RCard title="Transaksi" :subtitle="trendSubtitle" icon="ShoppingBag" accent="amber">
            <Bar :data="transaksiData" :options="barOpts('#f59e0b')" />
          </RCard>
        </div>

        <!-- 3. TOP MENU + PALING MENGHASILKAN -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-5">
          <RCard title="Top 10 Menu Terlaris" icon="Award" accent="amber" class="lg:col-span-2">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-white/25 text-[9px] uppercase tracking-[0.15em]">
                  <th class="pb-4 text-left font-normal">#</th>
                  <th class="pb-4 text-left font-normal">Menu</th>
                  <th class="pb-4 text-right font-normal">Qty</th>
                  <th class="pb-4 text-right font-normal">Omzet</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(m, i) in report.top_menu"
                  :key="i"
                  class="border-t border-white/4 group hover:bg-white/2 transition-colors"
                >
                  <td class="py-3 pr-3 text-white/20 text-xs font-oswald w-8">{{ String(i+1).padStart(2,'0') }}</td>
                  <td class="py-3 text-white font-oswald uppercase tracking-tight text-sm">{{ m.name }}</td>
                  <td class="py-3 text-right">
                    <span class="bg-amber-500/10 text-amber-400 font-bold text-xs px-2.5 py-1 rounded-lg">{{ m.qty }}</span>
                  </td>
                  <td class="py-3 text-right text-white/50 font-mono text-xs">{{ formatRp(m.omzet) }}</td>
                </tr>
                <tr v-if="!report.top_menu.length">
                  <td colspan="4" class="py-10 text-center text-white/20 text-xs">Belum ada data penjualan</td>
                </tr>
              </tbody>
            </table>
          </RCard>

          <RCard title="Paling Menghasilkan" icon="Gem" accent="emerald">
            <div class="space-y-5">
              <div v-for="(m, i) in report.menu_paling_menghasilkan" :key="i">
                <div class="flex justify-between text-xs mb-2">
                  <span class="text-white font-oswald uppercase tracking-tight">{{ m.name }}</span>
                  <span class="text-emerald-400 font-bold tabular-nums">{{ formatRp(m.omzet) }}</span>
                </div>
                <div class="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full transition-all duration-700"
                    :style="{ width: pct(m.omzet, maxMenghasilkan) + '%', background: 'linear-gradient(90deg, #10b981, #34d399)' }"
                  ></div>
                </div>
              </div>
              <p v-if="!report.menu_paling_menghasilkan.length" class="text-center text-white/20 text-xs py-8">
                Belum ada data
              </p>
            </div>
          </RCard>
        </div>

        <!-- 4. BOTTOM ROW -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-5">

          <!-- Menu Tidak Laku -->
          <RCard title="Menu Tidak Laku" icon="AlertTriangle" accent="red">
            <div class="space-y-2 max-h-64 overflow-y-auto pr-1 custom-scroll">
              <div
                v-for="(m, i) in report.menu_tidak_laku"
                :key="i"
                class="flex justify-between items-center bg-red-950/20 border border-red-500/8 rounded-xl px-4 py-3"
              >
                <span class="text-white text-xs font-oswald uppercase tracking-tight">{{ m.name }}</span>
                <span class="text-red-400/70 text-[9px] font-bold uppercase tracking-wider ml-3 shrink-0">
                  {{ m.transaksi }}×
                </span>
              </div>
              <div v-if="!report.menu_tidak_laku.length" class="text-center text-white/20 text-xs py-8">
                🎉 Semua menu terjual
              </div>
            </div>
          </RCard>

          <!-- Metode Pembayaran -->
          <RCard title="Metode Pembayaran" icon="CreditCard" accent="sky">
            <div class="flex flex-col items-center">
              <div class="w-40 h-40 mb-5">
                <Pie :data="paymentData" :options="pieOpts" />
              </div>
              <div class="w-full space-y-2.5">
                <div
                  v-for="(p, i) in report.metode_pembayaran"
                  :key="i"
                  class="flex items-center justify-between"
                >
                  <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full" :style="{ background: payColors[p.method] || '#6b7280' }"></div>
                    <span class="text-white/50 text-xs">{{ p.label }}</span>
                  </div>
                  <span class="text-white text-xs font-bold tabular-nums">{{ p.percent }}%</span>
                </div>
                <div v-if="!report.metode_pembayaran.length" class="text-center text-white/20 text-xs py-4">
                  Belum ada transaksi
                </div>
              </div>
            </div>
          </RCard>

          <!-- Jam Teramai -->
          <RCard title="Jam Teramai" icon="Clock" accent="violet">
            <Bar :data="jamData" :options="barOptsY('#8b5cf6')" />
          </RCard>
        </div>

        <!-- 5. PELANGGAN -->
        <RCard title="Pelanggan" icon="Users" accent="pink">
          <div class="grid grid-cols-3 gap-6 text-center">
            <div class="py-4">
              <p class="font-oswald text-4xl font-bold text-white mb-1">{{ report.pelanggan.baru }}</p>
              <p class="text-[9px] text-white/30 uppercase tracking-[0.2em]">Pelanggan Baru</p>
            </div>
            <div class="py-4 border-x border-white/5">
              <p class="font-oswald text-4xl font-bold text-white mb-1">{{ report.pelanggan.lama }}</p>
              <p class="text-[9px] text-white/30 uppercase tracking-[0.2em]">Pelanggan Lama</p>
            </div>
            <div class="py-4">
              <p class="font-oswald text-4xl font-bold text-amber-400 mb-1">{{ report.pelanggan.loyal_member }}</p>
              <p class="text-[9px] text-white/30 uppercase tracking-[0.2em]">Member Loyal</p>
            </div>
          </div>
        </RCard>
      </template>

      <!-- ═══ EMPTY ══════════════════════════════════════════════════════ -->
      <div v-else-if="!loading" class="text-center py-32">
        <p class="text-white/20 text-sm">Gagal memuat data. Coba lagi.</p>
        <button @click="fetch()" class="mt-4 text-red-500 text-xs hover:text-red-400 underline">Muat ulang</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from "vue";
import { Bar, Pie } from "vue-chartjs";
import {
  Chart as ChartJS, BarElement, CategoryScale, LinearScale,
  ArcElement, Tooltip, Legend,
} from "chart.js";
import {
  TrendingUp, Award, Download, ShoppingBag, DollarSign, Utensils,
  AlertTriangle, CreditCard, Clock, Users, Gem, Calendar,
  CalendarDays, CalendarRange, Infinity,
} from "lucide-vue-next";
import apiClient from "@/api/client";

ChartJS.register(BarElement, CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

// ── Filter state ──────────────────────────────────────────────────────────
const now        = new Date();
const loading    = ref(true);
const report     = ref(null);

const activeGroup = ref("lifetime");   // lifetime | weekly | monthly | yearly
const activeWeek  = ref("this");       // this | last
const activeMonth = ref(now.getMonth() + 1);
const activeYear  = ref(now.getFullYear());

const groups = [
  { label: "Lifetime",  value: "lifetime", icon: Infinity },
  { label: "Mingguan",  value: "weekly",   icon: CalendarDays },
  { label: "Bulanan",   value: "monthly",  icon: Calendar },
  { label: "Tahunan",   value: "yearly",   icon: CalendarRange },
];

const weekOptions = [
  { label: "Minggu ini",  value: "this" },
  { label: "Minggu lalu", value: "last" },
  { label: "2 minggu",    value: "2w" },
  { label: "4 minggu",    value: "4w" },
];

const yearOptions = Array.from({ length: 5 }, (_, i) => now.getFullYear() - i);

const BULAN = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"];
const monthName = (m) => BULAN[m - 1];

// ── Derived labels ────────────────────────────────────────────────────────
const periodLabel = computed(() => {
  if (activeGroup.value === "lifetime") return "Semua data tersimpan";
  if (activeGroup.value === "weekly") {
    const w = weekOptions.find(w => w.value === activeWeek.value);
    return w?.label || "Mingguan";
  }
  if (activeGroup.value === "monthly") return `${monthName(activeMonth.value)} ${activeYear.value}`;
  return `Tahun ${activeYear.value}`;
});

const trendSubtitle = computed(() => periodLabel.value);
const vsLabel       = computed(() => "vs. periode sebelumnya");

// ── API params ────────────────────────────────────────────────────────────
const buildParams = () => {
  const g = activeGroup.value;
  if (g === "lifetime") return { period: "lifetime" };
  if (g === "weekly") {
    const daysMap = { this: 7, last: 14, "2w": 14, "4w": 28 };
    const offset  = { this: 0, last: 7, "2w": 0, "4w": 0 };
    return { period: "week", days: daysMap[activeWeek.value], offset: offset[activeWeek.value] };
  }
  if (g === "monthly") return { period: "month", month: activeMonth.value, year: activeYear.value };
  return { period: "year", year: activeYear.value };
};

// ── Fetch ─────────────────────────────────────────────────────────────────
const fetch = async () => {
  loading.value = true;
  try {
    const { data } = await apiClient.get("/orders/reports/full/", { params: buildParams() });
    report.value = data;
  } catch (e) {
    console.error("Gagal load report:", e);
    report.value = null;
  } finally {
    loading.value = false;
  }
};

const selectGroup = (g) => {
  activeGroup.value = g;
  fetch();
};

// ── Chart data ────────────────────────────────────────────────────────────
const omzetData = computed(() => ({
  labels: report.value?.trend.labels || [],
  datasets: [{ label: "Omzet", data: report.value?.trend.omzet || [], backgroundColor: "#dc2626", borderRadius: 5, borderSkipped: false }],
}));

const transaksiData = computed(() => ({
  labels: report.value?.trend.labels || [],
  datasets: [{ label: "Transaksi", data: report.value?.trend.transaksi || [], backgroundColor: "#f59e0b", borderRadius: 5, borderSkipped: false }],
}));

const jamData = computed(() => ({
  labels: report.value?.jam_teramai.map(j => j.label) || [],
  datasets: [{ label: "Transaksi", data: report.value?.jam_teramai.map(j => j.count) || [], backgroundColor: "#8b5cf6", borderRadius: 5, borderSkipped: false }],
}));

const payColors = { cash: "#22c55e", qris: "#3b82f6", qris_manual: "#06b6d4", gateway: "#a855f7" };
const paymentData = computed(() => ({
  labels: report.value?.metode_pembayaran.map(p => p.label) || [],
  datasets: [{
    data: report.value?.metode_pembayaran.map(p => p.total) || [],
    backgroundColor: report.value?.metode_pembayaran.map(p => payColors[p.method] || "#374151") || [],
    borderWidth: 0,
    hoverOffset: 6,
  }],
}));

const maxMenghasilkan = computed(() =>
  Math.max(1, ...(report.value?.menu_paling_menghasilkan.map(m => m.omzet) || [1]))
);
const pct = (v, max) => Math.round((v / max) * 100);

// ── Chart options ─────────────────────────────────────────────────────────
const gridColor  = "rgba(255,255,255,0.04)";
const tickStyle  = { color: "rgba(255,255,255,0.3)", font: { size: 10, family: "Oswald" } };

const barOpts = (color) => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#111",
      borderColor: "rgba(255,255,255,0.08)",
      borderWidth: 1,
      titleColor: "#fff",
      bodyColor: "rgba(255,255,255,0.6)",
    },
  },
  scales: {
    x: { grid: { display: false }, ticks: tickStyle },
    y: { grid: { color: gridColor }, ticks: tickStyle, border: { display: false } },
  },
});

const barOptsY = (color) => ({
  ...barOpts(color),
  indexAxis: "y",
});

const pieOpts = {
  plugins: {
    legend: { display: false },
    tooltip: { backgroundColor: "#111", borderColor: "rgba(255,255,255,0.08)", borderWidth: 1 },
  },
  cutout: "60%",
};

// ── Format ────────────────────────────────────────────────────────────────
const formatRp = (v) => "Rp " + Math.round(v || 0).toLocaleString("id-ID");

// ── Export ────────────────────────────────────────────────────────────────
const exportDocument = (type) => {
  const g = activeGroup.value;
  let params = "";
  if (g === "monthly") params = `mode=monthly&month=${activeMonth.value}&year=${activeYear.value}`;
  else if (g === "yearly") params = `mode=yearly&year=${activeYear.value}`;
  else params = `mode=monthly&month=${activeMonth.value}&year=${activeYear.value}`;
  window.open(`${apiClient.defaults.baseURL}/orders/export/finance-${type === "pdf" ? "pdf" : "excel"}/?${params}`, "_blank");
};

// ── Komponen lokal ────────────────────────────────────────────────────────
const iconMap = { TrendingUp, Award, ShoppingBag, DollarSign, Utensils, AlertTriangle, CreditCard, Clock, Users, Gem };

const accentText = {
  red: "text-red-400", amber: "text-amber-400", emerald: "text-emerald-400",
  sky: "text-sky-400", violet: "text-violet-400", pink: "text-pink-400",
};

const RCard = (props, { slots }) =>
  h("div", { class: "bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 hover:border-white/10 transition-all duration-500" }, [
    h("div", { class: "flex items-center gap-2 mb-5" }, [
      props.icon && iconMap[props.icon]
        ? h(iconMap[props.icon], { size: 13, class: accentText[props.accent] || "text-red-400" })
        : null,
      h("h3", { class: "font-oswald uppercase text-white/25 text-[10px] tracking-[0.18em]" }, props.title),
      props.subtitle
        ? h("span", { class: "text-white/15 text-[10px] font-light ml-1" }, `· ${props.subtitle}`)
        : null,
    ]),
    slots.default ? slots.default() : null,
  ]);

const StatCard = (props) => {
  const bgMap   = { red: "bg-red-500/8", amber: "bg-amber-500/8", emerald: "bg-emerald-500/8", sky: "bg-sky-500/8" };
  const txtMap  = { red: "text-red-400",  amber: "text-amber-400",  emerald: "text-emerald-400",  sky: "text-sky-400" };
  return h("div", { class: "bg-[#0a0a0a] border border-white/5 p-5 rounded-2xl" }, [
    h("div", { class: `w-10 h-10 rounded-xl ${bgMap[props.color]} flex items-center justify-center mb-4` }, [
      iconMap[props.icon] ? h(iconMap[props.icon], { size: 18, class: txtMap[props.color] }) : null,
    ]),
    h("p", { class: "font-oswald text-xl font-bold text-white leading-tight" }, String(props.value)),
    h("p", { class: "text-[9px] text-white/25 uppercase tracking-[0.18em] mt-1" }, props.label),
  ]);
};

onMounted(fetch);
</script>

<style scoped>
.custom-scroll::-webkit-scrollbar { width: 3px; }
.custom-scroll::-webkit-scrollbar-track { background: transparent; }
.custom-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }
</style>