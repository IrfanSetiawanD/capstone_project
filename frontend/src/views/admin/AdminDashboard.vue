<template>
  <div class="w-full p-8">
    <div class="mb-12">
      <h1
        class="font-oswald text-5xl uppercase tracking-tighter italic text-red-600"
      >
        Admin Dashboard
      </h1>
      <p class="text-white/40 text-sm font-light">
        Monitoring Bisnis Masashimura Bekasi
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
        <p
          class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald"
        >
          Total Pendapatan
        </p>
        <h3 class="text-2xl font-oswald font-bold text-emerald-400">
          {{ formatPrice(stats.total_revenue) }}
        </h3>
      </div>

      <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
        <p
          class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald"
        >
          Total Pesanan
        </p>
        <h3 class="text-2xl font-oswald font-bold text-white">
          {{ stats.total_orders }}
        </h3>
      </div>

      <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
        <p
          class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald"
        >
          Menu Terlaris
        </p>
        <h3 class="text-lg font-oswald font-bold truncate text-amber-400">
          {{ stats.top_menus?.[0]?.name || "-" }}
        </h3>
      </div>

      <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
        <p
          class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald"
        >
          Pelanggan Loyal
        </p>
        <h3 class="text-2xl font-oswald font-bold text-white">
          {{ stats.loyal_users?.length || 0 }}
        </h3>
      </div>
    </div>

    <div class="mt-12">
      <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-8">
        <h2 class="text-xl font-oswald uppercase text-white/50 mb-4">
          Analisis Tren Pendapatan
        </h2>
        <div
          class="h-64 flex items-center justify-center border border-dashed border-white/10 rounded-xl text-white/20"
        >
          <span>Visualisasi Grafik Sedang Disiapkan</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { statsAPI } from "@/api";

const auth = useAuthStore();
const router = useRouter();

const stats = ref({
  total_revenue: 0,
  total_orders: 0,
  top_menus: [],
  loyal_users: [],
});

const formatPrice = (price) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(price || 0);

const fetchAdminStats = async () => {
  try {
    const res = await statsAPI.getDashboardSummary();
    if (res.data) stats.value = res.data;
  } catch (err) {
    console.warn("Stats endpoint belum siap, menggunakan data default.");
  }
};

onMounted(() => {
  if (!auth.user) {
    router.push("/login");
    return;
  }
  fetchAdminStats();
});
</script>
