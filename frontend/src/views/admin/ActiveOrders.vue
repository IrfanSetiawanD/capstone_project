<template>
  <div class="p-8 text-white max-w-6xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold font-oswald tracking-wide">
        Active Orders
      </h1>

      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari berdasarkan no HP..."
          class="w-full bg-[#0a0a0a] border border-white/10 rounded-xl py-3 pl-10 pr-4 text-sm focus:outline-none focus:border-red-600 transition"
        />
        <span class="absolute left-3 top-3.5 text-white/30">🔍</span>
      </div>
    </div>

    <div class="bg-[#0a0a0a] rounded-3xl border border-white/5 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-white/5 text-white/50 text-sm uppercase tracking-wider">
            <th class="p-6">ID</th>
            <th class="p-6">Customer</th>
            <th class="p-6">Total Price</th>
            <th class="p-6">Status</th>
            <th class="p-6 text-center">Waktu</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr
            v-for="order in filteredOrders"
            :key="order.id"
            @click="openOrderModal(order)"
            class="hover:bg-white/5 transition cursor-pointer"
          >
            <td class="p-6 font-bold text-red-500">#{{ order.id }}</td>
            <td class="p-6">{{ order.customer?.phone || "Guest" }}</td>
            <td class="p-6 font-medium">
              Rp {{ order.final_price?.toLocaleString() }}
            </td>
            <td class="p-6">
              <span
                class="px-3 py-1 rounded-full text-xs font-bold"
                :class="
                  order.status === 'selesai'
                    ? 'bg-emerald-500/20 text-emerald-500'
                    : 'bg-amber-500/20 text-amber-500'
                "
              >
                {{ order.status.toUpperCase() }}
              </span>
            </td>
            <td class="p-6 text-center text-white/40 text-sm">
              {{
                new Date(order.created_at).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <OrderEditModal
      :open="isModalOpen"
      :order="selectedOrder"
      @close="isModalOpen = false"
      @save="handleSaveOrder"
      @delete="handleDeleteOrder"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { orderAPI } from "@/api";
import OrderEditModal from "@/components/ui/modals/OrderEditModal.vue";

const orders = ref([]);
const searchQuery = ref("");
const isModalOpen = ref(false);
const selectedOrder = ref(null);

const fetchOrders = async () => {
  try {
    const res = await orderAPI.getAll();
    orders.value = res.data;
  } catch (error) {
    console.error(error);
  }
};

const filteredOrders = computed(() => {
  return orders.value.filter((o) =>
    (o.customer?.phone || "").includes(searchQuery.value),
  );
});

const openOrderModal = (order) => {
  selectedOrder.value = order;
  isModalOpen.value = true;
};

const handleSaveOrder = async (updatedOrder) => {
  // Logic untuk panggil API update
  await orderAPI.update(updatedOrder.id, updatedOrder);
  isModalOpen.value = false;
  fetchOrders();
};

const handleDeleteOrder = async (id) => {
  await orderAPI.delete(id);
  isModalOpen.value = false;
  fetchOrders();
};

onMounted(fetchOrders);
</script>
