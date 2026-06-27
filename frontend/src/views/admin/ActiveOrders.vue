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
        <button @click="changeDate(-1)"
          class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold tracking-wider uppercase transition">◀️
          Kemarin</button>
        <div class="px-3 text-xs font-mono font-bold tracking-widest text-white/80">{{ targetDateString }}</div>
        <button @click="changeDate(1)"
          class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-bold tracking-wider uppercase transition">Besok
          ▶️</button>
      </div>
      <div class="relative w-72">
        <input v-model="searchQuery" type="text" placeholder="Cari berdasarkan no HP..."
          class="w-full bg-[#0a0a0a] border border-white/10 rounded-xl py-3 pl-10 pr-4 text-sm focus:outline-none focus:border-red-600 transition" />
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
          <tr v-for="order in filteredOrders" :key="order.id" @click="openOrderModal(order)"
            class="hover:bg-white/5 transition cursor-pointer group">
            <td class="p-6 font-bold text-red-500 group-hover:text-red-400 transition">#{{ order.id }}</td>
            <td class="p-6 font-mono text-sm">{{ order.customer_phone || "Guest (Tanpa Member)" }}</td>
            <td class="p-6 font-medium text-white/90">{{ formatPrice(order.total_price) }}</td>
            <td class="p-6">
              <span class="px-3 py-1 rounded-full text-[10px] font-bold tracking-wider"
                :class="order.status === 'completed'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'">
                {{ order.status?.toUpperCase() }}
              </span>
            </td>
            <td class="p-6">
              <span class="px-3 py-1 rounded-full text-[10px] font-bold tracking-wider"
                :class="order.payment_status === 'paid'
                  ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                  : 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'">
                {{ (order.payment_status || 'PENDING').toUpperCase() }}
              </span>
            </td>
            <td class="p-6 text-sm font-medium text-white/70 capitalize">{{ order.payment_method || 'Cash' }}</td>
            <td class="p-6 text-center text-white/40 text-xs font-mono">{{ formatTime(order.created_at) }}</td>
            <td class="p-6 text-center" @click.stop>
              <button v-if="order.payment_status !== 'paid'" @click="openPayModal(order)"
                class="px-4 py-2 bg-primary hover:bg-red-700 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition">
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
    <div v-if="isModalOpen"
      class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div
        class="bg-[#0f0f0f] border border-white/10 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <div class="p-6 overflow-y-auto flex-1 font-mono text-xs text-zinc-300 space-y-4">
          <div class="text-center space-y-2">
            <!-- Logo saja, tanpa teks nama toko -->
            <img src="/src/assets/masashimura-logo.png" alt="Logo" class="h-16 mx-auto object-contain" />
            <p class="text-[10px] text-zinc-500">Jl. Pintu air no 48 Depan Pengadilan bekasi, Bekasi, Jawa Barat</p>
            <p class="text-zinc-600">========================================</p>
          </div>
          <div class="grid grid-cols-2 gap-y-1 text-[11px]">
            <div>No. Nota : <span class="text-white font-bold">{{ selectedOrder?.order_number }}</span></div>
            <div class="text-right">Kasir: <span class="text-white">{{ selectedOrder?.kasir_name || kasirName }}</span></div>
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
            <!-- FIX: subtotal fallback ke total_price jika 0/null -->
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span>{{ formatPrice(computedSubtotal) }}</span>
            </div>
            <div v-if="parseFloat(selectedOrder?.discount_amount) > 0" class="flex justify-between text-red-400">
              <span>Diskon Member</span><span>-{{ formatPrice(selectedOrder?.discount_amount) }}</span>
            </div>
            <p class="text-zinc-600 text-center">----------------------------------------</p>
            <div class="flex justify-between text-sm font-bold text-white">
              <span>TOTAL AKHIR</span>
              <span class="text-red-500">{{ formatPrice(selectedOrder?.total_price) }}</span>
            </div>
            <!-- Bayar & Kembalian di luar card, setelah total -->
            <div v-if="parseFloat(selectedOrder?.amount_paid) > 0" class="flex justify-between text-white/70 pt-1">
              <span>Bayar</span>
              <span class="text-white font-semibold">{{ formatPrice(selectedOrder.amount_paid) }}</span>
            </div>
            <div v-if="parseFloat(selectedOrder?.change_amount) > 0" class="flex justify-between">
              <span>Kembalian</span>
              <span class="text-emerald-400 font-bold">{{ formatPrice(selectedOrder.change_amount) }}</span>
            </div>
          </div>
          <p class="text-zinc-600 text-center">========================================</p>
          <!-- Card: hanya Metode + Kasir + Status -->
          <div class="bg-white/5 p-3 rounded-xl border border-white/5 space-y-1 text-[10px]">
            <div>• Metode Bayar : <span class="text-white font-bold uppercase">{{ selectedOrder?.payment_method || 'Cash' }}</span></div>
            <div>• Kasir : <span class="text-white font-bold">{{ selectedOrder?.kasir_name || kasirName }}</span></div>
            <div>• Status :
              <span :class="selectedOrder?.payment_status === 'paid' ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'">
                {{ (selectedOrder?.payment_status || 'PENDING').toUpperCase() }}
              </span>
            </div>
          </div>
        </div>
        <div class="p-4 bg-[#0a0a0a] border-t border-white/5 grid grid-cols-2 gap-3">
          <button @click="shareReceiptAsImage" :disabled="isCapturing"
            class="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition">
            {{ isCapturing ? '📸 Memproses...' : '🟢 Bagikan via WA' }}
          </button>
          <button @click="isModalOpen = false"
            class="w-full bg-white/5 hover:bg-white/10 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition">
            Tutup Struk
          </button>
        </div>
      </div>
    </div>

    <!--
      STRUK TERSEMBUNYI untuk screenshot WA.
      PENTING: tidak boleh ada class Tailwind sama sekali di sini.
      Tailwind v4 pakai oklch() di CSS variables-nya → html2canvas crash.
      Semua styling harus pakai inline style dengan warna hex/rgb biasa.
    -->
    <div
      ref="receiptRef"
      style="
        position: fixed;
        left: -9999px;
        top: 0;
        width: 400px;
        background-color: #0f0f0f;
        color: #d4d4d8;
        padding: 24px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        line-height: 1.6;
      "
    >
      <!-- Header: logo saja -->
      <div style="text-align:center; margin-bottom:16px;">
        <img
          src="/src/assets/masashimura-logo.png"
          alt="Logo"
          style="height:60px; margin:0 auto 8px; object-fit:contain; display:block;"
        />
        <div style="font-size:10px; color:#71717a;">Jl. Pintu air no 48 Depan Pengadilan bekasi, Bekasi, Jawa Barat</div>
        <div style="color:#3f3f46; margin-top:8px;">========================================</div>
      </div>

      <!-- Info nota -->
      <div style="font-size:11px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
          <span>No. Nota :</span>
          <span style="color:#ffffff; font-weight:700;">{{ selectedOrder?.order_number }}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
          <span>Kasir :</span>
          <span style="color:#ffffff;">{{ selectedOrder?.kasir_name || kasirName }}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
          <span>Waktu :</span>
          <span>{{ formatFullDateTime(selectedOrder?.created_at) }}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span>Pelanggan :</span>
          <span style="color:#ffffff;">{{ selectedOrder?.customer_name || selectedOrder?.customer_phone || 'Guest' }}</span>
        </div>
      </div>

      <div style="color:#3f3f46; margin-bottom:12px;">----------------------------------------</div>

      <!-- Detail pesanan -->
      <div style="margin-bottom:12px;">
        <div style="font-weight:700; color:#ffffff; font-size:11px; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">
          Detail Pesanan:
        </div>
        <div v-for="(item, idx) in selectedOrder?.items" :key="idx" style="margin-bottom:6px;">
          <div style="display:flex; justify-content:space-between; color:#ffffff;">
            <span>{{ item.quantity }}x {{ item.menu_name }}</span>
            <span>{{ formatPrice(item.price * item.quantity) }}</span>
          </div>
          <div v-if="item.notes" style="color:#f59e0b; font-size:10px; padding-left:12px; font-style:italic;">
            📋 "{{ item.notes }}"
          </div>
        </div>
      </div>

      <div style="color:#3f3f46; margin-bottom:12px;">----------------------------------------</div>

      <!-- Ringkasan harga -->
      <div style="font-size:11px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
          <span>Subtotal</span>
          <!-- FIX: fallback ke total_price jika subtotal 0/null -->
          <span>{{ formatPrice(computedSubtotal) }}</span>
        </div>
        <div v-if="parseFloat(selectedOrder?.discount_amount) > 0"
          style="display:flex; justify-content:space-between; color:#f87171; margin-bottom:4px;">
          <span>Diskon Member</span>
          <span>-{{ formatPrice(selectedOrder?.discount_amount) }}</span>
        </div>
        <div style="color:#3f3f46; margin:6px 0;">----------------------------------------</div>
        <div style="display:flex; justify-content:space-between; font-size:14px; font-weight:900; color:#ffffff; margin-bottom:6px;">
          <span>TOTAL AKHIR</span>
          <span style="color:#ef4444;">{{ formatPrice(selectedOrder?.total_price) }}</span>
        </div>
        <!-- Bayar & Kembalian di luar card, setelah total -->
        <div v-if="parseFloat(selectedOrder?.amount_paid) > 0"
          style="display:flex; justify-content:space-between; margin-bottom:2px; color:#a1a1aa;">
          <span>Bayar</span>
          <span style="color:#ffffff; font-weight:600;">{{ formatPrice(selectedOrder.amount_paid) }}</span>
        </div>
        <div v-if="parseFloat(selectedOrder?.change_amount) > 0"
          style="display:flex; justify-content:space-between;">
          <span>Kembalian</span>
          <span style="color:#34d399; font-weight:700;">{{ formatPrice(selectedOrder.change_amount) }}</span>
        </div>
      </div>

      <div style="color:#3f3f46; margin-bottom:12px;">========================================</div>

      <!-- Card: hanya Metode + Kasir + Status -->
      <div style="
        background-color: #1a1a1a;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #2a2a2a;
        font-size: 10px;
        line-height: 2;
        margin-bottom: 12px;
      ">
        <div>
          • Metode Bayar :
          <span style="color:#ffffff; font-weight:700; text-transform:uppercase;">
            {{ selectedOrder?.payment_method || 'Cash' }}
          </span>
        </div>
        <div>
          • Kasir :
          <span style="color:#ffffff; font-weight:700;">{{ selectedOrder?.kasir_name || kasirName }}</span>
        </div>
        <div>
          • Status :
          <span :style="selectedOrder?.payment_status === 'paid'
            ? 'color:#34d399; font-weight:700;'
            : 'color:#fbbf24; font-weight:700;'">
            {{ (selectedOrder?.payment_status || 'PENDING').toUpperCase() }}
          </span>
        </div>
      </div>

      <!-- Footer -->
      <div style="text-align:center; font-size:10px; color:#a1a1aa; padding-top:4px; font-weight:700;">
        Terima kasih sudah makan di Masashimura! 🙏
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
        <button @click="payMethod = 'cash'" class="py-3 rounded-xl border font-bold text-sm transition"
          :class="payMethod === 'cash' ? 'bg-primary border-primary text-white' : 'border-white/10 text-white/50'">
          💵 Cash
        </button>
        <button @click="payMethod = 'qris_manual'" class="py-3 rounded-xl border font-bold text-sm transition"
          :class="payMethod === 'qris_manual' ? 'bg-primary border-primary text-white' : 'border-white/10 text-white/50'">
          📱 QRIS
        </button>
      </div>
    </div>

    <!-- ++ TAMBAHAN: Input uang diterima (hanya muncul saat cash) -->
    <div v-if="payMethod === 'cash'" class="space-y-2">
      <label class="text-[10px] uppercase text-white/40 font-bold tracking-wider">Uang Diterima</label>
      <input
        v-model.number="payAmountPaid"
        type="number"
        placeholder="Nominal uang dari pelanggan..."
        class="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-sm focus:outline-none focus:border-primary transition text-white font-mono"
      />
      <!-- Kembalian -->
      <div
        v-if="payAmountPaid > 0 && payAmountPaid >= parseFloat(selectedPayOrder.total_price)"
        class="flex justify-between text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3"
      >
        <span>Kembalian</span>
        <span>{{ formatPrice(payAmountPaid - parseFloat(selectedPayOrder.total_price)) }}</span>
      </div>
      <!-- Kurang bayar -->
      <div
        v-else-if="payAmountPaid > 0 && payAmountPaid < parseFloat(selectedPayOrder.total_price)"
        class="text-xs text-red-400 font-mono px-1"
      >
        ⚠️ Kurang {{ formatPrice(parseFloat(selectedPayOrder.total_price) - payAmountPaid) }}
      </div>
    </div>

    <button @click="confirmPay" :disabled="isPaying || (payMethod === 'cash' && payAmountPaid > 0 && payAmountPaid < parseFloat(selectedPayOrder.total_price))"
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
import { useAuthStore } from '@/stores/auth';
import html2canvas from 'html2canvas';

const authStore = useAuthStore();
const kasirName = computed(() => authStore.user?.name || authStore.user?.username || 'Staff');
const payAmountPaid = ref(0);

const currentDate   = ref(new Date());
const orders        = ref([]);
const searchQuery   = ref("");
const isModalOpen   = ref(false);
const selectedOrder = ref(null);
const isCapturing   = ref(false);
const receiptRef    = ref(null);
let pollingTimer    = null;

const isPayModalOpen   = ref(false);
const selectedPayOrder = ref(null);
const payMethod        = ref("cash");
const isPaying         = ref(false);

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
  const d = new Date(currentDate.value);
  d.setDate(d.getDate() + days);
  currentDate.value = d;
  fetchActiveOrders();
};

const fetchActiveOrders = async () => {
  try {
    const res = await orderAPI.getActiveOrders(targetDateString.value);
    orders.value = res.data;
  } catch (err) {
    console.error("Gagal tarik data:", err);
  }
};

const filteredOrders = computed(() =>
  orders.value.filter(o => (o.customer_phone || "").includes(searchQuery.value))
);

const openOrderModal = (order) => {
  selectedOrder.value = order;
  isModalOpen.value   = true;
};

const openPayModal = (order) => {
  selectedPayOrder.value = order;
  payMethod.value        = order.payment_method || "cash";
  payAmountPaid.value    = 0;   // ++ reset
  isPayModalOpen.value   = true;
};

const confirmPay = async () => {
  if (!selectedPayOrder.value) return;
  isPaying.value = true;
  try {
    await apiClient.patch(`/orders/${selectedPayOrder.value.id}/pay/`, {
      payment_method: payMethod.value,
      amount_paid:    payMethod.value === 'cash' ? payAmountPaid.value : 0,  // ++ tambahan
      kasir_name:     kasirName.value,
    });
    toast.success(`Order ${selectedPayOrder.value.order_number} berhasil dilunasi`);
    isPayModalOpen.value   = false;
    selectedPayOrder.value = null;
    payAmountPaid.value    = 0;  // ++ reset
    fetchActiveOrders();
  } catch {
    toast.error("Gagal melunasi pembayaran");
  } finally {
    isPaying.value = false;
  }
};

// Screenshot struk → share WA sebagai foto
const shareReceiptAsImage = async () => {
  if (!receiptRef.value || !selectedOrder.value) return;
  isCapturing.value = true;

  await new Promise(r => setTimeout(r, 200));

  try {
    const canvas = await html2canvas(receiptRef.value, {
      backgroundColor: '#0f0f0f',
      scale: 2,
      useCORS: true,
    });

    canvas.toBlob(async (blob) => {
      if (!blob) { toast.error("Gagal membuat gambar struk"); isCapturing.value = false; return; }

      const file = new File([blob], `struk-${selectedOrder.value.order_number}.png`, { type: 'image/png' });

      if (navigator.share && navigator.canShare?.({ files: [file] })) {
        await navigator.share({
          files: [file],
          text: 'Bukti Pembelian di Masashimura, terimakasih banyak ditunggu orderan selanjutnya 🙏',
        });
      } else {
        // Fallback: download + buka WA
        const url = URL.createObjectURL(blob);
        const a   = document.createElement('a');
        a.href = url; a.download = file.name; a.click();
        URL.revokeObjectURL(url);

        const phone  = (selectedOrder.value.customer_phone || '').startsWith('0')
          ? '62' + selectedOrder.value.customer_phone.slice(1)
          : selectedOrder.value.customer_phone || '';
        const caption = encodeURIComponent(
          'Bukti Pembelian di Masashimura, terimakasih banyak ditunggu orderan selanjutnya 🙏'
        );
        const waUrl = phone ? `https://wa.me/${phone}?text=${caption}` : `https://wa.me/?text=${caption}`;
        setTimeout(() => window.open(waUrl, '_blank'), 500);
        toast.info("Gambar struk diunduh. Lampirkan ke WhatsApp secara manual jika perlu.");
      }
      isCapturing.value = false;
    }, 'image/png');
  } catch (err) {
    console.error(err);
    toast.error("Gagal screenshot struk");
    isCapturing.value = false;
  }
};

// Hitung subtotal dari items — tidak bergantung pada field subtotal backend
const computedSubtotal = computed(() => {
  const items = selectedOrder.value?.items || [];
  if (items.length) {
    return items.reduce((sum, item) => sum + (parseFloat(item.price) * parseInt(item.quantity || 1)), 0);
  }
  return parseFloat(selectedOrder.value?.subtotal || selectedOrder.value?.total_price || 0);
});

const formatPrice = (p) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(p || 0);
const formatTime = (s) =>
  new Date(s).toLocaleTimeString('id-ID', { hour: "2-digit", minute: "2-digit", hour12: false })
const formatFullDateTime = (s) =>
  new Date(s).toLocaleString('id-ID', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
  }) + ' WIB';

onMounted(() => {
  fetchActiveOrders();
  pollingTimer = setInterval(fetchActiveOrders, 5000);
});
onUnmounted(() => { if (pollingTimer) clearInterval(pollingTimer); });
</script>

<style scoped>
.max-h-\[260px\]::-webkit-scrollbar { display: none; }
.max-h-\[260px\] { -ms-overflow-style: none; scrollbar-width: none; }

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}
</style>