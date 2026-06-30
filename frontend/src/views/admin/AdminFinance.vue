<template>
  <div class="fr-root">

    <!-- ── PAGE HEADER ─────────────────────────────────────────────── -->
    <div class="fr-header">
      <div>
        <p class="fr-eyebrow">Masashimura · Keuangan</p>
        <h1 class="fr-title">Financial Reports</h1>
        <p class="fr-subtitle">{{ viewModeLabel }}</p>
      </div>

      <!-- Mode switcher -->
      <div class="mode-switch">
        <button
          v-for="m in viewModes"
          :key="m.key"
          @click="switchMode(m.key)"
          class="mode-btn"
          :class="{ active: viewMode === m.key }"
        >
          {{ m.label }}
        </button>
      </div>
    </div>

    <!-- ── DATE NAVIGATOR ─────────────────────────────────────────── -->
    <div class="nav-bar">
      <!-- HARIAN -->
      <template v-if="viewMode === 'daily'">
        <div class="date-nav">
          <button class="nav-btn" @click="changeDate(-1)">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
            Kemarin
          </button>
          <span class="nav-current">{{ targetDateString }}</span>
          <button class="nav-btn" @click="changeDate(1)">
            Besok
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>
      </template>

      <!-- BULANAN -->
      <template v-if="viewMode === 'monthly'">
        <div class="date-nav">
          <button class="nav-btn" @click="changeMonth(-1)">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <span class="nav-current">{{ monthNames[selectedMonth - 1] }} {{ selectedYear }}</span>
          <button class="nav-btn" @click="changeMonth(1)">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>
        <select v-model.number="selectedYear" @change="fetchMonthlyData" class="nav-select">
          <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
        </select>
      </template>

      <!-- TAHUNAN -->
      <template v-if="viewMode === 'yearly'">
        <div class="date-nav">
          <button class="nav-btn" @click="changeYear(-1)">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <span class="nav-current">Tahun {{ selectedYear }}</span>
          <button class="nav-btn" @click="changeYear(1)">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>
        <select v-model.number="selectedYear" @change="fetchYearlyData" class="nav-select">
          <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
        </select>
      </template>
    </div>

    <!-- ── SUMMARY CARDS ──────────────────────────────────────────── -->
    <div class="summary-grid">
      <div class="s-card s-green">
        <div class="s-top">
          <span class="s-label">Total Pendapatan</span>
          <span class="s-dot dot-green"></span>
        </div>
        <div class="s-value">Rp {{ formatNumber(summaryCards.revenue) }}</div>
        <div class="s-note">Order lunas terkonfirmasi</div>
      </div>

      <div class="s-card s-amber">
        <div class="s-top">
          <span class="s-label">Total Pengeluaran</span>
          <span class="s-dot dot-amber"></span>
        </div>
        <div class="s-value">Rp {{ formatNumber(summaryCards.expenses) }}</div>
        <div class="s-note">Dari buku kas harian</div>
      </div>

      <div class="s-card s-profit" :class="summaryCards.net_profit >= 0 ? 's-surplus' : 's-defisit'">
        <div class="s-top">
          <span class="s-label">Laba Bersih</span>
          <span class="s-badge" :class="summaryCards.net_profit >= 0 ? 'badge-up' : 'badge-down'">
            {{ summaryCards.net_profit >= 0 ? '▲ Surplus' : '▼ Defisit' }}
          </span>
        </div>
        <div class="s-value" :class="summaryCards.net_profit >= 0 ? 'val-green' : 'val-red'">
          Rp {{ formatNumber(summaryCards.net_profit) }}
        </div>
        <div class="s-note">Pendapatan dikurangi pengeluaran</div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         MODE HARIAN
    ══════════════════════════════════════════════ -->
    <div v-if="viewMode === 'daily'" class="daily-layout">

      <!-- Form Input Pengeluaran -->
      <div class="card expense-form-card">
        <div class="card-head">
          <p class="card-eyebrow">Catat Biaya</p>
          <h3 class="card-title">Input Pengeluaran</h3>
        </div>
        <form @submit.prevent="submitExpense" class="expense-form">
          <div class="field">
            <label class="field-label">Keterangan</label>
            <input
              v-model="expenseForm.description"
              type="text"
              placeholder="Beli Daging, Gas 3kg, dll."
              required
              class="field-input"
            />
          </div>
          <div class="field">
            <label class="field-label">Nominal (Rp)</label>
            <input
              v-model.number="expenseForm.amount"
              type="number"
              placeholder="150000"
              required
              min="1"
              class="field-input font-mono"
            />
          </div>
          <button type="submit" :disabled="isSubmittingExpense" class="submit-btn">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
            {{ isSubmittingExpense ? 'Menyimpan...' : 'Catat Pengeluaran' }}
          </button>
        </form>
      </div>

      <!-- Kolom kanan: Export + Log -->
      <div class="daily-right">

        <!-- Export Panel -->
        <div class="card export-card">
          <div class="export-head">
            <div>
              <p class="card-eyebrow">Unduh Laporan</p>
              <h3 class="card-title">Export Dokumen</h3>
            </div>
            <div class="export-toggle">
              <button @click="exportMode = 'monthly'" class="toggle-btn" :class="{ active: exportMode === 'monthly' }">Bulanan</button>
              <button @click="exportMode = 'yearly'"  class="toggle-btn" :class="{ active: exportMode === 'yearly'  }">Tahunan</button>
            </div>
          </div>

          <div class="export-controls">
            <select v-if="exportMode === 'monthly'" v-model.number="exportMonth" class="nav-select">
              <option v-for="(name, idx) in monthNames" :key="idx" :value="idx + 1">{{ name }}</option>
            </select>
            <select v-model.number="exportYear" class="nav-select">
              <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
            </select>
            <span class="export-period-label">
              {{ exportMode === 'monthly' ? `${monthNames[exportMonth - 1]} ${exportYear}` : `Tahun ${exportYear}` }}
            </span>
          </div>

          <div class="export-btns">
            <button @click="exportDocument('excel')" :disabled="isExporting" class="export-btn btn-excel">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
              {{ isExporting ? 'Mengunduh...' : 'Excel' }}
            </button>
            <button @click="exportDocument('pdf')" :disabled="isExporting" class="export-btn btn-pdf">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
              {{ isExporting ? 'Mengunduh...' : 'PDF' }}
            </button>
          </div>
        </div>

        <!-- Log Pengeluaran -->
        <div class="card table-card">
          <div class="card-head border-b">
            <p class="card-eyebrow">Rincian Hari Ini</p>
            <h3 class="card-title">Log Pengeluaran — {{ targetDateString }}</h3>
          </div>
          <div class="table-scroll">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Keterangan</th>
                  <th class="th-right">Nominal</th>
                  <th class="th-center">Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="exp in dailyExpensesList" :key="exp.id" class="data-row">
                  <td class="td-desc">{{ exp.description }}</td>
                  <td class="td-right td-amount">−Rp {{ formatNumber(exp.amount) }}</td>
                  <td class="td-center">
                    <button @click="deleteExpense(exp.id)" class="delete-btn">Hapus</button>
                  </td>
                </tr>
                <tr v-if="!dailyExpensesList.length">
                  <td colspan="3" class="empty-cell">
                    <div class="empty-icon">📋</div>
                    <p>Belum ada pengeluaran hari ini</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         MODE BULANAN
    ══════════════════════════════════════════════ -->
    <div v-if="viewMode === 'monthly'" class="section-stack">

      <!-- Bar chart -->
      <div class="card chart-card">
        <div class="card-head">
          <p class="card-eyebrow">Visualisasi</p>
          <h3 class="card-title">Pendapatan & Pengeluaran Per Hari — {{ monthNames[selectedMonth - 1] }} {{ selectedYear }}</h3>
        </div>

        <div v-if="isLoadingChart" class="chart-loading">
          <div class="spinner-sm"></div>
          <span>Memuat grafik...</span>
        </div>

        <div v-else class="chart-area">
          <div class="bar-chart">
            <div
              v-for="d in monthlyData"
              :key="d.date"
              class="bar-col"
              :title="`${d.date}\nPendapatan: Rp ${formatNumber(d.revenue)}\nPengeluaran: Rp ${formatNumber(d.expenses)}`"
            >
              <div class="bar-pair">
                <div class="bar bar-rev" :style="{ height: barHeight(d.revenue, maxMonthlyRevenue) + 'px' }"></div>
                <div class="bar bar-exp" :style="{ height: barHeight(d.expenses, maxMonthlyRevenue) * 0.6 + 'px' }"></div>
              </div>
              <span class="bar-label">{{ d.day }}</span>
            </div>
          </div>
          <div class="chart-legend">
            <span class="legend-item"><span class="legend-dot ld-green"></span>Pendapatan</span>
            <span class="legend-item"><span class="legend-dot ld-amber"></span>Pengeluaran</span>
          </div>
        </div>
      </div>

      <!-- Table per hari -->
      <div class="card table-card">
        <div class="card-head border-b">
          <p class="card-eyebrow">Detail Harian</p>
          <h3 class="card-title">{{ monthNames[selectedMonth - 1] }} {{ selectedYear }}</h3>
        </div>
        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th>Tanggal</th>
                <th class="th-right">Pendapatan</th>
                <th class="th-right">Pengeluaran</th>
                <th class="th-right">Laba Bersih</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="d in monthlyDataFiltered" :key="d.date" class="data-row">
                <td class="td-mono">{{ d.date }}</td>
                <td class="td-right td-rev">{{ d.revenue > 0 ? 'Rp ' + formatNumber(d.revenue) : '—' }}</td>
                <td class="td-right td-exp">{{ d.expenses > 0 ? 'Rp ' + formatNumber(d.expenses) : '—' }}</td>
                <td class="td-right" :class="d.net_profit >= 0 ? 'td-pos' : 'td-neg'">Rp {{ formatNumber(d.net_profit) }}</td>
              </tr>
              <tr v-if="!monthlyDataFiltered.length">
                <td colspan="4" class="empty-cell"><p>Tidak ada data untuk bulan ini</p></td>
              </tr>
              <tr v-if="monthlyDataFiltered.length" class="total-row">
                <td>Total Bulan</td>
                <td class="td-right td-rev">Rp {{ formatNumber(summaryCards.revenue) }}</td>
                <td class="td-right td-exp">Rp {{ formatNumber(summaryCards.expenses) }}</td>
                <td class="td-right" :class="summaryCards.net_profit >= 0 ? 'td-pos' : 'td-neg'">Rp {{ formatNumber(summaryCards.net_profit) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Export strip -->
      <div class="card export-strip">
        <div class="export-strip-left">
          <p class="card-title">Export Laporan</p>
          <p class="s-note">Periode aktif: <span class="period-highlight">{{ monthNames[selectedMonth - 1] }} {{ selectedYear }}</span></p>
        </div>
        <div class="export-strip-right">
          <div class="export-toggle">
            <button @click="exportMode = 'monthly'" class="toggle-btn" :class="{ active: exportMode === 'monthly' }">Bulanan</button>
            <button @click="exportMode = 'yearly'"  class="toggle-btn" :class="{ active: exportMode === 'yearly'  }">Tahunan</button>
          </div>
          <select v-if="exportMode === 'monthly'" v-model.number="exportMonth" class="nav-select">
            <option v-for="(name, idx) in monthNames" :key="idx" :value="idx + 1">{{ name }}</option>
          </select>
          <select v-model.number="exportYear" class="nav-select">
            <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
          </select>
          <button @click="exportDocument('excel')" :disabled="isExporting" class="export-btn btn-excel">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
            Excel
          </button>
          <button @click="exportDocument('pdf')" :disabled="isExporting" class="export-btn btn-pdf">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
            PDF
          </button>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         MODE TAHUNAN
    ══════════════════════════════════════════════ -->
    <div v-if="viewMode === 'yearly'" class="section-stack">

      <!-- Bar chart tahunan -->
      <div class="card chart-card">
        <div class="card-head">
          <p class="card-eyebrow">Visualisasi</p>
          <h3 class="card-title">Pendapatan & Pengeluaran Per Bulan — Tahun {{ selectedYear }}</h3>
        </div>

        <div v-if="isLoadingChart" class="chart-loading">
          <div class="spinner-sm"></div>
          <span>Memuat grafik...</span>
        </div>

        <div v-else class="chart-area">
          <div class="bar-chart bar-chart-yearly">
            <div
              v-for="d in yearlyData"
              :key="d.month"
              class="bar-col"
              :title="`${d.month_name}\nPendapatan: Rp ${formatNumber(d.revenue)}\nPengeluaran: Rp ${formatNumber(d.expenses)}`"
            >
              <div class="bar-pair">
                <div class="bar bar-rev" :style="{ height: barHeight(d.revenue, maxYearlyRevenue) + 'px' }"></div>
                <div class="bar bar-exp" :style="{ height: barHeight(d.expenses, maxYearlyRevenue) * 0.6 + 'px' }"></div>
              </div>
              <span class="bar-label">{{ d.month_name.slice(0, 3) }}</span>
            </div>
          </div>
          <div class="chart-legend">
            <span class="legend-item"><span class="legend-dot ld-green"></span>Pendapatan</span>
            <span class="legend-item"><span class="legend-dot ld-amber"></span>Pengeluaran</span>
          </div>
        </div>
      </div>

      <!-- Table 12 bulan -->
      <div class="card table-card">
        <div class="card-head border-b">
          <p class="card-eyebrow">Rekap Tahunan</p>
          <h3 class="card-title">Tahun {{ selectedYear }}</h3>
        </div>
        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th>Bulan</th>
                <th class="th-right">Pendapatan</th>
                <th class="th-right">Pengeluaran</th>
                <th class="th-right">Laba Bersih</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="d in yearlyData"
                :key="d.month"
                class="data-row"
                :class="{ 'row-empty': d.revenue === 0 && d.expenses === 0 }"
              >
                <td class="td-month">{{ d.month_name }}</td>
                <td class="td-right td-rev">{{ d.revenue > 0 ? 'Rp ' + formatNumber(d.revenue) : '—' }}</td>
                <td class="td-right td-exp">{{ d.expenses > 0 ? 'Rp ' + formatNumber(d.expenses) : '—' }}</td>
                <td class="td-right" :class="d.net_profit >= 0 ? 'td-pos' : 'td-neg'">
                  {{ (d.revenue > 0 || d.expenses > 0) ? 'Rp ' + formatNumber(d.net_profit) : '—' }}
                </td>
              </tr>
              <tr class="total-row">
                <td>Total {{ selectedYear }}</td>
                <td class="td-right td-rev">Rp {{ formatNumber(summaryCards.revenue) }}</td>
                <td class="td-right td-exp">Rp {{ formatNumber(summaryCards.expenses) }}</td>
                <td class="td-right" :class="summaryCards.net_profit >= 0 ? 'td-pos' : 'td-neg'">Rp {{ formatNumber(summaryCards.net_profit) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Export strip -->
      <div class="card export-strip">
        <div class="export-strip-left">
          <p class="card-title">Export Laporan</p>
          <p class="s-note">Periode aktif: <span class="period-highlight">Tahun {{ selectedYear }}</span></p>
        </div>
        <div class="export-strip-right">
          <div class="export-toggle">
            <button @click="exportMode = 'monthly'" class="toggle-btn" :class="{ active: exportMode === 'monthly' }">Bulanan</button>
            <button @click="exportMode = 'yearly'"  class="toggle-btn" :class="{ active: exportMode === 'yearly'  }">Tahunan</button>
          </div>
          <select v-if="exportMode === 'monthly'" v-model.number="exportMonth" class="nav-select">
            <option v-for="(name, idx) in monthNames" :key="idx" :value="idx + 1">{{ name }}</option>
          </select>
          <select v-model.number="exportYear" class="nav-select">
            <option v-for="y in yearsAvailable" :key="y" :value="y">{{ y }}</option>
          </select>
          <button @click="exportDocument('excel')" :disabled="isExporting" class="export-btn btn-excel">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
            Excel
          </button>
          <button @click="exportDocument('pdf')" :disabled="isExporting" class="export-btn btn-pdf">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
            PDF
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import apiClient from "@/api/client";
import { toast } from "vue-sonner";

const monthNames = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"];
const viewModes  = [{ key: "daily", label: "Harian" }, { key: "monthly", label: "Bulanan" }, { key: "yearly", label: "Tahunan" }];

const viewMode       = ref("daily");
const currentDate    = ref(new Date());
const selectedMonth  = ref(new Date().getMonth() + 1);
const selectedYear   = ref(new Date().getFullYear());
const yearsAvailable = ref([new Date().getFullYear()]);

const financialSummary    = ref({ revenue: 0, expenses: 0, net_profit: 0 });
const dailyExpensesList   = ref([]);
const monthlyData         = ref([]);
const yearlyData          = ref([]);
const isLoadingChart      = ref(false);
const isSubmittingExpense = ref(false);
const isExporting         = ref(false);
const expenseForm         = ref({ description: "", amount: null });

const exportMode  = ref("monthly");
const exportMonth = ref(new Date().getMonth() + 1);
const exportYear  = ref(new Date().getFullYear());

const targetDateString = computed(() => {
  const d = currentDate.value;
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
});
const viewModeLabel = computed(() => {
  if (viewMode.value === "daily")   return `Per Tanggal — ${targetDateString.value}`;
  if (viewMode.value === "monthly") return `Per Hari — ${monthNames[selectedMonth.value - 1]} ${selectedYear.value}`;
  return `Per Bulan — Tahun ${selectedYear.value}`;
});
const summaryCards = computed(() => {
  if (viewMode.value === "daily") return financialSummary.value;
  const src = viewMode.value === "monthly" ? monthlyData.value : yearlyData.value;
  const rev = src.reduce((a, d) => a + (d.revenue  || 0), 0);
  const exp = src.reduce((a, d) => a + (d.expenses || 0), 0);
  return { revenue: rev, expenses: exp, net_profit: rev - exp };
});
const monthlyDataFiltered = computed(() => monthlyData.value.filter(d => d.revenue > 0 || d.expenses > 0));
const maxMonthlyRevenue   = computed(() => Math.max(...monthlyData.value.map(d => Math.max(d.revenue || 0, d.expenses || 0)), 1));
const maxYearlyRevenue    = computed(() => Math.max(...yearlyData.value.map(d => Math.max(d.revenue || 0, d.expenses || 0)), 1));

const formatNumber = (v) => Math.round(v || 0).toLocaleString("id-ID");
const barHeight    = (value, max, maxPx = 140) => max ? Math.max(0, ((value || 0) / max) * maxPx) : 0;

const switchMode = (mode) => {
  viewMode.value = mode;
  if (mode === "monthly") { exportMode.value = "monthly"; exportMonth.value = selectedMonth.value; exportYear.value = selectedYear.value; fetchMonthlyData(); }
  else if (mode === "yearly") { exportMode.value = "yearly"; exportYear.value = selectedYear.value; fetchYearlyData(); }
  else { fetchDailyData(); }
};
const changeDate  = (days) => { const d = new Date(currentDate.value); d.setDate(d.getDate() + days); currentDate.value = d; fetchDailyData(); };
const changeMonth = (delta) => { let m = selectedMonth.value + delta, y = selectedYear.value; if (m < 1) { m = 12; y--; } if (m > 12) { m = 1; y++; } selectedMonth.value = m; selectedYear.value = y; exportMonth.value = m; exportYear.value = y; fetchMonthlyData(); };
const changeYear  = (delta) => { selectedYear.value += delta; exportYear.value = selectedYear.value; fetchYearlyData(); };

const fetchDailyData = async () => {
  try {
    const [summaryRes, expenseRes] = await Promise.all([
      apiClient.get("/orders/admin_dashboard_daily_stats/", { params: { target_date: targetDateString.value } }),
      apiClient.get("/expenses/", { params: { date: targetDateString.value } }),
    ]);
    financialSummary.value  = summaryRes.data;
    dailyExpensesList.value = expenseRes.data;
  } catch (err) { console.error(err); toast.error("Gagal memuat data finansial harian."); }
};
const fetchMonthlyData = async () => {
  isLoadingChart.value = true;
  try {
    const { data } = await apiClient.get("/orders/finance/daily/", { params: { year: selectedYear.value, month: selectedMonth.value } });
    monthlyData.value = data.data;
    if (data.years_available) yearsAvailable.value = data.years_available;
  } catch (err) { console.error(err); toast.error("Gagal memuat data bulanan."); }
  finally { isLoadingChart.value = false; }
};
const fetchYearlyData = async () => {
  isLoadingChart.value = true;
  try {
    const { data } = await apiClient.get("/orders/finance/monthly/", { params: { year: selectedYear.value } });
    yearlyData.value = data.data;
    if (data.years_available) yearsAvailable.value = data.years_available;
  } catch (err) { console.error(err); toast.error("Gagal memuat data tahunan."); }
  finally { isLoadingChart.value = false; }
};
const submitExpense = async () => {
  if (!expenseForm.value.description || !expenseForm.value.amount) return;
  isSubmittingExpense.value = true;
  try {
    await apiClient.post("/expenses/", { description: expenseForm.value.description, amount: expenseForm.value.amount, date: targetDateString.value });
    expenseForm.value = { description: "", amount: null };
    await fetchDailyData();
    toast.success("Pengeluaran dicatat!");
  } catch { toast.error("Gagal mencatat pengeluaran."); }
  finally { isSubmittingExpense.value = false; }
};
const deleteExpense = async (id) => {
  if (!confirm("Hapus catatan pengeluaran ini?")) return;
  try { await apiClient.delete(`/expenses/${id}/`); toast.success("Pengeluaran dihapus."); fetchDailyData(); }
  catch { toast.error("Gagal menghapus pengeluaran."); }
};
const exportDocument = async (type) => {
  isExporting.value = true;
  const endpoint = type === "excel" ? "/orders/export/finance-excel/" : "/orders/export/finance-pdf/";
  const params   = new URLSearchParams({ mode: exportMode.value, year: exportYear.value });
  if (exportMode.value === "monthly") params.append("month", exportMonth.value);
  const url         = `${apiClient.defaults.baseURL}${endpoint}?${params.toString()}`;
  const periodLabel = exportMode.value === "monthly" ? `${monthNames[exportMonth.value - 1]} ${exportYear.value}` : `Tahun ${exportYear.value}`;
  try { window.open(url, "_blank"); toast.success(`Mengunduh laporan ${type.toUpperCase()} — ${periodLabel}`); }
  catch { toast.error("Gagal membuka link unduhan."); }
  finally { setTimeout(() => { isExporting.value = false; }, 1500); }
};

onMounted(async () => {
  await fetchDailyData();
  try {
    const { data } = await apiClient.get("/orders/finance/monthly/", { params: { year: selectedYear.value } });
    if (data.years_available) yearsAvailable.value = data.years_available;
    yearlyData.value = data.data;
  } catch {}
});
</script>

<style scoped>
/* ── Root ────────────────────────────────────────────────────────── */
.fr-root {
  min-height: 100vh;
  background: #080808;
  color: #fff;
  padding: 2rem 1.5rem;
  max-width: 1280px;
  margin: 0 auto;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ── Header ──────────────────────────────────────────────────────── */
.fr-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-wrap: wrap;
}
.fr-eyebrow {
  font-family: 'Oswald', sans-serif;
  font-size: 0.6rem; letter-spacing: 0.2em;
  text-transform: uppercase; color: #dc2626;
  margin: 0 0 0.3rem;
}
.fr-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1.75rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.04em;
  margin: 0 0 0.3rem;
}
.fr-subtitle { font-size: 0.7rem; color: rgba(255,255,255,0.3); margin: 0; font-family: monospace; }

.mode-switch {
  display: flex;
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 4px;
  gap: 2px;
}
.mode-btn {
  padding: 0.45rem 1.1rem;
  border-radius: 9px; border: none;
  background: transparent;
  color: rgba(255,255,255,0.35);
  font-family: 'Oswald', sans-serif;
  font-size: 0.7rem; letter-spacing: 0.1em;
  text-transform: uppercase; cursor: pointer;
  transition: all 0.15s;
}
.mode-btn:hover { color: rgba(255,255,255,0.7); }
.mode-btn.active { background: #dc2626; color: #fff; }

/* ── Nav bar ─────────────────────────────────────────────────────── */
.nav-bar { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
.date-nav {
  display: flex; align-items: center;
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px; overflow: hidden;
}
.nav-btn {
  display: flex; align-items: center; gap: 0.3rem;
  padding: 0.5rem 0.85rem;
  background: transparent; border: none;
  color: rgba(255,255,255,0.4);
  font-family: 'Oswald', sans-serif;
  font-size: 0.65rem; letter-spacing: 0.1em;
  text-transform: uppercase; cursor: pointer;
  transition: all 0.15s;
}
.nav-btn:hover { color: #fff; background: rgba(255,255,255,0.04); }
.nav-current {
  padding: 0.5rem 1rem;
  font-family: monospace; font-size: 0.82rem; color: #fff;
  border-left: 1px solid rgba(255,255,255,0.06);
  border-right: 1px solid rgba(255,255,255,0.06);
  white-space: nowrap;
}
.nav-select {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 0.5rem 0.85rem;
  color: #fff; font-family: monospace; font-size: 0.8rem;
  outline: none; cursor: pointer;
  transition: border-color 0.15s;
}
.nav-select:focus { border-color: rgba(220,38,38,0.5); }

/* ── Summary Cards ───────────────────────────────────────────────── */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
@media (max-width: 768px) { .summary-grid { grid-template-columns: 1fr; } }
@media (max-width: 1024px) and (min-width: 769px) { .summary-grid { grid-template-columns: repeat(3, 1fr); } }

.s-card {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 1.4rem 1.5rem;
  position: relative; overflow: hidden;
}
.s-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.s-green::before { background: #22c55e; }
.s-amber::before { background: #f59e0b; }
.s-surplus::before { background: #22c55e; }
.s-defisit::before { background: #ef4444; }

.s-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.s-label { font-family: 'Oswald', sans-serif; font-size: 0.62rem; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.35); }
.s-dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-green { background: #22c55e; }
.dot-amber { background: #f59e0b; }
.s-badge {
  font-size: 0.55rem; padding: 0.15rem 0.55rem; border-radius: 100px;
  font-family: 'Oswald', sans-serif; letter-spacing: 0.08em; text-transform: uppercase;
}
.badge-up   { background: rgba(34,197,94,0.1);  color: #4ade80; border: 1px solid rgba(34,197,94,0.2); }
.badge-down { background: rgba(239,68,68,0.1);  color: #f87171; border: 1px solid rgba(239,68,68,0.2); }

.s-value { font-family: monospace; font-size: 1.4rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; margin-bottom: 0.4rem; }
.val-green { color: #4ade80; }
.val-red   { color: #f87171; }
.s-note    { font-size: 0.68rem; color: rgba(255,255,255,0.2); }

/* ── Card base ───────────────────────────────────────────────────── */
.card {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  overflow: hidden;
}
.card-head {
  padding: 1.25rem 1.5rem;
}
.card-head.border-b { border-bottom: 1px solid rgba(255,255,255,0.05); }
.card-eyebrow {
  font-family: 'Oswald', sans-serif; font-size: 0.58rem;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #dc2626; margin: 0 0 0.2rem;
}
.card-title { font-family: 'Oswald', sans-serif; font-size: 0.9rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; margin: 0; color: rgba(255,255,255,0.85); }

/* ── Daily layout ────────────────────────────────────────────────── */
.daily-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 1rem;
  align-items: start;
}
@media (max-width: 900px) { .daily-layout { grid-template-columns: 1fr; } }

.daily-right { display: flex; flex-direction: column; gap: 1rem; }

/* Expense Form */
.expense-form-card .card-head { padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
.expense-form { padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-label { font-family: 'Oswald', sans-serif; font-size: 0.58rem; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(255,255,255,0.3); }
.field-input {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px; padding: 0.7rem 1rem;
  color: #fff; font-size: 0.85rem; font-family: 'Inter', sans-serif;
  outline: none; transition: border-color 0.15s;
}
.field-input::placeholder { color: rgba(255,255,255,0.2); }
.field-input:focus { border-color: rgba(220,38,38,0.45); }
.submit-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.4rem;
  padding: 0.75rem; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
  color: #fbbf24; font-family: 'Oswald', sans-serif;
  font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;
  cursor: pointer; transition: all 0.15s;
}
.submit-btn:hover:not(:disabled) { background: rgba(251,191,36,0.08); border-color: rgba(251,191,36,0.25); }
.submit-btn:disabled { opacity: 0.35; cursor: not-allowed; }

/* Export card */
.export-card { }
.export-head {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: 1.25rem 1.5rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.05);
  gap: 1rem; flex-wrap: wrap;
}
.export-toggle {
  display: flex; background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 3px; gap: 2px;
}
.toggle-btn {
  padding: 0.3rem 0.7rem; border-radius: 6px; border: none; background: transparent;
  color: rgba(255,255,255,0.35);
  font-family: 'Oswald', sans-serif; font-size: 0.62rem;
  letter-spacing: 0.1em; text-transform: uppercase; cursor: pointer; transition: all 0.15s;
}
.toggle-btn:hover { color: rgba(255,255,255,0.65); }
.toggle-btn.active { background: #dc2626; color: #fff; }
.export-controls {
  display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
  padding: 1rem 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.export-period-label {
  font-family: monospace; font-size: 0.75rem;
  color: rgba(255,255,255,0.25);
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px; padding: 0.4rem 0.75rem; white-space: nowrap;
}
.export-btns {
  display: flex; gap: 0.5rem; padding: 1rem 1.5rem;
}
.export-btn {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.4rem;
  padding: 0.65rem; border-radius: 10px; border: 1px solid;
  font-family: 'Oswald', sans-serif; font-size: 0.68rem;
  letter-spacing: 0.1em; text-transform: uppercase;
  cursor: pointer; transition: all 0.15s;
}
.export-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-excel { background: rgba(34,197,94,0.07); border-color: rgba(34,197,94,0.2); color: #4ade80; }
.btn-excel:hover:not(:disabled) { background: rgba(34,197,94,0.14); }
.btn-pdf   { background: rgba(220,38,38,0.07);  border-color: rgba(220,38,38,0.2);  color: #f87171; }
.btn-pdf:hover:not(:disabled)   { background: rgba(220,38,38,0.14); }

/* Table */
.table-scroll { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; min-width: 400px; }
.data-table th {
  padding: 0.65rem 1.25rem;
  font-family: 'Oswald', sans-serif; font-size: 0.58rem; font-weight: 400;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: rgba(255,255,255,0.22); text-align: left;
  background: rgba(255,255,255,0.015);
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.th-right  { text-align: right; }
.th-center { text-align: center; }

.data-row { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.12s; }
.data-row:hover { background: rgba(255,255,255,0.02); }
.data-row:last-child { border-bottom: none; }
.row-empty { opacity: 0.3; }

.data-table td { padding: 0.8rem 1.25rem; font-size: 0.82rem; vertical-align: middle; }
.td-mono   { font-family: monospace; color: rgba(255,255,255,0.65); }
.td-month  { font-weight: 600; color: rgba(255,255,255,0.8); }
.td-desc   { color: rgba(255,255,255,0.8); }
.td-right  { text-align: right; }
.td-center { text-align: center; }
.td-rev    { font-family: monospace; font-weight: 700; color: #4ade80; }
.td-exp    { font-family: monospace; color: #fbbf24; }
.td-amount { font-family: monospace; font-weight: 700; color: #fbbf24; }
.td-pos    { font-family: monospace; font-weight: 700; color: #fff; }
.td-neg    { font-family: monospace; font-weight: 700; color: #f87171; }

.total-row {
  background: rgba(255,255,255,0.03) !important;
  border-top: 1px solid rgba(255,255,255,0.08) !important;
}
.total-row td { font-family: 'Oswald', sans-serif; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.45); padding: 0.7rem 1.25rem; }
.total-row .td-rev, .total-row .td-exp, .total-row .td-pos, .total-row .td-neg { font-size: 0.82rem; }

.delete-btn {
  padding: 0.25rem 0.65rem; border-radius: 6px;
  background: rgba(239,68,68,0.07); border: 1px solid rgba(239,68,68,0.15);
  color: #f87171; font-family: 'Oswald', sans-serif;
  font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase;
  cursor: pointer; transition: all 0.15s;
}
.delete-btn:hover { background: rgba(239,68,68,0.15); }

.empty-cell { padding: 2.5rem !important; text-align: center; color: rgba(255,255,255,0.2); }
.empty-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.empty-cell p { margin: 0; font-size: 0.78rem; }

/* ── Chart ───────────────────────────────────────────────────────── */
.chart-card .card-head { border-bottom: 1px solid rgba(255,255,255,0.05); }
.chart-loading {
  display: flex; align-items: center; justify-content: center; gap: 0.6rem;
  padding: 3rem; color: rgba(255,255,255,0.25); font-size: 0.75rem;
  font-family: 'Oswald', sans-serif; letter-spacing: 0.1em; text-transform: uppercase;
}
.spinner-sm {
  width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.07);
  border-top-color: #dc2626; border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.chart-area { padding: 1.25rem 1.5rem 1rem; }
.bar-chart {
  display: flex; align-items: flex-end; gap: 3px;
  height: 150px; overflow-x: auto; padding-bottom: 0.5rem;
}
.bar-chart-yearly { gap: 6px; overflow-x: visible; }
.bar-col { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; flex: 1; min-width: 20px; }
.bar-pair { display: flex; flex-direction: column; justify-content: flex-end; gap: 2px; width: 100%; flex: 1; align-items: center; }
.bar { width: 100%; border-radius: 3px 3px 0 0; transition: height 0.5s ease; min-width: 6px; }
.bar-rev { background: #22c55e; }
.bar-exp { background: #f59e0b; opacity: 0.75; }
.bar-label { font-size: 0.55rem; font-family: monospace; color: rgba(255,255,255,0.25); white-space: nowrap; }
.chart-legend { display: flex; gap: 1.25rem; margin-top: 0.75rem; }
.legend-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.7rem; color: rgba(255,255,255,0.4); }
.legend-dot { width: 8px; height: 8px; border-radius: 2px; }
.ld-green { background: #22c55e; }
.ld-amber { background: #f59e0b; }

/* ── Export strip (monthly/yearly footer) ────────────────────────── */
.export-strip {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.5rem; flex-wrap: wrap; gap: 1rem;
}
.export-strip-left { display: flex; flex-direction: column; gap: 0.2rem; }
.export-strip-right {
  display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
}
.period-highlight { color: #dc2626; font-family: monospace; }

/* ── Section stack (monthly/yearly) ─────────────────────────────── */
.section-stack { display: flex; flex-direction: column; gap: 1rem; }

/* ── Responsive ─────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .fr-root { padding: 1.25rem 1rem; }
  .fr-header { flex-direction: column; }
  .fr-title { font-size: 1.4rem; }
  .export-strip { flex-direction: column; align-items: flex-start; }
  .export-strip-right { width: 100%; }
  .export-head { flex-direction: column; }
  .export-btns { flex-direction: row; }
}

/* Hide spinners */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
input[type=number] { -moz-appearance: textfield; }
</style>