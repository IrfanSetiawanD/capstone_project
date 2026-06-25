<template>
  <div class="p-8 text-white max-w-6xl mx-auto">
    <h1 class="text-3xl font-oswald mb-6">Riwayat Transaksi</h1>

    <div class="flex gap-2 mb-6">
      <button @click="period = 'today'" :class="period === 'today' ? 'bg-primary' : 'bg-white/5'" class="px-4 py-2 rounded-xl">Hari Ini</button>
      <button @click="period = 'week'"  :class="period === 'week'  ? 'bg-primary' : 'bg-white/5'" class="px-4 py-2 rounded-xl">Minggu Ini</button>
      <button @click="period = 'month'" :class="period === 'month' ? 'bg-primary' : 'bg-white/5'" class="px-4 py-2 rounded-xl">Bulan Ini</button>
    </div>

    <div class="space-y-3">
      <div
        v-for="order in orders"
        :key="order.id"
        class="bg-[#0a0a0a] border border-white/5 p-4 rounded-xl"
      >
        <div class="flex justify-between">
          <div>
            <p class="font-bold">{{ order.order_number }}</p>
            <p class="text-xs text-white/40">{{ order.customer_name || 'Walk In' }}</p>
            <p class="text-xs text-white/30 font-mono">{{ order.created_time }}</p>
          </div>
          <div class="text-right">
            <!-- FIX: gunakan total_price bukan final_price -->
            <p class="text-primary font-bold">{{ formatPrice(order.total_price) }}</p>
            <p class="text-xs text-white/40">{{ order.payment_status }}</p>
            <p class="text-xs text-white/30">{{ order.payment_method || '-' }}</p>
          </div>
        </div>

        <!-- Detail item -->
        <div v-if="order.items?.length" class="mt-3 pt-3 border-t border-white/5 space-y-1">
          <div v-for="item in order.items" :key="item.id" class="flex justify-between text-xs text-white/50">
            <span>{{ item.quantity }}x {{ item.menu_name }}</span>
            <span>{{ formatPrice(item.price * item.quantity) }}</span>
          </div>
        </div>
      </div>

      <div v-if="!orders.length" class="text-center text-white/30 py-16">
        Tidak ada riwayat transaksi untuk periode ini.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import apiClient from "@/api/client";

const orders = ref([]);
const period = ref("today");

const fetchHistory = async () => {
  try {
    const { data } = await apiClient.get("/orders/history/", {
      params: { period: period.value }
    });
    orders.value = data;
  } catch (err) {
    console.error(err);
  }
};

watch(period, fetchHistory);
onMounted(fetchHistory);

const formatPrice = (value) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency", currency: "IDR", minimumFractionDigits: 0,
  }).format(value || 0);
</script>