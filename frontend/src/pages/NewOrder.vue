<template>
  <div class="p-4 sm:p-8 text-white max-w-7xl mx-auto flex flex-col lg:flex-row gap-6 lg:gap-8 items-start w-full box-border">

    <!-- KATALOG MENU -->
    <div class="flex-1 w-full min-w-0 space-y-5">
      <div class="flex justify-between items-start gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold tracking-wide font-oswald">New Order (POS)</h1>
          <p class="text-xs text-white/40 mt-1">
            📅 Tanggal Operasional:
            <span class="text-primary font-mono font-bold">{{ liveFormattedDate }}</span>
          </p>
        </div>
        <button @click="showUnpaidDrawer = true"
          class="relative w-12 h-12 rounded-xl bg-[#0a0a0a] border border-white/10 hover:border-primary transition">
          🧾
          <span v-if="unpaidOrders.length"
            class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-primary text-[10px] flex items-center justify-center font-bold">
            {{ unpaidOrders.length }}
          </span>
        </button>
      </div>

      <div v-if="isLoadingMenus" class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div v-for="n in 6" :key="n"
          class="bg-[#0a0a0a] p-4 rounded-xl border border-white/5 min-h-[140px] animate-pulse space-y-4">
          <div class="h-4 bg-white/5 rounded w-3/4"></div>
          <div class="h-3 bg-white/5 rounded w-1/3"></div>
        </div>
      </div>

      <div v-else-if="menuLoadError"
        class="bg-[#0a0a0a] border border-red-600/20 rounded-2xl p-8 text-center space-y-3">
        <p class="text-sm text-white/60">⚠️ Gagal memuat katalog menu dari database.</p>
        <button @click="fetchMenus"
          class="px-4 py-2 bg-primary hover:bg-red-700 rounded-xl text-xs font-bold uppercase tracking-wider transition">
          Coba Lagi
        </button>
      </div>

      <div v-else-if="filteredMenus.length === 0"
        class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-10 text-center space-y-1">
        <p class="text-sm text-white/40 font-medium">Menu tidak ditemukan.</p>
        <p class="text-xs text-white/20">Coba kata kunci atau kategori lain.</p>
      </div>

      <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div
          v-for="menu in filteredMenus" :key="menu.id"
          class="bg-[#0a0a0a] border rounded-xl p-4 transition min-h-[140px] flex flex-col justify-between gap-4 group w-full box-border relative"
          :class="!menu.is_available
            ? 'opacity-50 border-zinc-800 grayscale cursor-not-allowed'
            : 'border-white/5 hover:border-red-600 cursor-pointer'"
          @click="addToOrder(menu)"
        >
          <div v-if="!menu.is_available"
            class="absolute inset-0 z-10 flex items-center justify-center bg-black/70 rounded-xl">
            <span class="font-oswald font-bold text-red-500 border border-red-500 px-3 py-1 text-xs uppercase tracking-widest">Habis</span>
          </div>
          <div class="space-y-1 w-full min-w-0">
            <h3 class="font-bold text-sm text-white/90 truncate">{{ menu.name }}</h3>
            <p class="text-xs font-mono font-bold text-primary">{{ formatPrice(menu.price) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- RINGKASAN PESANAN -->
    <div class="w-full lg:w-[390px] bg-[#0a0a0a] p-5 sm:p-6 rounded-2xl border border-white/5 h-fit shrink-0 lg:sticky lg:top-8 space-y-6 box-border">
      <h2 class="text-lg font-bold font-oswald tracking-wide border-b border-white/5 pb-3">Ringkasan Pesanan</h2>

      <!-- Data Pelanggan -->
      <div class="space-y-3">
        <div class="space-y-1">
          <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Nomor HP Pelanggan</label>
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center text-xs font-bold text-primary shrink-0 font-mono">
              {{ customerInitial }}
            </div>
            <input
              v-model="customerPhone"
              @input="debounceTrackLoyalty"
              placeholder="Contoh: 081234567xxx"
              class="flex-1 min-w-0 bg-white/5 border border-white/10 rounded-xl p-3 text-sm focus:outline-none focus:border-primary font-mono transition text-white"
            />
          </div>
        </div>

        <div class="space-y-1">
          <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Nama Pelanggan (Opsional)</label>
          <input
            v-model="customerName"
            type="text"
            placeholder="Nama pembeli..."
            class="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-sm focus:outline-none focus:border-primary transition text-white"
          />
        </div>

        <div v-if="customerPhone.length >= 9" class="p-3.5 rounded-xl border text-xs transition">
          <div v-if="isTrackingLoyalty" class="text-white/50 animate-pulse font-medium">
            ⏳ Tracking status kuota bulanan member...
          </div>
          <div v-else-if="isLoyal" class="bg-emerald-500/10 border-emerald-500/20 text-emerald-400 space-y-1 font-medium">
            <p class="font-bold">🎉 Member Terverifikasi Loyal!</p>
            <p class="text-[11px] text-white/60">
              Berhak dapet potongan harga otomatis
              <span class="text-emerald-400 font-bold">-{{ discountPercent }}%</span>.
            </p>
          </div>
          <div v-else class="bg-white/5 border-white/5 text-white/40 leading-relaxed">
            ℹ️ Nomor HP belum memenuhi kualifikasi syarat belanja minimal bulan ini.
          </div>
        </div>
      </div>

      <!-- Keranjang Kosong -->
      <div v-if="orderItems.length === 0" class="text-white/20 text-center py-12 text-xs font-medium">
        Keranjang belanjaan kasir masih kosong.
      </div>

      <!-- Keranjang Berisi -->
      <div v-else class="space-y-4">
        <div class="max-h-[260px] overflow-y-auto pr-1 space-y-3 scrollbar-thin">
          <div
            v-for="(item, index) in orderItems" :key="index"
            class="bg-white/5 p-4 rounded-xl border border-white/5 space-y-3"
          >
            <div class="flex items-start justify-between gap-2">
              <div class="min-w-0 flex-1">
                <p class="text-xs font-bold text-white/90 truncate">{{ item.name }}</p>
                <p class="text-[11px] font-mono text-zinc-400 mt-0.5">{{ formatPrice(item.price) }}</p>
              </div>
              <div class="flex items-center gap-1.5 bg-black border border-white/10 p-1 rounded-lg shrink-0 font-mono text-xs">
                <button @click="updateQty(index, -1)"
                  class="w-6 h-6 flex items-center justify-center hover:bg-white/10 rounded font-bold transition">-</button>
                <span class="w-5 text-center font-bold">{{ item.quantity }}</span>
                <button @click="updateQty(index, 1)"
                  class="w-6 h-6 flex items-center justify-center hover:bg-white/10 rounded font-bold transition">+</button>
              </div>
            </div>
            <input
              type="text"
              v-model="item.notes"
              @input="handleNotesChange(index)"
              placeholder="Catatan porsi koki (Level 5, Tanpa Bawang, dll)..."
              class="w-full bg-black/40 border border-white/5 rounded-lg py-2 px-3 text-[11px] text-amber-400 focus:outline-none focus:border-amber-500/50 font-sans transition"
            />
          </div>
        </div>

        <!-- Alur Konsumsi -->
        <div class="space-y-1">
          <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Alur Konsumsi</label>
          <div class="grid grid-cols-2 gap-2">
            <button
              @click="orderType = 'dine_in_now'"
              class="py-2.5 rounded-xl font-bold border transition uppercase tracking-wider text-[11px]"
              :class="orderType === 'dine_in_now'
                ? 'bg-primary border-primary text-white'
                : 'bg-transparent border-white/10 text-white/40 hover:text-white'"
            >
              ⚡ Bayar Sekarang
            </button>
            <button
              @click="orderType = 'dine_in_later'"
              :disabled="paymentMethod === 'qris_manual'"
              class="py-2.5 rounded-xl font-bold border transition uppercase tracking-wider text-[11px]"
              :class="orderType === 'dine_in_later'
                ? 'bg-amber-600 border-amber-600 text-white'
                : paymentMethod === 'qris_manual'
                  ? 'bg-transparent border-white/5 text-white/20 cursor-not-allowed'
                  : 'bg-transparent border-white/10 text-white/40 hover:text-white'"
            >
              🕒 Makan Dulu
            </button>
          </div>
        </div>
      </div>

      <!-- Metode Transaksi -->
      <div class="space-y-1">
        <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Metode Transaksi</label>
        <div class="grid grid-cols-2 gap-2">
          <button
            @click="selectPaymentMethod('cash')"
            class="py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider border transition flex items-center justify-center gap-1.5"
            :class="paymentMethod === 'cash' ? 'bg-white/10 border-white/20 text-white' : 'bg-transparent border-white/10 text-white/40 hover:text-white'"
          >
            💵 Tunai
          </button>
          <button
            @click="selectPaymentMethod('qris_manual')"
            class="py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider border transition flex items-center justify-center gap-1.5"
            :class="paymentMethod === 'qris_manual' ? 'bg-white/10 border-white/20 text-white' : 'bg-transparent border-white/10 text-white/40 hover:text-white'"
          >
            📱 QRIS Manual
          </button>
        </div>
      </div>

      <!-- Input Uang Diterima (hanya cash + bayar sekarang) -->
      <div v-if="paymentMethod === 'cash' && orderType === 'dine_in_now'" class="space-y-2">
        <label class="text-[10px] uppercase font-bold tracking-wider text-white/40">Uang Diterima</label>
        <input
          v-model.number="amountPaid"
          type="number"
          placeholder="Nominal uang dari pelanggan..."
          class="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-sm focus:outline-none focus:border-primary transition text-white font-mono"
        />
        <div
          v-if="amountPaid > 0 && amountPaid >= totalPrice"
          class="flex justify-between text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3"
        >
          <span>Kembalian</span>
          <span>{{ formatPrice(changeDue) }}</span>
        </div>
        <div v-else-if="amountPaid > 0 && amountPaid < totalPrice" class="text-xs text-red-400 font-mono px-1">
          ⚠️ Kurang {{ formatPrice(totalPrice - amountPaid) }}
        </div>
      </div>

      <!-- Info Kasir -->
      <div class="flex items-center gap-2 text-xs text-white/30 px-1">
        <span>👤 Kasir:</span>
        <span class="text-white/60 font-medium">{{ kasirName }}</span>
      </div>

      <!-- Ringkasan Harga -->
      <div class="border-t border-white/10 pt-4 space-y-2 font-mono text-xs text-zinc-400">
        <div class="flex justify-between">
          <span>Subtotal</span>
          <span class="text-white">{{ formatPrice(subtotal) }}</span>
        </div>
        <div v-if="isLoyal" class="flex justify-between text-emerald-400">
          <span>Diskon Member ({{ discountPercent }}%)</span>
          <span>-{{ formatPrice(discountAmount) }}</span>
        </div>
        <div class="flex justify-between font-bold text-sm pt-2 border-t border-white/10 text-white">
          <span>TOTAL AKHIR</span>
          <span class="text-primary text-base font-bold">{{ formatPrice(totalPrice) }}</span>
        </div>
      </div>

      <button
        @click="submitOrder"
        :disabled="isSubmitting || orderItems.length === 0"
        class="w-full bg-primary disabled:bg-white/10 disabled:text-white/30 py-3.5 rounded-xl font-bold hover:bg-red-700 transition uppercase tracking-widest text-xs"
      >
        {{ isSubmitting ? 'Memproses Transaksi...' : 'Eksekusi Proses Pesanan' }}
      </button>
    </div>
  </div>

  <!-- DRAWER TAGIHAN BELUM LUNAS -->
  <transition
    enter-active-class="duration-300" leave-active-class="duration-300"
    enter-from-class="opacity-0" enter-to-class="opacity-100"
    leave-from-class="opacity-100" leave-to-class="opacity-0"
  >
    <div v-if="showUnpaidDrawer" class="fixed inset-0 z-50 bg-black/70" @click.self="showUnpaidDrawer = false">
      <div class="absolute right-0 top-0 w-full sm:w-[420px] h-full bg-[#090909] border-l border-white/10 p-6 overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h2 class="font-oswald text-xl">🧾 Tagihan Belum Lunas</h2>
          <button @click="showUnpaidDrawer = false" class="text-white/40 hover:text-white">✕</button>
        </div>
        <input
          v-model="unpaidSearch"
          placeholder="Cari nomor order, nama, HP..."
          class="w-full mb-4 bg-white/5 border border-white/10 rounded-xl p-3 text-sm"
        />
        <div v-if="!filteredUnpaidOrders.length" class="text-center text-white/30 py-16">Tidak ada tagihan.</div>
        <div
          v-for="order in filteredUnpaidOrders" :key="order.id"
          class="mb-4 p-4 rounded-xl bg-white/5 border border-white/10"
        >
          <div class="flex justify-between">
            <div>
              <p class="font-bold">{{ order.order_number }}</p>
              <p class="text-xs text-white/50">{{ order.customer_name || "Walk In" }}</p>
              <p class="text-xs text-white/30">{{ order.customer_phone || "-" }}</p>
            </div>
            <div class="text-right">
              <p class="font-bold text-primary">{{ formatPrice(order.total_price) }}</p>
              <p class="text-xs text-white/40">{{ order.items.length }} Item</p>
            </div>
          </div>
          <button
            class="mt-4 w-full py-2 rounded-lg bg-primary hover:bg-red-700 text-xs font-bold"
            @click="openPaymentModal(order)"
          >
            Bayar
          </button>
        </div>
      </div>
    </div>
  </transition>

  <!-- MODAL KONFIRMASI PEMBAYARAN -->
  <transition
    enter-active-class="duration-300" leave-active-class="duration-300"
    enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100"
    leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95"
  >
    <div
      v-if="showPaymentModal && selectedUnpaidOrder"
      class="fixed inset-0 z-[70] bg-black/70 flex items-center justify-center p-5"
      @click.self="showPaymentModal = false"
    >
      <div class="bg-[#0b0b0b] w-full max-w-lg rounded-2xl border border-white/10 p-6 space-y-5 max-h-[90vh] overflow-y-auto">

        <!-- Header -->
        <div class="flex justify-between items-center">
          <h2 class="font-oswald text-xl">💳 Konfirmasi Pembayaran</h2>
          <button @click="showPaymentModal = false" class="text-white/40 hover:text-white">✕</button>
        </div>

        <!-- Info order -->
        <div class="space-y-1">
          <p class="font-mono font-bold text-primary">{{ selectedUnpaidOrder.order_number }}</p>
          <p>{{ selectedUnpaidOrder.customer_name || "Walk In" }}</p>
          <p class="text-xs text-white/40">{{ selectedUnpaidOrder.customer_phone || "-" }}</p>
          <p class="text-xs text-white/40">{{ selectedUnpaidOrder.created_time }}</p>
        </div>

        <hr class="border-white/10" />

        <!-- List item dengan scroll -->
        <div class="space-y-3 max-h-[180px] overflow-y-auto pr-1">
          <div
            v-for="item in selectedUnpaidOrder.items" :key="item.id"
            class="flex justify-between text-sm"
          >
            <div>
              <p class="font-semibold">{{ item.menu_name }} x{{ item.quantity }}</p>
              <p v-if="item.notes" class="text-xs text-amber-400">+ {{ item.notes }}</p>
            </div>
            <span>{{ formatPrice(item.price * item.quantity) }}</span>
          </div>
        </div>

        <hr class="border-white/10" />

        <!-- Subtotal & Total -->
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-white/50">Subtotal</span>
            <span>{{ formatPrice(selectedUnpaidOrder.subtotal) }}</span>
          </div>
          <div v-if="parseFloat(selectedUnpaidOrder.discount_amount) > 0" class="flex justify-between text-emerald-400">
            <span>Diskon</span>
            <span>-{{ formatPrice(selectedUnpaidOrder.discount_amount) }}</span>
          </div>
          <div class="flex justify-between font-bold text-base">
            <span>Total</span>
            <span class="text-primary">{{ formatPrice(selectedUnpaidOrder.total_price) }}</span>
          </div>
        </div>

        <hr class="border-white/10" />

        <!-- Metode Pembayaran -->
        <div class="space-y-2">
          <label class="text-[10px] uppercase text-white/40 font-bold tracking-wider">Metode Pembayaran</label>
          <div class="grid grid-cols-2 gap-2">
            <button
              @click="selectedPaymentMethod = 'cash'"
              class="py-3 rounded-xl border font-bold transition"
              :class="selectedPaymentMethod === 'cash' ? 'bg-primary border-primary text-white' : 'border-white/10 text-white/50'"
            >
              💵 Cash
            </button>
            <button
              @click="selectedPaymentMethod = 'qris_manual'"
              class="py-3 rounded-xl border font-bold transition"
              :class="selectedPaymentMethod === 'qris_manual' ? 'bg-primary border-primary text-white' : 'border-white/10 text-white/50'"
            >
              📱 QRIS
            </button>
          </div>
        </div>

        <!-- Input uang diterima (hanya cash) -->
        <div v-if="selectedPaymentMethod === 'cash'" class="space-y-2">
          <label class="text-[10px] uppercase text-white/40 font-bold tracking-wider">Uang Diterima</label>
          <input
            v-model.number="amountPaidModal"
            type="number"
            placeholder="Nominal uang dari pelanggan..."
            class="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-sm font-mono text-white focus:outline-none focus:border-primary transition"
          />
          <div
            v-if="amountPaidModal > 0 && amountPaidModal >= parseFloat(selectedUnpaidOrder.total_price)"
            class="flex justify-between text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3"
          >
            <span>Kembalian</span>
            <span>{{ formatPrice(amountPaidModal - parseFloat(selectedUnpaidOrder.total_price)) }}</span>
          </div>
          <div
            v-else-if="amountPaidModal > 0 && amountPaidModal < parseFloat(selectedUnpaidOrder.total_price)"
            class="text-xs text-red-400 font-mono px-1"
          >
            ⚠️ Kurang {{ formatPrice(parseFloat(selectedUnpaidOrder.total_price) - amountPaidModal) }}
          </div>
        </div>

        <!-- Tombol konfirmasi -->
        <button
          @click="confirmPayment"
          :disabled="isPaying || (selectedPaymentMethod === 'cash' && amountPaidModal > 0 && amountPaidModal < parseFloat(selectedUnpaidOrder.total_price))"
          class="w-full py-3 rounded-xl bg-primary font-bold hover:bg-red-700 disabled:opacity-40 transition uppercase tracking-widest text-sm"
        >
          {{ isPaying ? "Memproses..." : "Konfirmasi Pembayaran" }}
        </button>

      </div>
    </div>
  </transition>

  <!-- STRUK TERSEMBUNYI untuk screenshot -->
  <div
    ref="receiptRef"
    class="fixed -left-[9999px] top-0 w-[380px] bg-white text-black p-6 font-mono text-xs space-y-3"
    style="font-family: 'Courier New', monospace;"
  >
    <div class="text-center space-y-1">
      <p class="text-base font-black uppercase tracking-widest">MASASHIMURA</p>
      <p class="text-[10px] text-gray-500">Jl. Pintu air no 48 Depan Pengadilan Bekasi</p>
      <p class="text-[10px] text-gray-400">{{ new Date().toLocaleString('id-ID') }}</p>
      <p class="text-gray-300">========================================</p>
    </div>
    <div v-if="lastOrder" class="space-y-1 text-[11px]">
      <div class="flex justify-between">
        <span>No. Nota</span>
        <span class="font-bold">{{ lastOrder.order_number }}</span>
      </div>
      <div class="flex justify-between">
        <span>Kasir</span>
        <span>{{ kasirName }}</span>
      </div>
      <div class="flex justify-between">
        <span>Pelanggan</span>
        <span>{{ lastOrder.customer_name || lastOrder.customer_phone || 'Walk In' }}</span>
      </div>
    </div>
    <p class="text-gray-300">----------------------------------------</p>
    <div v-if="lastOrder" class="space-y-2">
      <div v-for="(item, idx) in lastOrderItems" :key="idx">
        <div class="flex justify-between font-medium">
          <span>{{ item.quantity }}x {{ item.name }}</span>
          <span>{{ formatPrice(item.price * item.quantity) }}</span>
        </div>
        <div v-if="item.notes" class="text-amber-600 text-[10px] pl-3 italic">📋 {{ item.notes }}</div>
      </div>
    </div>
    <p class="text-gray-300">----------------------------------------</p>
    <div v-if="lastOrder" class="space-y-1 text-[11px]">
      <div class="flex justify-between">
        <span>Subtotal</span>
        <span>{{ formatPrice(lastOrder.subtotal || lastOrder.total_price) }}</span>
      </div>
      <div v-if="parseFloat(lastOrder.discount_amount) > 0" class="flex justify-between text-green-700">
        <span>Diskon Member</span>
        <span>-{{ formatPrice(lastOrder.discount_amount) }}</span>
      </div>
      <div class="flex justify-between font-black text-sm border-t border-gray-200 pt-1">
        <span>TOTAL</span>
        <span>{{ formatPrice(lastOrder.total_price) }}</span>
      </div>
      <div v-if="lastOrder.amount_paid > 0" class="flex justify-between">
        <span>Bayar</span>
        <span>{{ formatPrice(lastOrder.amount_paid) }}</span>
      </div>
      <div v-if="lastOrder.change_amount > 0" class="flex justify-between text-green-700 font-bold">
        <span>Kembalian</span>
        <span>{{ formatPrice(lastOrder.change_amount) }}</span>
      </div>
    </div>
    <p class="text-gray-300">========================================</p>
    <div class="text-center text-[10px] text-gray-500 space-y-0.5">
      <p>Metode: {{ lastOrder?.payment_method?.toUpperCase() || 'CASH' }}</p>
      <p class="font-bold">Terima kasih sudah makan di Masashimura! 🙏</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { menuAPI, orderAPI, apiClient } from "@/api";
import { toast } from "vue-sonner";
import { useAuthStore } from '@/stores/auth';
import html2canvas from 'html2canvas';

const authStore  = useAuthStore();
const kasirName  = computed(() => authStore.user?.name || authStore.user?.username || 'Staff');

const menus             = ref([]);
const isLoadingMenus    = ref(false);
const menuLoadError     = ref(false);
const searchQuery       = ref("");
const unpaidSearch      = ref("");
const selectedCategory  = ref("Semua");
const orderItems        = ref([]);
const customerPhone     = ref("");
const customerName      = ref("");
const isLoyal           = ref(false);
const discountPercent   = ref(0);
const paymentMethod     = ref("cash");
const orderType         = ref("dine_in_now");
const isSubmitting      = ref(false);
const isTrackingLoyalty = ref(false);
let debounceTimeout     = null;

const unpaidOrders          = ref([]);
const showUnpaidDrawer      = ref(false);
const isLoadingUnpaid       = ref(false);
const selectedUnpaidOrder   = ref(null);
const showPaymentModal      = ref(false);
const selectedPaymentMethod = ref("cash");
const isPaying              = ref(false);
const amountPaidModal       = ref(0);

const amountPaid = ref(0);
const changeDue  = computed(() => {
  if (paymentMethod.value !== 'cash' || orderType.value !== 'dine_in_now') return 0;
  return amountPaid.value >= totalPrice.value ? amountPaid.value - totalPrice.value : 0;
});

const receiptRef     = ref(null);
const lastOrder      = ref(null);
const lastOrderItems = ref([]);

// ── Unpaid orders ─────────────────────────────────────────────────────────────
const fetchUnpaidOrders = async () => {
  isLoadingUnpaid.value = true;
  try {
    const { data } = await apiClient.get("/orders/unpaid/");
    unpaidOrders.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    isLoadingUnpaid.value = false;
  }
};

const filteredUnpaidOrders = computed(() => {
  const q = unpaidSearch.value.toLowerCase().trim();
  if (!q) return unpaidOrders.value;
  return unpaidOrders.value.filter(order =>
    order.order_number?.toLowerCase().includes(q) ||
    order.customer_name?.toLowerCase().includes(q) ||
    order.customer_phone?.includes(q)
  );
});

const openPaymentModal = (order) => {
  selectedUnpaidOrder.value   = order;
  selectedPaymentMethod.value = "cash";
  amountPaidModal.value       = 0;
  showPaymentModal.value      = true;
};

const confirmPayment = async () => {
  if (!selectedUnpaidOrder.value) return;
  isPaying.value = true;
  try {
    await apiClient.patch(`/orders/${selectedUnpaidOrder.value.id}/pay/`, {
      payment_method: selectedPaymentMethod.value,
      amount_paid:    selectedPaymentMethod.value === 'cash' ? amountPaidModal.value : 0,
      kasir_name:     kasirName.value,
    });
    toast.success("Pembayaran berhasil");
    showPaymentModal.value    = false;
    selectedUnpaidOrder.value = null;
    amountPaidModal.value     = 0;
    fetchUnpaidOrders();
  } catch {
    toast.error("Pembayaran gagal");
  } finally {
    isPaying.value = false;
  }
};

// ── Computed ──────────────────────────────────────────────────────────────────
const liveFormattedDate = computed(() =>
  new Date().toLocaleDateString('id-ID', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })
);
const customerInitial = computed(() =>
  customerPhone.value ? customerPhone.value.trim().charAt(0).toUpperCase() : "?"
);
const filteredMenus = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return menus.value
    .filter(menu => {
      const matchCat = selectedCategory.value === "Semua" || (menu.category || "Makanan") === selectedCategory.value;
      const matchQ   = !query || menu.name?.toLowerCase().includes(query);
      return matchCat && matchQ;
    })
    .sort((a, b) => b.is_available - a.is_available);
});
const subtotal       = computed(() => orderItems.value.reduce((acc, item) => acc + item.price * item.quantity, 0));
const discountAmount = computed(() => isLoyal.value ? (subtotal.value * discountPercent.value) / 100 : 0);
const totalPrice     = computed(() => subtotal.value - discountAmount.value);

// ── Menu ──────────────────────────────────────────────────────────────────────
const fetchMenus = async () => {
  isLoadingMenus.value = true;
  menuLoadError.value  = false;
  try {
    const res = await menuAPI.getAll();
    menus.value = res.data;
  } catch {
    menuLoadError.value = true;
  } finally {
    isLoadingMenus.value = false;
  }
};

// ── Loyalty ───────────────────────────────────────────────────────────────────
const debounceTrackLoyalty = () => {
  clearTimeout(debounceTimeout);
  if (customerPhone.value.length < 9) { // ← 10 jadi 9
    isLoyal.value = false;
    discountPercent.value = 0;
    return;
  }
  isTrackingLoyalty.value = true;
  debounceTimeout = setTimeout(checkLoyalty, 800);
};

const checkLoyalty = async () => {
  try {
    const { data } = await apiClient.get("/orders/check_loyalty_status/", {
      params: { phone: customerPhone.value }
    });
    console.log('loyalty response:', data);
    console.log('is_loyal:', data.is_loyal);
    console.log('discount_percent:', data.discount_percent);
    isLoyal.value         = data.is_loyal;
    discountPercent.value = data.discount_percent || 0;
    console.log('after set - isLoyal:', isLoyal.value, 'discountPercent:', discountPercent.value);
  } catch (err) {
    console.error('loyalty error:', err);
    isLoyal.value         = false;
    discountPercent.value = 0;
  } finally {
    isTrackingLoyalty.value = false;
  }
};

// ── Cart ──────────────────────────────────────────────────────────────────────
const addToOrder = (menu) => {
  if (!menu.is_available) { toast.error("Menu ini sedang habis!"); return; }
  const existing = orderItems.value.find(i => i.id === menu.id && i.notes === "");
  if (existing) {
    existing.quantity++;
  } else {
    orderItems.value.push({ ...menu, quantity: 1, notes: "" });
  }
};
const handleNotesChange = (index) => {
  const cur = orderItems.value[index];
  const dup = orderItems.value.findIndex((item, idx) =>
    idx !== index &&
    item.id === cur.id &&
    item.notes.trim().toLowerCase() === cur.notes.trim().toLowerCase()
  );
  if (dup > -1) {
    orderItems.value[dup].quantity += cur.quantity;
    orderItems.value.splice(index, 1);
    toast.info("Menu dengan catatan sama digabungkan!");
  }
};
const updateQty = (index, delta) => {
  orderItems.value[index].quantity += delta;
  if (orderItems.value[index].quantity <= 0) orderItems.value.splice(index, 1);
};

// ── Metode Pembayaran ─────────────────────────────────────────────────────────
// FIX: gunakan selectPaymentMethod agar side effect (reset orderType) ikut terpanggil
const selectPaymentMethod = (method) => {
  paymentMethod.value = method;
  // QRIS tidak bisa "makan dulu" — force bayar sekarang
  if (method === 'qris_manual') {
    orderType.value = 'dine_in_now';
  }
};

// ── Screenshot struk ──────────────────────────────────────────────────────────
const shareReceiptAsImage = async (orderData) => {
  await new Promise(r => setTimeout(r, 300));
  try {
    const canvas = await html2canvas(receiptRef.value, {
      backgroundColor: '#ffffff',
      scale: 2,
      useCORS: true,
    });
    canvas.toBlob(async (blob) => {
      if (!blob) { toast.error("Gagal membuat gambar struk"); return; }
      if (navigator.share && navigator.canShare?.({ files: [new File([blob], 'struk.png', { type: 'image/png' })] })) {
        const file = new File([blob], `struk-${orderData.order_number}.png`, { type: 'image/png' });
        await navigator.share({
          files: [file],
          text: 'Bukti Pembelian di Masashimura, terimakasih banyak ditunggu orderan selanjutnya 🙏',
        });
      } else {
        const url = URL.createObjectURL(blob);
        const a   = document.createElement('a');
        a.href     = url;
        a.download = `struk-${orderData.order_number}.png`;
        a.click();
        URL.revokeObjectURL(url);
        const caption = encodeURIComponent('Bukti Pembelian di Masashimura, terimakasih banyak ditunggu orderan selanjutnya 🙏');
        const phone   = (customerPhone.value || '').startsWith('0')
          ? '62' + customerPhone.value.slice(1)
          : customerPhone.value;
        const waUrl = phone ? `https://wa.me/${phone}?text=${caption}` : `https://wa.me/?text=${caption}`;
        setTimeout(() => window.open(waUrl, '_blank'), 500);
        toast.info("Gambar struk diunduh. Silakan lampirkan ke WhatsApp secara manual.");
      }
    }, 'image/png');
  } catch (err) {
    console.error(err);
    toast.error("Gagal membuat screenshot struk");
  }
};

// ── Submit order ──────────────────────────────────────────────────────────────
const submitOrder = async () => {
  if (orderItems.value.length === 0) return toast.error("Keranjang kosong!");
  isSubmitting.value = true;

  const payload = {
    source:         'pos',
    customer:       customerPhone.value
      ? { phone: customerPhone.value, name: customerName.value || "Member Baru" }
      : null,
    payment_method: paymentMethod.value,
    payment_status: orderType.value === 'dine_in_later' ? 'pending' : 'paid',
    status:         'pending',
    amount_paid:    paymentMethod.value === 'cash' ? amountPaid.value : 0,
    kasir_name:     kasirName.value,
    items: orderItems.value.map(item => ({
      menu_id:  item.id,
      quantity: item.quantity,
      price:    item.price,
      notes:    item.notes,
    })),
  };

  try {
    const res = await apiClient.post("/orders/", payload);
    lastOrder.value      = res.data;
    lastOrderItems.value = [...orderItems.value];
    toast.success("Pesanan berhasil masuk ke sistem!");

    // FIX: reset semua state termasuk orderType
    orderItems.value    = [];
    customerPhone.value = "";
    customerName.value  = "";
    isLoyal.value       = false;
    discountPercent.value = 0;
    paymentMethod.value = "cash";
    orderType.value     = "dine_in_now";
    amountPaid.value    = 0;

    fetchUnpaidOrders();
    await shareReceiptAsImage(res.data);
  } catch (e) {
    console.error(e);
    toast.error("Gagal menyimpan data transaksi ke server.");
  } finally {
    isSubmitting.value = false;
  }
};

const formatPrice = (p) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(p || 0);

onMounted(() => {
  fetchMenus();
  fetchUnpaidOrders();
});
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