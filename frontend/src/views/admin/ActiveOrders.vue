<template>
  <div class="p-8 text-white max-w-6xl mx-auto">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold font-oswald tracking-wide">Active Orders</h1>
        <p class="text-sm text-white/40 mt-1 flex items-center gap-2">
          📅 Kalender Operasional:
          <span class="text-red-400 font-semibold">{{ formattedCurrentDate }}</span>
        </p>
      </div>

      <div class="flex items-center gap-2 bg-[#0a0a0a] border border-white/5 p-1.5 rounded-2xl">
        <button @click="changeDate(-1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold tracking-wider uppercase transition">◀️ Kemarin</button>
        <div class="px-3 text-xs font-mono font-bold tracking-widest text-white/80">{{ targetDateString }}</div>
        <button @click="changeDate(1)" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold tracking-wider uppercase transition">Besok ▶️</button>
      </div>

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

    <div class="bg-[#0a0a0a] rounded-3xl border border-white/5 overflow-hidden shadow-2xl">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-white/5 text-white/50 text-xs uppercase tracking-wider">
            <th class="p-6">ID</th>
            <th class="p-6">Customer (No HP)</th>
            <th class="p-6">Total Tagihan</th>
            <th class="p-6">Status Order</th>
            <th class="p-6">Pembayaran</th>
            <th class="p-6">Metode</th>
            <th class="p-6 text-center">Waktu</th>
            <th class="p-6 text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr
            v-for="order in filteredOrders"
            :key="order.id"
            @click="openOrderModal(order)"
            class="hover:bg-white/5 transition cursor-pointer group"
          >
            <td class="p-6 font-bold text-red-500 group-hover:text-red-400 transition">#{{ order.id }}</td>
            <td class="p-6 font-mono text-sm">{{ order.customer_phone || "Guest (Tanpa Member)" }}</td>
            <td class="p-6 font-medium text-white/90">{{ formatPrice(order.total_price) }}</td>
            <td class="p-6">
              <span
                class="px-3 py-1 rounded-full text-[10px] font-bold tracking-wider"
                :class="order.status === 'completed'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'"
              >
                {{ order.status?.toUpperCase() }}
              </span>
            </td>
            <td class="p-6">
              <span
                class="px-3 py-1 rounded-full text-[10px] font-bold tracking-wider"
                :class="order.payment_status === 'paid'
                  ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                  : 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'"
              >
                {{ (order.payment_status || 'PENDING').toUpperCase() }}
              </span>
            </td>
            <td class="p-6 text-sm font-medium text-white/70 capitalize">{{ order.payment_method || 'Cash' }}</td>
            <td class="p-6 text-center text-white/40 text-xs font-mono">{{ formatTime(order.created_at) }}</td>

            <!-- Kolom Aksi: tombol Lunasi untuk order yang belum bayar -->
            <td class="p-6 text-center" @click.stop>
              <button
                v-if="order.payment_status !== 'paid'"
                @click="openPayModal(order)"
                class="px-4 py-2 bg-primary hover:bg-red-700 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition"
              >
                Lunasi
              </button>
              <span v-else class="text-white/20 text-xs">—</span>
            </td>
          </tr>

          <tr v-if="filteredOrders.length === 0">
            <td colspan="8" class="p-12 text-center text-white/30 text-sm font-medium">
              Tidak ada antrean pesanan aktif untuk tanggal {{ targetDateString }}.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL STRUK -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-[#0f0f0f] border border-white/10 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <div class="p-6 overflow-y-auto flex-1 font-mono text-xs text-zinc-300 space-y-4">
          <div class="text-center space-y-2">
            <img src="/src/assets/masashimura-logo.png" alt="Masashimura Logo" class="h-14 mx-auto object-contain mb-1" onerror="this.style.display='none'" />
            <h2 class="text-base font-bold text-white uppercase tracking-wider">MASASHIMURA</h2>
            <p class="text-[10px] text-zinc-500">Jl. Pintu air no 48 Depan Pengadilan bekasi, Bekasi, Jawa Barat</p>
            <p class="text-zinc-600">========================================</p>
          </div>

          <div class="grid grid-cols-2 gap-y-1 text-[11px]">
            <div>No. Nota : <span class="text-white font-bold">{{ selectedOrder?.order_number }}</span></div>
            <div class="text-right">Kasir: <span class="text-white">Staff</span></div>
            <div>Waktu : <span>{{ formatFullDateTime(selectedOrder?.created_at) }}</span></div>
            <div class="text-right truncate">Pelanggan: <span class="text-white">{{ selectedOrder?.customer_name || selectedOrder?.customer_phone || 'Guest' }}</span></div>
          </div>
          <p class="text-zinc-600 text-center">----------------------------------------</p>

          <div class="space-y-3">
            <p class="font-bold text-white text-[11px] uppercase tracking-wide">Detail Pesanan:</p>
            <div v-for="(item, idx) in selectedOrder?.items" :key="idx" class="space-y-0.5">
              <div class="flex justify-between text-white">
                <span>{{ item.quantity }}x {{ item.menu_name }}</span>
                <span>{{ formatPrice(item.price * item.quantity) }}</span>
              </div>
              <div v-if="item.notes" class="text-amber-400 text-[10px] pl-4 italic">📋 "{{ item.notes }}"</div>
            </div>
          </div>
          <p class="text-zinc-600 text-center">----------------------------------------</p>

          <div class="space-y-1.5 text-[11px]">
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span>{{ formatPrice(selectedOrder?.subtotal) }}</span>
            </div>
            <div v-if="parseFloat(selectedOrder?.discount_amount) > 0" class="flex justify-between text-red-400">
              <span>Diskon Member</span>
              <span>-{{ formatPrice(selectedOrder?.discount_amount) }}</span>
            </div>
            <p class="text-zinc-600 text-center">----------------------------------------</p>
            <div class="flex justify-between text-sm font-bold text-white">
              <span>TOTAL AKHIR</span>
              <span class="text-red-500">{{ formatPrice(selectedOrder?.total_price) }}</span>
            </div>
          </div>
          <p class="text-zinc-600 text-center">========================================</p>

          <div class="bg-white/5 p-3 rounded-xl border border-white/5 space-y-1 text-[10px]">
            <div>• Metode Bayar : <span class="text-white font-bold uppercase">{{ selectedOrder?.payment_method || 'Cash' }}</span></div>
            <div>• Status :
              <span :class="selectedOrder?.payment_status === 'paid' ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'">
                {{ (selectedOrder?.payment_status || 'PENDING').toUpperCase() }}
              </span>
            </div>
          </div>
        </div>

        <div class="p-4 bg-[#0a0a0a] border-t border-white/5 grid grid-cols-2 gap-3">
          <button @click="shareToWhatsApp" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition">
            🟢 Bagikan via WA
          </button>
          <button @click="isModalOpen = false" class="w-full bg-white/5 hover:bg-white/10 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition">
            Tutup Struk
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL LUNASI PEMBAYARAN -->
    <div v-if="isPayModalOpen && selectedPayOrder"
      class="fixed inset-0 z-[60] bg-black/70 flex items-center justify-center p-5"
      @click.self="isPayModalOpen = false">
      <div class="bg-[#0b0b0b] w-full max-w-md rounded-2xl border border-white/10 p-6 space-y-5">
        <div class="flex justify-between items-center">
          <h2 class="font-oswald text-xl">💳 Lunasi Pembayaran</h2>
          <button @click="isPayModalOpen = false" class="text-white/40 hover:text-white">✕</button>
        </div>

        <div class="space-y-1 text-sm">
          <p class="font-mono font-bold text-primary">{{ selectedPayOrder.order_number }}</p>
          <p class="text-white/70">{{ selectedPayOrder.customer_name || "Walk In" }}</p>
          <p class="text-white/40 text-xs">{{ selectedPayOrder.customer_phone || "-" }}</p>
        </div>

        <div class="flex justify-between text-sm border-t border-white/5 pt-3">
          <span class="text-white/50">Total Tagihan</span>
          <span class="font-bold text-primary font-mono text-lg">{{ formatPrice(selectedPayOrder.total_price) }}</span>
        </div>

        <div class="space-y-2">
          <label class="text-[10px] uppercase text-white/40 font-bold tracking-wider">Metode Pembayaran</label>
          <div class="grid grid-cols-2 gap-2">
            <button @click="payMethod = 'cash'"
              class="py-3 rounded-xl border font-bold text-sm transition"
              :class="payMethod === 'cash' ? 'bg-primary border-primary text-white' : 'border-white/10 text-white/50'">
              💵 Cash
            </button>
            <button @click="payMethod = 'qris_manual'"
              class="py-3 rounded-xl border font-bold text-sm transition"
              :class="payMethod === 'qris_manual' ? 'bg-primary border-primary text-white' : 'border-white/10 text-white/50'">
              📱 QRIS
            </button>
          </div>
        </div>

        <button @click="confirmPay" :disabled="isPaying"
          class="w-full py-3.5 rounded-xl bg-primary hover:bg-red-700 disabled:opacity-40 font-bold uppercase tracking-widest text-sm transition">
          {{ isPaying ? "Memproses..." : "Konfirmasi Lunas" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { orderAPI, apiClient } from "@/api";
import { toast } from "vue-sonner";

const currentDate    = ref(new Date());
const orders         = ref([]);
const searchQuery    = ref("");
const isModalOpen    = ref(false);
const selectedOrder  = ref(null);
let pollingTimer     = null;

// State modal lunasi
const isPayModalOpen    = ref(false);
const selectedPayOrder  = ref(null);
const payMethod         = ref("cash");
const isPaying          = ref(false);

const formattedCurrentDate = computed(() =>
  currentDate.value.toLocaleDateString('id-ID', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })
);

const targetDateString = computed(() => {
  const yyyy = currentDate.value.getFullYear();
  const mm   = String(currentDate.value.getMonth() + 1).padStart(2, '0');
  const dd   = String(currentDate.value.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
});

const changeDate = (days) => {
  const newDate = new Date(currentDate.value);
  newDate.setDate(newDate.getDate() + days);
  currentDate.value = newDate;
  fetchActiveOrders();
};

const fetchActiveOrders = async () => {
  try {
    const res = await orderAPI.getActiveOrders(targetDateString.value);
    orders.value = res.data;
  } catch (error) {
    console.error("Gagal tarik data:", error);
  }
};

const filteredOrders = computed(() =>
  orders.value.filter(o => (o.customer_phone || "").includes(searchQuery.value))
);

const openOrderModal = (order) => {
  selectedOrder.value = order;
  isModalOpen.value   = true;
};

// Buka modal lunasi — hentikan propagasi agar tidak buka modal struk
const openPayModal = (order) => {
  selectedPayOrder.value = order;
  payMethod.value        = order.payment_method || "cash";
  isPayModalOpen.value   = true;
};

const confirmPay = async () => {
  if (!selectedPayOrder.value) return;
  isPaying.value = true;
  try {
    await apiClient.patch(`/orders/${selectedPayOrder.value.id}/pay/`, {
      payment_method: payMethod.value,
    });
    toast.success(`Order ${selectedPayOrder.value.order_number} berhasil dilunasi`);
    isPayModalOpen.value   = false;
    selectedPayOrder.value = null;
    fetchActiveOrders();
  } catch (err) {
    toast.error("Gagal melunasi pembayaran");
    console.error(err);
  } finally {
    isPaying.value = false;
  }
};

// Share WA dari struk
const shareToWhatsApp = () => {
  if (!selectedOrder.value) return;
  const order = selectedOrder.value;
  const phone = order.customer_phone || "";

  let text = `*MASASHIMURA BEKASI*\n=========================\n`;
  text += `*No. Nota :* ${order.order_number}\n`;
  text += `*Waktu :* ${formatFullDateTime(order.created_at)}\n`;
  text += `*Pelanggan :* ${order.customer_name || phone || 'Guest'}\n`;
  text += `-------------------------\n`;

  order.items?.forEach(item => {
    text += `• ${item.quantity}x ${item.menu_name} = ${formatPrice(item.price * item.quantity)}\n`;
    if (item.notes) text += `  _(${item.notes})_\n`;
  });

  text += `-------------------------\n`;
  if (parseFloat(order.discount_amount) > 0) {
    text += `*Diskon :* -${formatPrice(order.discount_amount)}\n`;
  }
  text += `*TOTAL :* ${formatPrice(order.total_price)}\n`;
  text += `*Status :* ${(order.payment_status || 'PENDING').toUpperCase()}\n`;

  const target = phone.startsWith('0') ? '62' + phone.slice(1) : phone;
  window.open(`https://api.whatsapp.com/send?phone=${target}&text=${encodeURIComponent(text)}`, '_blank');
};

const formatPrice = (p) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(p || 0);

const formatTime = (dateTimeStr) =>
  new Date(dateTimeStr).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

const formatFullDateTime = (dateTimeStr) =>
  new Date(dateTimeStr).toLocaleString('id-ID', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  }) + ' WIB';

onMounted(() => {
  fetchActiveOrders();
  pollingTimer = setInterval(fetchActiveOrders, 5000);
});

onUnmounted(() => {
  if (pollingTimer) clearInterval(pollingTimer);
});
</script>