<template>
  <div class="p-8 text-white">
    <h1 class="text-2xl font-bold mb-6">New Order (POS)</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <h2 class="text-lg font-semibold mb-4">Pilih Menu</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div
            v-for="menu in menus"
            :key="menu.id"
            class="bg-[#0a0a0a] p-4 rounded-xl border border-white/5 hover:border-primary transition cursor-pointer"
            @click="addToOrder(menu)"
          >
            <h3 class="font-bold truncate">{{ menu.name }}</h3>
            <p class="text-primary text-sm">{{ formatPrice(menu.price) }}</p>
          </div>
        </div>
      </div>

      <div class="bg-[#0a0a0a] p-6 rounded-2xl border border-white/5 h-fit">
        <h2 class="text-lg font-semibold mb-4">Ringkasan Pesanan</h2>

        <div class="mb-4">
          <input
            v-model="customerPhone"
            @blur="checkLoyalty"
            placeholder="Nomor WhatsApp Pelanggan"
            class="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-sm focus:outline-none focus:border-primary transition"
          />
          <p v-if="isLoyal" class="text-green-500 text-xs mt-1">
            ✓ Pelanggan Loyal (Diskon {{ discountPercent }}%)
          </p>
        </div>

        <div
          v-if="orderItems.length === 0"
          class="text-white/30 text-center py-10"
        >
          Belum ada pesanan
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="(item, index) in orderItems"
            :key="index"
            class="flex items-center justify-between gap-2"
          >
            <div class="flex-1">
              <p class="text-sm font-medium truncate">{{ item.name }}</p>
              <p class="text-xs text-white/50">{{ formatPrice(item.price) }}</p>
            </div>

            <div class="flex items-center gap-1 bg-white/5 rounded-lg p-1">
              <button
                @click="updateQty(index, -1)"
                class="w-6 h-6 flex items-center justify-center hover:bg-white/10 rounded"
              >
                -
              </button>
              <input
                type="number"
                v-model.number="item.quantity"
                class="w-10 text-center bg-transparent text-sm focus:outline-none"
                @change="validateQty(index)"
              />
              <button
                @click="updateQty(index, 1)"
                class="w-6 h-6 flex items-center justify-center hover:bg-white/10 rounded"
              >
                +
              </button>
            </div>
          </div>

          <div class="border-t border-white/10 pt-4 space-y-2">
            <div class="flex justify-between text-sm">
              <span>Subtotal</span>
              <span>{{ formatPrice(subtotal) }}</span>
            </div>
            <div
              v-if="isLoyal"
              class="flex justify-between text-sm text-red-500"
            >
              <span>Diskon ({{ discountPercent }}%)</span>
              <span>-{{ formatPrice(discountAmount) }}</span>
            </div>
            <div
              class="flex justify-between font-bold text-lg pt-2 border-t border-white/10"
            >
              <span>Total</span>
              <span class="text-primary">{{ formatPrice(totalPrice) }}</span>
            </div>
          </div>

          <button
            @click="submitOrder"
            class="w-full bg-primary py-3 rounded-xl font-bold hover:bg-red-700 transition"
          >
            Proses Pesanan
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { menuAPI, orderAPI } from "@/api";
import { toast } from "vue-sonner";
import axios from "axios";

const menus = ref([]);
const orderItems = ref([]);
const customerPhone = ref("");
const isLoyal = ref(false);
const discountPercent = ref(0);

const subtotal = computed(() =>
  orderItems.value.reduce((acc, item) => acc + item.price * item.quantity, 0),
);
const discountAmount = computed(() =>
  isLoyal.value ? (subtotal.value * discountPercent.value) / 100 : 0,
);
const totalPrice = computed(() => subtotal.value - discountAmount.value);

const fetchMenus = async () => {
  const res = await menuAPI.getAll();
  menus.value = res.data;
};

const checkLoyalty = async () => {
  if (!customerPhone.value) return;
  try {
    const { data } = await axios.get(
      `/api/orders/check-loyalty/?phone=${customerPhone.value}`,
    );
    isLoyal.value = data.is_loyal;
    discountPercent.value = data.discount_percent;
  } catch (e) {
    isLoyal.value = false;
  }
};

const addToOrder = (menu) => {
  const existing = orderItems.value.find((i) => i.id === menu.id);
  if (existing) existing.quantity++;
  else orderItems.value.push({ ...menu, quantity: 1 });
};

const updateQty = (index, delta) => {
  orderItems.value[index].quantity += delta;
  if (orderItems.value[index].quantity <= 0) orderItems.value.splice(index, 1);
};

const validateQty = (index) => {
  if (orderItems.value[index].quantity < 1) orderItems.value.splice(index, 1);
};

const submitOrder = async () => {
  if (orderItems.value.length === 0) return toast.error("Keranjang kosong!");

  try {
    const payload = {
      phone: customerPhone.value || "ANON",
      payment_method: "cash",
      total_price: totalPrice.value,
      items: orderItems.value.map((item) => ({
        menu_id: item.id,
        quantity: item.quantity,
      })),
    };

    await orderAPI.create(payload);
    toast.success("Pesanan berhasil dibuat!");
    orderItems.value = [];
    customerPhone.value = "";
    isLoyal.value = false;
  } catch (e) {
    toast.error("Gagal simpan pesanan");
  }
};

const formatPrice = (p) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(p);

fetchMenus();
</script>
