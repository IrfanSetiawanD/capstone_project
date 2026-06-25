<template>
  <div class="p-4 sm:p-6 lg:p-8 text-white max-w-7xl mx-auto w-full box-border space-y-8">

    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold font-oswald tracking-wide">
          FINANCIAL REPORTS
        </h1>
        <p class="text-xs text-white/40 mt-1">
          📅 Tampilan:
          <span class="text-red-400 font-mono font-bold">{{ viewModeLabel }}</span>
        </p>
      </div>

      <!-- MODE SWITCH -->
      <div class="flex items-center gap-2 bg-[#0a0a0a] border border-white/5 p-1.5 rounded-2xl">
        <button
          v-for="m in viewModes"
          :key="m.key"
          @click="switchMode(m.key)"
          class="px-4 py-2 rounded-xl text-xs font-bold transition uppercase tracking-wider"
          :class="viewMode === m.key ? 'bg-red-600 text-white' : 'bg-white/5 hover:bg-white/10 text-white/50'"
        >
          {{ m.label }}
        </button>
      </div>
    </div>

    <!-- NAVIGASI TANGGAL: HARIAN -->
    <div v-if="viewMode === 'daily'" class="flex items-center gap-2 bg-[#0a0a0a] border border-white/5 p-1.5 rounded-2xl w-full md:w-fit">
      <button @click="changeDate(-1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold transition">◀️ Kemarin</button>
      <div class="px-3 text-xs font-mono font-bold text-white/80 tracking-widest">{{ targetDateString }}</div>
      <button @click="changeDate(1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold transition">Besok ▶️</button>
    </div>

    <!-- NAVIGASI BULAN (untuk tampilan harian per bulan) -->
    <div v-if="viewMode === 'monthly'" class="flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-2 bg-[#0a0a0a] border border-white/5 p-1.5 rounded-2xl">
        <button @click="changeMonth(-1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold transition">◀️</button>
        <div class="px-3 text-xs font-mono font-bold text-white/80 tracking-widest">{{ monthNames[selectedMonth - 1] }} {{ selectedYear }}</div>
        <button @click="changeMonth(1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold transition">▶️</button>
      </div>
      <select v-model.number="selectedYear" @change="fetchMonthlyData"
        class="bg-[#0a0a0a] border border-white/10 rounded-xl px-4 py-2.5 text-xs font-mono text-white outline-none focus:border-red-600 transition">
        <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
      </select>
    </div>

    <!-- NAVIGASI TAHUN (untuk tampilan bulanan per tahun) -->
    <div v-if="viewMode === 'yearly'" class="flex items-center gap-3">
      <div class="flex items-center gap-2 bg-[#0a0a0a] border border-white/5 p-1.5 rounded-2xl">
        <button @click="changeYear(-1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold transition">◀️</button>
        <div class="px-3 text-xs font-mono font-bold text-white/80 tracking-widest">Tahun {{ selectedYear }}</div>
        <button @click="changeYear(1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold transition">▶️</button>
      </div>
      <select v-model.number="selectedYear" @change="fetchYearlyData"
        class="bg-[#0a0a0a] border border-white/10 rounded-xl px-4 py-2.5 text-xs font-mono text-white outline-none focus:border-red-600 transition">
        <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
      </select>
    </div>

    <!-- 3 CARD RINGKASAN -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl space-y-2 shadow-lg">
        <p class="text-[10px] uppercase font-bold tracking-widest text-white/40">Total Pendapatan</p>
        <p class="text-xl sm:text-2xl font-mono font-bold text-emerald-400">
          Rp {{ formatNumber(summaryCards.revenue) }}
        </p>
        <p class="text-[10px] text-white/20">Hanya order yang sudah lunas (paid)</p>
      </div>
      <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl space-y-2 shadow-lg">
        <p class="text-[10px] uppercase font-bold tracking-widest text-white/40">Total Pengeluaran</p>
        <p class="text-xl sm:text-2xl font-mono font-bold text-amber-500">
          Rp {{ formatNumber(summaryCards.expenses) }}
        </p>
        <p class="text-[10px] text-white/20">Dari buku kas harian</p>
      </div>
      <div class="bg-[#0a0a0a] border border-red-600/10 bg-gradient-to-b from-red-600/5 to-transparent p-6 rounded-2xl space-y-2 shadow-lg">
        <p class="text-[10px] uppercase font-bold tracking-widest text-white/40">Laba Bersih</p>
        <p class="text-xl sm:text-2xl font-mono font-bold" :class="summaryCards.net_profit >= 0 ? 'text-red-400' : 'text-red-600'">
          Rp {{ formatNumber(summaryCards.net_profit) }}
        </p>
        <p class="text-[10px]" :class="summaryCards.net_profit >= 0 ? 'text-emerald-500/60' : 'text-red-500/60'">
          {{ summaryCards.net_profit >= 0 ? '▲ Surplus' : '▼ Defisit' }}
        </p>
      </div>
    </div>

    <!-- GRAFIK + TABEL (mode harian per tanggal) -->
    <div v-if="viewMode === 'daily'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

      <!-- FORM INPUT PENGELUARAN -->
      <div class="lg:col-span-1 bg-[#0a0a0a] border border-white/5 rounded-2xl p-5 sm:p-6 space-y-4">
        <div>
          <h3 class="font-bold text-base font-oswald text-white/90 uppercase tracking-wide">Input Pengeluaran</h3>
          <p class="text-[11px] text-white/30">Catat biaya operasional harian</p>
        </div>
        <form @submit.prevent="submitExpense" class="space-y-4 text-xs">
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Keterangan</label>
            <input v-model="expenseForm.description" type="text" placeholder="Misal: Beli Daging, Gas 3kg" required
              class="w-full bg-[#111] border border-white/10 rounded-xl py-3 px-4 text-sm focus:outline-none focus:border-red-600 transition text-white" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Nominal (Rp)</label>
            <input v-model.number="expenseForm.amount" type="number" placeholder="Contoh: 150000" required min="1"
              class="w-full bg-[#111] border border-white/10 rounded-xl py-3 px-4 text-sm focus:outline-none focus:border-red-600 font-mono transition text-white" />
          </div>
          <button type="submit" :disabled="isSubmittingExpense"
            class="w-full bg-white/5 hover:bg-white/10 border border-white/10 font-bold py-3.5 rounded-xl text-xs uppercase tracking-widest transition text-amber-500 disabled:opacity-30">
            {{ isSubmittingExpense ? 'Menyimpan...' : '⚡ Catat Pengeluaran' }}
          </button>
        </form>
      </div>

      <!-- DOKUMEN + LOG PENGELUARAN -->
      <div class="lg:col-span-2 space-y-4 w-full">
        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3 bg-[#0a0a0a] border border-white/5 p-4 rounded-2xl shadow-lg">
          <div class="text-xs">
            <h4 class="font-bold text-white uppercase tracking-wide">Export Dokumen</h4>
            <p class="text-white/30 text-[11px]">Rekap transaksi database (bulanan / tahunan)</p>
          </div>
          <div class="flex items-center gap-2">
            <div class="flex gap-1">
              <select v-model.number="exportMonth"
                class="bg-[#111] border border-white/10 rounded-xl px-3 py-2 text-xs font-mono text-white outline-none focus:border-red-600">
                <option v-for="(name, idx) in monthNames" :key="idx" :value="idx + 1">{{ name }}</option>
              </select>
              <select v-model.number="exportYear"
                class="bg-[#111] border border-white/10 rounded-xl px-3 py-2 text-xs font-mono text-white outline-none focus:border-red-600">
                <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
              </select>
            </div>
            <button @click="exportDocument('excel')"
              class="px-4 py-2.5 bg-emerald-600/10 hover:bg-emerald-600/20 border border-emerald-500/20 rounded-xl text-xs font-bold text-emerald-400 uppercase tracking-wider transition">
              📥 Excel
            </button>
            <button @click="exportDocument('pdf')"
              class="px-4 py-2.5 bg-red-600/10 hover:bg-red-600/20 border border-red-500/20 rounded-xl text-xs font-bold text-red-500 uppercase tracking-wider transition">
              📄 PDF
            </button>
          </div>
        </div>

        <!-- Log Pengeluaran Harian -->
        <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden shadow-2xl">
          <div class="p-4 bg-white/5 border-b border-white/5">
            <h4 class="font-bold font-oswald text-xs uppercase tracking-wider text-white/50">
              Rincian Pengeluaran — {{ targetDateString }}
            </h4>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse min-w-[400px]">
              <thead class="bg-black/20">
                <tr class="text-white/30 text-[10px] font-bold uppercase tracking-widest border-b border-white/5">
                  <th class="px-6 py-3">Keterangan</th>
                  <th class="px-6 py-3 text-right">Nominal</th>
                  <th class="px-6 py-3 text-center">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5 text-xs text-zinc-300">
                <tr v-for="exp in dailyExpensesList" :key="exp.id" class="hover:bg-white/5 transition-colors">
                  <td class="px-6 py-4">{{ exp.description }}</td>
                  <td class="px-6 py-4 text-right font-mono font-bold text-amber-500">-Rp {{ formatNumber(exp.amount) }}</td>
                  <td class="px-6 py-4 text-center">
                    <button @click="deleteExpense(exp.id)" class="text-red-400 hover:text-red-300 text-[10px] uppercase tracking-wider transition">Hapus</button>
                  </td>
                </tr>
                <tr v-if="!dailyExpensesList.length">
                  <td colspan="3" class="p-8 text-center text-white/20 text-xs">Belum ada pengeluaran untuk tanggal ini.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- GRAFIK BULANAN (per hari dalam 1 bulan) -->
    <div v-if="viewMode === 'monthly'" class="space-y-6">
      <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 space-y-4">
        <h3 class="font-oswald text-xs uppercase tracking-widest text-white/40">
          Pendapatan & Pengeluaran Per Hari — {{ monthNames[selectedMonth - 1] }} {{ selectedYear }}
        </h3>

        <div v-if="isLoadingChart" class="text-center py-12 text-white/30 text-xs animate-pulse">Memuat data grafik...</div>

        <div v-else class="space-y-2">
          <!-- Bar Chart Sederhana -->
          <div class="flex items-end gap-1 h-40 overflow-x-auto pb-2">
            <div
              v-for="d in monthlyData"
              :key="d.date"
              class="flex flex-col items-center gap-1 min-w-[28px] flex-1"
              :title="`${d.date}\nPendapatan: Rp ${formatNumber(d.revenue)}\nPengeluaran: Rp ${formatNumber(d.expenses)}\nLaba: Rp ${formatNumber(d.net_profit)}`"
            >
              <!-- Revenue bar -->
              <div class="w-full rounded-t transition-all duration-500"
                :style="{ height: barHeight(d.revenue, maxMonthlyRevenue) + 'px', background: '#10b981', minHeight: d.revenue > 0 ? '4px' : '0' }">
              </div>
              <!-- Expense bar -->
              <div class="w-full rounded-t transition-all duration-500"
                :style="{ height: barHeight(d.expenses, maxMonthlyRevenue) * 0.6 + 'px', background: '#f59e0b', minHeight: d.expenses > 0 ? '4px' : '0' }">
              </div>
              <span class="text-[8px] text-white/30 font-mono">{{ d.day }}</span>
            </div>
          </div>
          <div class="flex gap-4 text-[10px]">
            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-emerald-500 inline-block"></span>Pendapatan</span>
            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-amber-500 inline-block"></span>Pengeluaran</span>
          </div>
        </div>
      </div>

      <!-- Tabel detail per hari -->
      <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse min-w-[500px]">
            <thead class="bg-white/5 border-b border-white/5">
              <tr class="text-white/30 text-[10px] font-bold uppercase tracking-widest">
                <th class="px-6 py-4">Tanggal</th>
                <th class="px-6 py-4 text-right">Pendapatan</th>
                <th class="px-6 py-4 text-right">Pengeluaran</th>
                <th class="px-6 py-4 text-right">Laba Bersih</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5 text-xs">
              <tr v-for="d in monthlyDataFiltered" :key="d.date" class="hover:bg-white/5 transition-colors">
                <td class="px-6 py-3 font-mono text-white/70">{{ d.date }}</td>
                <td class="px-6 py-3 text-right font-mono font-bold text-emerald-400">
                  {{ d.revenue > 0 ? 'Rp ' + formatNumber(d.revenue) : '-' }}
                </td>
                <td class="px-6 py-3 text-right font-mono text-amber-400">
                  {{ d.expenses > 0 ? 'Rp ' + formatNumber(d.expenses) : '-' }}
                </td>
                <td class="px-6 py-3 text-right font-mono font-bold"
                  :class="d.net_profit >= 0 ? 'text-white' : 'text-red-400'">
                  Rp {{ formatNumber(d.net_profit) }}
                </td>
              </tr>
              <tr v-if="!monthlyDataFiltered.length">
                <td colspan="4" class="p-8 text-center text-white/20 text-xs">Tidak ada data untuk bulan ini.</td>
              </tr>
              <!-- Row total -->
              <tr v-if="monthlyDataFiltered.length" class="bg-white/5 font-bold border-t border-white/10">
                <td class="px-6 py-3 text-white/50 text-[10px] uppercase tracking-wider">Total Bulan</td>
                <td class="px-6 py-3 text-right font-mono text-emerald-400">Rp {{ formatNumber(summaryCards.revenue) }}</td>
                <td class="px-6 py-3 text-right font-mono text-amber-400">Rp {{ formatNumber(summaryCards.expenses) }}</td>
                <td class="px-6 py-3 text-right font-mono" :class="summaryCards.net_profit >= 0 ? 'text-white' : 'text-red-400'">
                  Rp {{ formatNumber(summaryCards.net_profit) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Export untuk mode monthly -->
      <div class="flex gap-3 justify-end">
        <button @click="exportDocument('excel', selectedMonth, selectedYear)"
          class="px-4 py-2.5 bg-emerald-600/10 hover:bg-emerald-600/20 border border-emerald-500/20 rounded-xl text-xs font-bold text-emerald-400 uppercase tracking-wider transition">
          📥 Export Excel Bulan Ini
        </button>
        <button @click="exportDocument('pdf', selectedMonth, selectedYear)"
          class="px-4 py-2.5 bg-red-600/10 hover:bg-red-600/20 border border-red-500/20 rounded-xl text-xs font-bold text-red-500 uppercase tracking-wider transition">
          📄 Export PDF Bulan Ini
        </button>
      </div>
    </div>

    <!-- GRAFIK TAHUNAN (per bulan dalam 1 tahun) -->
    <div v-if="viewMode === 'yearly'" class="space-y-6">
      <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 space-y-4">
        <h3 class="font-oswald text-xs uppercase tracking-widest text-white/40">
          Pendapatan & Pengeluaran Per Bulan — Tahun {{ selectedYear }}
        </h3>

        <div v-if="isLoadingChart" class="text-center py-12 text-white/30 text-xs animate-pulse">Memuat data grafik...</div>

        <div v-else class="space-y-2">
          <!-- Bar Chart 12 Bulan -->
          <div class="flex items-end gap-2 h-48">
            <div
              v-for="d in yearlyData"
              :key="d.month"
              class="flex flex-col items-center gap-1 flex-1"
              :title="`${d.month_name}\nPendapatan: Rp ${formatNumber(d.revenue)}\nPengeluaran: Rp ${formatNumber(d.expenses)}`"
            >
              <div class="w-full flex flex-col justify-end gap-0.5 flex-1">
                <div class="w-full rounded-t transition-all duration-700"
                  :style="{ height: barHeight(d.revenue, maxYearlyRevenue) + 'px', background: '#10b981', minHeight: d.revenue > 0 ? '4px' : '0' }">
                </div>
                <div class="w-full rounded-t transition-all duration-700"
                  :style="{ height: barHeight(d.expenses, maxYearlyRevenue) * 0.6 + 'px', background: '#f59e0b', minHeight: d.expenses > 0 ? '4px' : '0' }">
                </div>
              </div>
              <span class="text-[8px] text-white/30 font-mono">{{ d.month_name.slice(0, 3) }}</span>
            </div>
          </div>
          <div class="flex gap-4 text-[10px]">
            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-emerald-500 inline-block"></span>Pendapatan</span>
            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-amber-500 inline-block"></span>Pengeluaran</span>
          </div>
        </div>
      </div>

      <!-- Tabel 12 bulan -->
      <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse min-w-[500px]">
            <thead class="bg-white/5 border-b border-white/5">
              <tr class="text-white/30 text-[10px] font-bold uppercase tracking-widest">
                <th class="px-6 py-4">Bulan</th>
                <th class="px-6 py-4 text-right">Pendapatan</th>
                <th class="px-6 py-4 text-right">Pengeluaran</th>
                <th class="px-6 py-4 text-right">Laba Bersih</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5 text-xs">
              <tr v-for="d in yearlyData" :key="d.month" class="hover:bg-white/5 transition-colors"
                :class="d.revenue === 0 && d.expenses === 0 ? 'opacity-30' : ''">
                <td class="px-6 py-3 font-bold text-white/80">{{ d.month_name }}</td>
                <td class="px-6 py-3 text-right font-mono font-bold text-emerald-400">
                  {{ d.revenue > 0 ? 'Rp ' + formatNumber(d.revenue) : '-' }}
                </td>
                <td class="px-6 py-3 text-right font-mono text-amber-400">
                  {{ d.expenses > 0 ? 'Rp ' + formatNumber(d.expenses) : '-' }}
                </td>
                <td class="px-6 py-3 text-right font-mono font-bold"
                  :class="d.net_profit >= 0 ? 'text-white' : 'text-red-400'">
                  {{ (d.revenue > 0 || d.expenses > 0) ? 'Rp ' + formatNumber(d.net_profit) : '-' }}
                </td>
              </tr>
              <!-- Row total tahunan -->
              <tr class="bg-white/5 font-bold border-t border-white/10">
                <td class="px-6 py-3 text-white/50 text-[10px] uppercase tracking-wider">Total Tahun {{ selectedYear }}</td>
                <td class="px-6 py-3 text-right font-mono text-emerald-400">Rp {{ formatNumber(summaryCards.revenue) }}</td>
                <td class="px-6 py-3 text-right font-mono text-amber-400">Rp {{ formatNumber(summaryCards.expenses) }}</td>
                <td class="px-6 py-3 text-right font-mono" :class="summaryCards.net_profit >= 0 ? 'text-white' : 'text-red-400'">
                  Rp {{ formatNumber(summaryCards.net_profit) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Export untuk mode yearly -->
      <div class="flex gap-3 justify-end">
        <button @click="exportDocument('excel', null, selectedYear)"
          class="px-4 py-2.5 bg-emerald-600/10 hover:bg-emerald-600/20 border border-emerald-500/20 rounded-xl text-xs font-bold text-emerald-400 uppercase tracking-wider transition">
          📥 Export Excel Tahun {{ selectedYear }}
        </button>
        <button @click="exportDocument('pdf', null, selectedYear)"
          class="px-4 py-2.5 bg-red-600/10 hover:bg-red-600/20 border border-red-500/20 rounded-xl text-xs font-bold text-red-500 uppercase tracking-wider transition">
          📄 Export PDF Tahun {{ selectedYear }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import apiClient from "@/api/client";
import { toast } from "vue-sonner";

// ── Constants ────────────────────────────────────────────────────────────────
const monthNames = [
  "Januari","Februari","Maret","April","Mei","Juni",
  "Juli","Agustus","September","Oktober","November","Desember"
];

const viewModes = [
  { key: "daily",   label: "Harian" },
  { key: "monthly", label: "Bulanan" },
  { key: "yearly",  label: "Tahunan" },
];

// ── State ────────────────────────────────────────────────────────────────────
const viewMode      = ref("daily");
const currentDate   = ref(new Date());
const selectedMonth = ref(new Date().getMonth() + 1);
const selectedYear  = ref(new Date().getFullYear());
const yearsAvailable = ref([new Date().getFullYear()]);

const financialSummary  = ref({ revenue: 0, expenses: 0, net_profit: 0 });
const dailyExpensesList = ref([]);
const monthlyData       = ref([]);
const yearlyData        = ref([]);
const isLoadingChart    = ref(false);
const isSubmittingExpense = ref(false);
const expenseForm = ref({ description: "", amount: null });

// Export controls
const exportMonth = ref(new Date().getMonth() + 1);
const exportYear  = ref(new Date().getFullYear());

// ── Computed ─────────────────────────────────────────────────────────────────
const targetDateString = computed(() => {
  const yyyy = currentDate.value.getFullYear();
  const mm   = String(currentDate.value.getMonth() + 1).padStart(2, '0');
  const dd   = String(currentDate.value.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
});

const viewModeLabel = computed(() => {
  if (viewMode.value === "daily")   return `Per Tanggal — ${targetDateString.value}`;
  if (viewMode.value === "monthly") return `Per Hari — ${monthNames[selectedMonth.value - 1]} ${selectedYear.value}`;
  return `Per Bulan — Tahun ${selectedYear.value}`;
});

const summaryCards = computed(() => {
  if (viewMode.value === "daily") return financialSummary.value;
  if (viewMode.value === "monthly") {
    const rev = monthlyData.value.reduce((a, d) => a + d.revenue, 0);
    const exp = monthlyData.value.reduce((a, d) => a + d.expenses, 0);
    return { revenue: rev, expenses: exp, net_profit: rev - exp };
  }
  const rev = yearlyData.value.reduce((a, d) => a + d.revenue, 0);
  const exp = yearlyData.value.reduce((a, d) => a + d.expenses, 0);
  return { revenue: rev, expenses: exp, net_profit: rev - exp };
});

const monthlyDataFiltered = computed(() =>
  monthlyData.value.filter(d => d.revenue > 0 || d.expenses > 0)
);

const maxMonthlyRevenue = computed(() =>
  Math.max(...monthlyData.value.map(d => Math.max(d.revenue, d.expenses)), 1)
);

const maxYearlyRevenue = computed(() =>
  Math.max(...yearlyData.value.map(d => Math.max(d.revenue, d.expenses)), 1)
);

// ── Methods ───────────────────────────────────────────────────────────────────
const formatNumber = (v) => Math.round(v || 0).toLocaleString("id-ID");

const barHeight = (value, max, maxPx = 140) => {
  if (!max || max === 0) return 0;
  return Math.max(0, (value / max) * maxPx);
};

const switchMode = (mode) => {
  viewMode.value = mode;
  if (mode === "daily")   fetchDailyData();
  if (mode === "monthly") fetchMonthlyData();
  if (mode === "yearly")  fetchYearlyData();
};

// ── Navigation ────────────────────────────────────────────────────────────────
const changeDate = (days) => {
  const d = new Date(currentDate.value);
  d.setDate(d.getDate() + days);
  currentDate.value = d;
  fetchDailyData();
};

const changeMonth = (delta) => {
  let m = selectedMonth.value + delta;
  let y = selectedYear.value;
  if (m < 1) { m = 12; y--; }
  if (m > 12) { m = 1; y++; }
  selectedMonth.value = m;
  selectedYear.value = y;
  fetchMonthlyData();
};

const changeYear = (delta) => {
  selectedYear.value += delta;
  fetchYearlyData();
};

// ── Fetch ─────────────────────────────────────────────────────────────────────
const fetchDailyData = async () => {
  try {
    const [summaryRes, expenseRes] = await Promise.all([
      apiClient.get("/orders/admin_dashboard_daily_stats/", {
        params: { target_date: targetDateString.value },
      }),
      apiClient.get("/expenses/", {
        params: { date: targetDateString.value },
      }),
    ]);
    financialSummary.value  = summaryRes.data;
    dailyExpensesList.value = expenseRes.data;
  } catch (error) {
    console.error("Gagal memuat data harian:", error);
    toast.error("Gagal memuat data finansial harian.");
  }
};

const fetchMonthlyData = async () => {
  isLoadingChart.value = true;
  try {
    const { data } = await apiClient.get("/orders/finance/daily/", {
      params: { year: selectedYear.value, month: selectedMonth.value },
    });
    monthlyData.value = data.data;
    if (data.years_available) yearsAvailable.value = data.years_available;
  } catch (error) {
    console.error("Gagal memuat data bulanan:", error);
    toast.error("Gagal memuat data bulanan.");
  } finally {
    isLoadingChart.value = false;
  }
};

const fetchYearlyData = async () => {
  isLoadingChart.value = true;
  try {
    const { data } = await apiClient.get("/orders/finance/monthly/", {
      params: { year: selectedYear.value },
    });
    yearlyData.value = data.data;
    if (data.years_available) yearsAvailable.value = data.years_available;
  } catch (error) {
    console.error("Gagal memuat data tahunan:", error);
    toast.error("Gagal memuat data tahunan.");
  } finally {
    isLoadingChart.value = false;
  }
};

// ── Expense CRUD ──────────────────────────────────────────────────────────────
const submitExpense = async () => {
  if (!expenseForm.value.description || !expenseForm.value.amount) return;
  isSubmittingExpense.value = true;
  try {
    await apiClient.post("/expenses/", {
      description: expenseForm.value.description,
      amount:      expenseForm.value.amount,
      date:        targetDateString.value,
    });
    toast.success("Pengeluaran berhasil dicatat!");
    expenseForm.value = { description: "", amount: null };
    fetchDailyData();
  } catch {
    toast.error("Gagal mencatat pengeluaran.");
  } finally {
    isSubmittingExpense.value = false;
  }
};

const deleteExpense = async (id) => {
  if (!confirm("Hapus catatan pengeluaran ini?")) return;
  try {
    await apiClient.delete(`/expenses/${id}/`);
    toast.success("Pengeluaran dihapus.");
    fetchDailyData();
  } catch {
    toast.error("Gagal menghapus pengeluaran.");
  }
};

// ── Export ────────────────────────────────────────────────────────────────────
const exportDocument = (type, month = null, year = null) => {
  const m = month ?? exportMonth.value;
  const y = year  ?? exportYear.value;
  const endpoint = type === 'excel' ? 'export_excel_report' : 'export_pdf_report';
  const url = `${apiClient.defaults.baseURL}/orders/${endpoint}/?month=${m}&year=${y}`;
  window.open(url, '_blank');
  toast.success(`Mengunduh laporan ${type.toUpperCase()}...`);
};

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  await fetchDailyData();
  // Pre-load years available dari yearly endpoint
  try {
    const { data } = await apiClient.get("/orders/finance/monthly/", {
      params: { year: selectedYear.value },
    });
    if (data.years_available) yearsAvailable.value = data.years_available;
    yearlyData.value = data.data;
  } catch {}
});
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
input[type=number] { -moz-appearance: textfield; }
</style>