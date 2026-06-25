<template>
  <div class="w-full">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col md:flex-row justify-between items-end mb-12 gap-6">
        <div>
          <h1 class="font-oswald text-5xl uppercase italic tracking-tighter text-red-600">
            Menu Reports
          </h1>
          <p class="text-white/40 text-sm font-light mt-1">
            Analisis performa produk dan tren penjualan bulanan
          </p>
        </div>

        <div class="flex gap-4">
          <div class="relative group">
            <select
              v-model="selectedMonth"
              @change="fetchReportData"
              class="appearance-none bg-[#0a0a0a] border border-white/10 rounded-xl px-6 py-3 text-xs font-oswald uppercase tracking-widest outline-none focus:border-red-600 transition-all pr-12 text-white"
            >
              <option v-for="m in monthOptions" :key="m.value" :value="m.value">
                {{ m.label }}
              </option>
            </select>
            <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-white/20">
              <ChevronDown size="14" />
            </div>
          </div>

          <button
            @click="exportDocument('pdf')"
            class="flex items-center gap-2 bg-white/5 border border-white/10 px-6 py-3 rounded-xl text-[10px] font-oswald uppercase tracking-widest hover:bg-white/10 transition-all text-white"
          >
            <Download size="14" class="text-red-500" /> Export PDF
          </button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-20 text-white/30">Memuat data laporan...</div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div class="bg-[#0a0a0a] border border-white/5 p-10 rounded-3xl h-[450px] flex flex-col hover:border-red-500/20 transition-all duration-500">
          <div class="flex justify-between items-start mb-12">
            <h3 class="font-oswald uppercase text-white/40 text-xs tracking-widest flex items-center gap-2">
              <TrendingUp size="16" class="text-red-500" /> Ringkasan Performa
            </h3>
          </div>

          <div class="flex-grow flex flex-col justify-center">
            <apexchart 
              type="bar" 
              height="250" 
              :options="performanceOptions" 
              :series="performanceSeries"
            ></apexchart>
          </div>
        </div>

        <div class="bg-[#0a0a0a] border border-white/5 p-10 rounded-3xl flex flex-col hover:border-amber-500/20 transition-all duration-500">
          <h3 class="font-oswald uppercase text-white/40 text-xs tracking-widest mb-10 flex items-center gap-2">
            <Award size="16" class="text-amber-500" /> Top 5 Menu Terlaris
          </h3>

          <div class="space-y-10">
            <div v-for="item in topMenus" :key="item.menu__name" class="space-y-3">
              <div class="flex justify-between text-sm items-end">
                <span class="font-oswald text-white uppercase tracking-tight">{{ item.menu__name }}</span>
                <span class="text-amber-400 font-bold text-xs">{{ item.total_qty }} Porsi</span>
              </div>
              <div class="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                <div class="bg-amber-500 h-full transition-all duration-1000 ease-out" 
                     :style="{ width: (item.total_qty / Math.max(...topMenus.map(m=>m.total_qty)) * 100) + '%' }">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import VueApexCharts from 'vue3-apexcharts';
import { TrendingUp, Award, Download, ChevronDown } from "lucide-vue-next";
import apiClient from "@/api/client";

const loading = ref(true);
const totalRevenue = ref(0);
const totalOrders = ref(0);
const topMenus = ref([]);
const selectedMonth = ref(new Date().getMonth() + 1);
const selectedYear = ref(new Date().getFullYear());
const apexchart = VueApexCharts;

const performanceOptions = computed(() => ({
  chart: { 
    toolbar: { show: false },
    animations: { enabled: true, easing: 'easeinout', speed: 800 }
  },
  plotOptions: { bar: { borderRadius: 6, columnWidth: '40%' } },
  xaxis: { categories: ['Revenue', 'Orders'] },
  colors: ['#dc2626'],
  tooltip: {
    theme: 'dark',
    y: { formatter: (val) => val.toLocaleString('id-ID') }
  },
  dataLabels: { enabled: false }
}));

const performanceSeries = computed(() => [{
  name: 'Jumlah',
  data: [totalRevenue.value, totalOrders.value]
}]);

const monthOptions = [
  { label: "Januari 2026", value: 1 },
  { label: "Februari 2026", value: 2 },
  { label: "Maret 2026", value: 3 },
  { label: "April 2026", value: 4 },
];

const fetchReportData = async () => {
  loading.value = true;
  try {
    const { data } = await apiClient.get("/orders/reports/", {
      params: { month: selectedMonth.value, year: selectedYear.value }
    });
    totalRevenue.value = data.total_revenue;
    totalOrders.value = data.total_orders;
    topMenus.value = data.top_menus;
  } catch (err) {
    console.error("Gagal load report", err);
  } finally {
    loading.value = false;
  }
};

const exportDocument = (type) => {
  const url = `${apiClient.defaults.baseURL}/orders/export_${type}_report/?month=${selectedMonth.value}&year=${selectedYear.value}`;
  window.open(url, '_blank');
};

onMounted(fetchReportData);
</script>