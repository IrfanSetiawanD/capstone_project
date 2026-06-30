<template>
  <div class="ao-root">

    <!-- ── PAGE HEADER ─────────────────────────────────────────────── -->
    <div class="ao-header">
      <div class="ao-header-left">
        <p class="ao-eyebrow">Masashimura · Operasional</p>
        <h1 class="ao-title">Active Orders</h1>
        <p class="ao-date-label">{{ formattedCurrentDate }}</p>
      </div>

      <div class="ao-header-right">
        <!-- Date navigator -->
        <div class="date-nav">
          <button class="date-nav-btn" @click="changeDate(-1)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
            Kemarin
          </button>
          <span class="date-nav-current">{{ targetDateString }}</span>
          <button class="date-nav-btn" @click="changeDate(1)">
            Besok
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>

        <!-- Search -->
        <div class="search-wrap">
          <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari no. HP..."
            class="search-input"
          />
        </div>
      </div>
    </div>

    <!-- ── ORDERS TABLE ────────────────────────────────────────────── -->
    <div class="ao-table-card">
      <!-- Summary strip -->
      <div class="ao-summary">
        <span class="summary-item">
          <span class="summary-dot dot-all"></span>
          {{ filteredOrders.length }} pesanan
        </span>
        <span class="summary-item">
          <span class="summary-dot dot-pending"></span>
          {{ filteredOrders.filter(o => o.payment_status !== 'paid').length }} belum lunas
        </span>
        <span class="summary-item">
          <span class="summary-dot dot-paid"></span>
          {{ filteredOrders.filter(o => o.payment_status === 'paid').length }} lunas
        </span>
      </div>

      <div class="table-scroll">
        <table class="ao-table">
          <thead>
            <tr>
              <th>Order</th>
              <th>Customer</th>
              <th class="th-right">Tagihan</th>
              <th class="th-center">Status</th>
              <th class="th-center">Pembayaran</th>
              <th>Metode</th>
              <th class="th-center">Waktu</th>
              <th class="th-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in filteredOrders"
              :key="order.id"
              class="ao-row"
              @click="openOrderModal(order)"
            >
              <td class="td-id">#{{ order.id }}</td>

              <td class="td-customer">
                <span class="customer-phone">{{ order.customer_phone || '—' }}</span>
                <span v-if="!order.customer_phone" class="guest-badge">Guest</span>
              </td>

              <td class="td-right td-price">{{ formatPrice(order.total_price) }}</td>

              <td class="td-center">
                <span
                  class="status-pill"
                  :class="order.status === 'completed' ? 'pill-green' : 'pill-amber'"
                >
                  {{ order.status === 'completed' ? 'Selesai' : 'Proses' }}
                </span>
              </td>

              <td class="td-center">
                <span
                  class="status-pill"
                  :class="order.payment_status === 'paid' ? 'pill-green' : 'pill-yellow'"
                >
                  {{ order.payment_status === 'paid' ? 'Lunas' : 'Pending' }}
                </span>
              </td>

              <td class="td-method">
                <span class="method-icon">{{ order.payment_method === 'qris_manual' ? '📱' : '💵' }}</span>
                {{ order.payment_method === 'qris_manual' ? 'QRIS' : (order.payment_method || 'Cash') }}
              </td>

              <td class="td-center td-time">{{ formatTime(order.created_at) }}</td>

              <td class="td-center" @click.stop>
                <button
                  v-if="order.payment_status !== 'paid'"
                  class="lunasi-btn"
                  @click="openPayModal(order)"
                >
                  Lunasi
                </button>
                <span v-else class="td-dash">✓</span>
              </td>
            </tr>

            <tr v-if="filteredOrders.length === 0">
              <td colspan="8" class="ao-empty">
                <div class="empty-icon">🍱</div>
                <p class="empty-text">Tidak ada pesanan untuk {{ targetDateString }}</p>
                <p class="empty-hint">Pesanan baru akan muncul otomatis setiap 5 detik</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── MODAL STRUK ─────────────────────────────────────────────── -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="isModalOpen = false">
      <div class="modal-box">
        <!-- Modal header -->
        <div class="modal-header">
          <div>
            <p class="modal-eyebrow">Struk Pesanan</p>
            <h2 class="modal-title">{{ selectedOrder?.order_number }}</h2>
          </div>
          <button class="modal-close" @click="isModalOpen = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Receipt body -->
        <div class="receipt-body">
          <div class="receipt-logo-area">
            <img src="/src/assets/masashimura-logo.png" alt="Logo" class="receipt-logo" />
            <p class="receipt-address">Jl. Pintu air no 48 Depan Pengadilan bekasi, Bekasi, Jawa Barat</p>
          </div>

          <div class="receipt-divider">· · · · · · · · · · · · · · · · · · · ·</div>

          <div class="receipt-meta">
            <div class="meta-row"><span>No. Nota</span><span class="meta-val">{{ selectedOrder?.order_number }}</span></div>
            <div class="meta-row"><span>Kasir</span><span class="meta-val">{{ selectedOrder?.kasir_name || kasirName }}</span></div>
            <div class="meta-row"><span>Waktu</span><span class="meta-val">{{ formatFullDateTime(selectedOrder?.created_at) }}</span></div>
            <div class="meta-row"><span>Pelanggan</span><span class="meta-val">{{ selectedOrder?.customer_name || selectedOrder?.customer_phone || 'Guest' }}</span></div>
          </div>

          <div class="receipt-divider">· · · · · · · · · · · · · · · · · · · ·</div>

          <div class="receipt-items">
            <p class="items-heading">Detail Pesanan</p>
            <div v-for="(item, idx) in selectedOrder?.items" :key="idx" class="item-row">
              <div class="item-main">
                <span class="item-qty">{{ item.quantity }}×</span>
                <span class="item-name">{{ item.menu_name }}</span>
                <span class="item-subtotal">{{ formatPrice(item.price * item.quantity) }}</span>
              </div>
              <div v-if="item.notes" class="item-note">{{ item.notes }}</div>
            </div>
          </div>

          <div class="receipt-divider">· · · · · · · · · · · · · · · · · · · ·</div>

          <div class="receipt-totals">
            <div class="total-row"><span>Subtotal</span><span>{{ formatPrice(computedSubtotal) }}</span></div>
            <div v-if="parseFloat(selectedOrder?.discount_amount) > 0" class="total-row total-discount">
              <span>Diskon Member</span><span>-{{ formatPrice(selectedOrder?.discount_amount) }}</span>
            </div>
            <div class="total-row total-final">
              <span>Total</span><span>{{ formatPrice(selectedOrder?.total_price) }}</span>
            </div>
            <div v-if="parseFloat(selectedOrder?.amount_paid) > 0" class="total-row total-paid">
              <span>Dibayar</span><span>{{ formatPrice(selectedOrder?.amount_paid) }}</span>
            </div>
            <div v-if="parseFloat(selectedOrder?.change_amount) > 0" class="total-row total-change">
              <span>Kembalian</span><span>{{ formatPrice(selectedOrder?.change_amount) }}</span>
            </div>
          </div>

          <div class="receipt-info-card">
            <div class="info-row"><span>Metode</span><span class="info-val">{{ order?.payment_method === 'qris_manual' ? 'QRIS' : (selectedOrder?.payment_method || 'Cash') }}</span></div>
            <div class="info-row"><span>Kasir</span><span class="info-val">{{ selectedOrder?.kasir_name || kasirName }}</span></div>
            <div class="info-row">
              <span>Status</span>
              <span :class="selectedOrder?.payment_status === 'paid' ? 'info-paid' : 'info-pending'">
                {{ selectedOrder?.payment_status === 'paid' ? 'LUNAS' : 'PENDING' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Modal footer actions -->
        <div class="modal-footer">
          <button class="btn-share" :disabled="isCapturing" @click="shareReceiptAsImage">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
            {{ isCapturing ? 'Memproses...' : 'Kirim via WA' }}
          </button>
          <button class="btn-close-modal" @click="isModalOpen = false">Tutup</button>
        </div>
      </div>
    </div>

    <!-- ── STRUK TERSEMBUNYI (untuk screenshot) ────────────────────── -->
    <div
      ref="receiptRef"
      style="
        position: fixed; left: -9999px; top: 0;
        width: 400px; background-color: #0f0f0f;
        color: #d4d4d8; padding: 24px;
        font-family: 'Courier New', monospace;
        font-size: 12px; line-height: 1.6;
      "
    >
      <div style="text-align:center; margin-bottom:16px;">
        <img src="/src/assets/masashimura-logo.png" alt="Logo" style="height:60px; margin:0 auto 8px; object-fit:contain; display:block;" />
        <div style="font-size:10px; color:#71717a;">Jl. Pintu air no 48 Depan Pengadilan bekasi, Bekasi, Jawa Barat</div>
        <div style="color:#3f3f46; margin-top:8px;">========================================</div>
      </div>
      <div style="font-size:11px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:2px;"><span>No. Nota :</span><span style="color:#ffffff; font-weight:700;">{{ selectedOrder?.order_number }}</span></div>
        <div style="display:flex; justify-content:space-between; margin-bottom:2px;"><span>Kasir :</span><span style="color:#ffffff;">{{ selectedOrder?.kasir_name || kasirName }}</span></div>
        <div style="display:flex; justify-content:space-between; margin-bottom:2px;"><span>Waktu :</span><span>{{ formatFullDateTime(selectedOrder?.created_at) }}</span></div>
        <div style="display:flex; justify-content:space-between;"><span>Pelanggan :</span><span style="color:#ffffff;">{{ selectedOrder?.customer_name || selectedOrder?.customer_phone || 'Guest' }}</span></div>
      </div>
      <div style="color:#3f3f46; margin-bottom:12px;">----------------------------------------</div>
      <div style="margin-bottom:12px;">
        <div style="font-weight:700; color:#ffffff; font-size:11px; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Detail Pesanan:</div>
        <div v-for="(item, idx) in selectedOrder?.items" :key="idx" style="margin-bottom:6px;">
          <div style="display:flex; justify-content:space-between; color:#ffffff;"><span>{{ item.quantity }}x {{ item.menu_name }}</span><span>{{ formatPrice(item.price * item.quantity) }}</span></div>
          <div v-if="item.notes" style="color:#f59e0b; font-size:10px; padding-left:12px; font-style:italic;">📋 "{{ item.notes }}"</div>
        </div>
      </div>
      <div style="color:#3f3f46; margin-bottom:12px;">----------------------------------------</div>
      <div style="font-size:11px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>Subtotal</span><span>{{ formatPrice(computedSubtotal) }}</span></div>
        <div v-if="parseFloat(selectedOrder?.discount_amount) > 0" style="display:flex; justify-content:space-between; color:#f87171; margin-bottom:4px;"><span>Diskon Member</span><span>-{{ formatPrice(selectedOrder?.discount_amount) }}</span></div>
        <div style="color:#3f3f46; margin:6px 0;">----------------------------------------</div>
        <div style="display:flex; justify-content:space-between; font-size:14px; font-weight:900; color:#ffffff; margin-bottom:6px;"><span>TOTAL AKHIR</span><span style="color:#ef4444;">{{ formatPrice(selectedOrder?.total_price) }}</span></div>
        <div v-if="parseFloat(selectedOrder?.amount_paid) > 0" style="display:flex; justify-content:space-between; margin-bottom:2px; color:#a1a1aa;"><span>Bayar</span><span style="color:#ffffff; font-weight:600;">{{ formatPrice(selectedOrder.amount_paid) }}</span></div>
        <div v-if="parseFloat(selectedOrder?.change_amount) > 0" style="display:flex; justify-content:space-between;"><span>Kembalian</span><span style="color:#34d399; font-weight:700;">{{ formatPrice(selectedOrder.change_amount) }}</span></div>
      </div>
      <div style="color:#3f3f46; margin-bottom:12px;">========================================</div>
      <div style="background-color:#1a1a1a; padding:12px; border-radius:12px; border:1px solid #2a2a2a; font-size:10px; line-height:2; margin-bottom:12px;">
        <div>• Metode Bayar : <span style="color:#ffffff; font-weight:700; text-transform:uppercase;">{{ selectedOrder?.payment_method || 'Cash' }}</span></div>
        <div>• Kasir : <span style="color:#ffffff; font-weight:700;">{{ selectedOrder?.kasir_name || kasirName }}</span></div>
        <div>• Status : <span :style="selectedOrder?.payment_status === 'paid' ? 'color:#34d399; font-weight:700;' : 'color:#fbbf24; font-weight:700;'">{{ (selectedOrder?.payment_status || 'PENDING').toUpperCase() }}</span></div>
      </div>
      <div style="text-align:center; font-size:10px; color:#a1a1aa; padding-top:4px; font-weight:700;">Terima kasih sudah makan di Masashimura! 🙏</div>
    </div>

    <!-- ── MODAL LUNASI ────────────────────────────────────────────── -->
    <div v-if="isPayModalOpen && selectedPayOrder" class="modal-overlay" @click.self="isPayModalOpen = false">
      <div class="pay-modal-box">
        <div class="modal-header">
          <div>
            <p class="modal-eyebrow">Konfirmasi Pembayaran</p>
            <h2 class="modal-title">{{ selectedPayOrder.order_number }}</h2>
          </div>
          <button class="modal-close" @click="isPayModalOpen = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>

        <div class="pay-body">
          <!-- Customer info -->
          <div class="pay-customer">
            <p class="pay-name">{{ selectedPayOrder.customer_name || 'Walk In' }}</p>
            <p class="pay-phone">{{ selectedPayOrder.customer_phone || 'Tanpa nomor' }}</p>
          </div>

          <!-- Total -->
          <div class="pay-total-strip">
            <span class="pay-total-label">Total Tagihan</span>
            <span class="pay-total-val">{{ formatPrice(selectedPayOrder.total_price) }}</span>
          </div>

          <!-- Method selector -->
          <div class="pay-section">
            <p class="pay-section-label">Metode Pembayaran</p>
            <div class="pay-method-grid">
              <button
                @click="payMethod = 'cash'"
                class="pay-method-btn"
                :class="{ active: payMethod === 'cash' }"
              >
                <span class="method-btn-icon">💵</span>
                Cash
              </button>
              <button
                @click="payMethod = 'qris_manual'"
                class="pay-method-btn"
                :class="{ active: payMethod === 'qris_manual' }"
              >
                <span class="method-btn-icon">📱</span>
                QRIS
              </button>
            </div>
          </div>

          <!-- Cash amount -->
          <div v-if="payMethod === 'cash'" class="pay-section">
            <p class="pay-section-label">Uang Diterima</p>
            <input
              v-model.number="payAmountPaid"
              type="number"
              placeholder="0"
              class="pay-amount-input"
            />
            <div
              v-if="payAmountPaid > 0 && payAmountPaid >= parseFloat(selectedPayOrder.total_price)"
              class="change-box change-ok"
            >
              <span>Kembalian</span>
              <span>{{ formatPrice(payAmountPaid - parseFloat(selectedPayOrder.total_price)) }}</span>
            </div>
            <div
              v-else-if="payAmountPaid > 0 && payAmountPaid < parseFloat(selectedPayOrder.total_price)"
              class="change-box change-err"
            >
              <span>⚠ Kurang</span>
              <span>{{ formatPrice(parseFloat(selectedPayOrder.total_price) - payAmountPaid) }}</span>
            </div>
          </div>

          <button
            @click="confirmPay"
            :disabled="isPaying || (payMethod === 'cash' && payAmountPaid > 0 && payAmountPaid < parseFloat(selectedPayOrder.total_price))"
            class="pay-confirm-btn"
          >
            {{ isPaying ? 'Memproses...' : 'Konfirmasi Lunas' }}
          </button>
        </div>
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
  currentDate.value.toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
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
  } catch (err) { console.error("Gagal tarik data:", err); }
};

const filteredOrders = computed(() =>
  orders.value.filter(o => (o.customer_phone || "").includes(searchQuery.value))
);

const openOrderModal = (order) => { selectedOrder.value = order; isModalOpen.value = true; };
const openPayModal = (order) => {
  selectedPayOrder.value = order;
  payMethod.value        = order.payment_method || "cash";
  payAmountPaid.value    = 0;
  isPayModalOpen.value   = true;
};

const confirmPay = async () => {
  if (!selectedPayOrder.value) return;
  isPaying.value = true;
  try {
    await apiClient.patch(`/orders/${selectedPayOrder.value.id}/pay/`, {
      payment_method: payMethod.value,
      amount_paid:    payMethod.value === 'cash' ? payAmountPaid.value : 0,
      kasir_name:     kasirName.value,
    });
    toast.success(`Order ${selectedPayOrder.value.order_number} berhasil dilunasi`);
    isPayModalOpen.value = false; selectedPayOrder.value = null; payAmountPaid.value = 0;
    fetchActiveOrders();
  } catch { toast.error("Gagal melunasi pembayaran"); }
  finally { isPaying.value = false; }
};

const shareReceiptAsImage = async () => {
  if (!receiptRef.value || !selectedOrder.value) return;
  isCapturing.value = true;
  await new Promise(r => setTimeout(r, 200));
  try {
    const canvas = await html2canvas(receiptRef.value, { backgroundColor: '#0f0f0f', scale: 2, useCORS: true });
    canvas.toBlob(async (blob) => {
      if (!blob) { toast.error("Gagal membuat gambar struk"); isCapturing.value = false; return; }
      const file = new File([blob], `struk-${selectedOrder.value.order_number}.png`, { type: 'image/png' });
      if (navigator.share && navigator.canShare?.({ files: [file] })) {
        await navigator.share({ files: [file], text: 'Bukti Pembelian di Masashimura 🙏' });
      } else {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url; a.download = file.name; a.click();
        URL.revokeObjectURL(url);
        const phone = (selectedOrder.value.customer_phone || '').startsWith('0')
          ? '62' + selectedOrder.value.customer_phone.slice(1) : selectedOrder.value.customer_phone || '';
        const caption = encodeURIComponent('Bukti Pembelian di Masashimura 🙏');
        setTimeout(() => window.open(phone ? `https://wa.me/${phone}?text=${caption}` : `https://wa.me/?text=${caption}`, '_blank'), 500);
        toast.info("Gambar diunduh. Lampirkan ke WhatsApp secara manual jika perlu.");
      }
      isCapturing.value = false;
    }, 'image/png');
  } catch (err) { console.error(err); toast.error("Gagal screenshot struk"); isCapturing.value = false; }
};

const computedSubtotal = computed(() => {
  const items = selectedOrder.value?.items || [];
  if (items.length) return items.reduce((sum, item) => sum + (parseFloat(item.price) * parseInt(item.quantity || 1)), 0);
  return parseFloat(selectedOrder.value?.subtotal || selectedOrder.value?.total_price || 0);
});

const formatPrice = (p) => new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(p || 0);
const formatTime = (s) => new Date(s).toLocaleTimeString('id-ID', { hour: "2-digit", minute: "2-digit", hour12: false });
const formatFullDateTime = (s) => new Date(s).toLocaleString('id-ID', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) + ' WIB';

onMounted(() => { fetchActiveOrders(); pollingTimer = setInterval(fetchActiveOrders, 5000); });
onUnmounted(() => { if (pollingTimer) clearInterval(pollingTimer); });
</script>

<style scoped>
/* ── Root ─────────────────────────────────────────────────────────── */
.ao-root {
  min-height: 100vh;
  background: #080808;
  color: #fff;
  padding: 2rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: 'Inter', sans-serif;
}

/* ── Page Header ─────────────────────────────────────────────────── */
.ao-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1.75rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-wrap: wrap;
}
.ao-eyebrow {
  font-family: 'Oswald', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #dc2626;
  margin: 0 0 0.3rem;
}
.ao-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin: 0 0 0.3rem;
}
.ao-date-label {
  font-size: 0.72rem;
  color: rgba(255,255,255,0.3);
  margin: 0;
}
.ao-header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* Date navigator */
.date-nav {
  display: flex;
  align-items: center;
  gap: 0;
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  overflow: hidden;
}
.date-nav-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.55rem 0.85rem;
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.45);
  font-family: 'Oswald', sans-serif;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.15s;
}
.date-nav-btn:hover { background: rgba(255,255,255,0.04); color: #fff; }
.date-nav-current {
  padding: 0.55rem 1rem;
  font-family: monospace;
  font-size: 0.8rem;
  color: #fff;
  border-left: 1px solid rgba(255,255,255,0.06);
  border-right: 1px solid rgba(255,255,255,0.06);
}

/* Search */
.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon {
  position: absolute;
  left: 0.75rem;
  color: rgba(255,255,255,0.25);
  pointer-events: none;
}
.search-input {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 0.55rem 0.85rem 0.55rem 2.25rem;
  color: #fff;
  font-size: 0.82rem;
  font-family: 'Inter', sans-serif;
  outline: none;
  width: 200px;
  transition: border-color 0.15s;
}
.search-input::placeholder { color: rgba(255,255,255,0.2); }
.search-input:focus { border-color: rgba(220,38,38,0.5); }

/* ── Table Card ───────────────────────────────────────────────────── */
.ao-table-card {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  overflow: hidden;
}

/* Summary strip */
.ao-summary {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.85rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  background: rgba(255,255,255,0.01);
}
.summary-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.72rem;
  color: rgba(255,255,255,0.4);
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.summary-dot {
  width: 6px; height: 6px; border-radius: 50%;
}
.dot-all     { background: rgba(255,255,255,0.3); }
.dot-pending { background: #f59e0b; }
.dot-paid    { background: #22c55e; }

/* Table */
.table-scroll { overflow-x: auto; }
.ao-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}
.ao-table th {
  padding: 0.7rem 1.25rem;
  font-family: 'Oswald', sans-serif;
  font-size: 0.58rem;
  font-weight: 400;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.22);
  text-align: left;
  background: rgba(255,255,255,0.015);
  white-space: nowrap;
}
.th-center { text-align: center; }
.th-right  { text-align: right; }

.ao-row {
  border-top: 1px solid rgba(255,255,255,0.04);
  cursor: pointer;
  transition: background 0.12s;
}
.ao-row:hover { background: rgba(255,255,255,0.025); }
.ao-table td {
  padding: 0.9rem 1.25rem;
  font-size: 0.85rem;
  vertical-align: middle;
}

.td-id { font-family: monospace; font-weight: 700; color: #dc2626; font-size: 0.82rem; }

.td-customer { display: flex; align-items: center; gap: 0.5rem; }
.customer-phone { font-family: monospace; font-size: 0.82rem; color: rgba(255,255,255,0.8); }
.guest-badge {
  font-size: 0.55rem; padding: 0.1rem 0.4rem;
  border-radius: 4px; border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.25);
  font-family: 'Oswald', sans-serif; letter-spacing: 0.08em; text-transform: uppercase;
}

.td-right { text-align: right; }
.td-price { font-family: monospace; font-weight: 700; color: #fbbf24; }

.td-center { text-align: center; }

.status-pill {
  display: inline-block;
  padding: 0.22rem 0.65rem;
  border-radius: 100px;
  font-size: 0.62rem;
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 500;
}
.pill-green  { background: rgba(34,197,94,0.1);  color: #4ade80; border: 1px solid rgba(34,197,94,0.2); }
.pill-amber  { background: rgba(245,158,11,0.1); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2); }
.pill-yellow { background: rgba(234,179,8,0.08); color: #facc15; border: 1px solid rgba(234,179,8,0.18); }

.td-method { font-size: 0.8rem; color: rgba(255,255,255,0.55); text-transform: capitalize; }
.method-icon { margin-right: 0.2rem; }

.td-time { font-family: monospace; font-size: 0.78rem; color: rgba(255,255,255,0.3); }
.td-dash { color: rgba(255,255,255,0.15); font-size: 0.8rem; }

.lunasi-btn {
  padding: 0.4rem 1rem;
  background: #dc2626;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-family: 'Oswald', sans-serif;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.15s;
}
.lunasi-btn:hover { background: #b91c1c; }

/* Empty state */
.ao-empty {
  padding: 4rem 2rem !important;
  text-align: center;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.empty-text { color: rgba(255,255,255,0.3); font-size: 0.875rem; margin: 0 0 0.3rem; }
.empty-hint { color: rgba(255,255,255,0.15); font-size: 0.7rem; margin: 0; }

/* ── Modal overlay ───────────────────────────────────────────────── */
.modal-overlay {
  position: fixed; inset: 0; z-index: 50;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  padding: 1rem;
}

/* ── Receipt Modal ───────────────────────────────────────────────── */
.modal-box {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  width: 100%; max-width: 420px;
  max-height: 90vh;
  display: flex; flex-direction: column;
  overflow: hidden;
}
.modal-header {
  display: flex; align-items: flex-start;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.modal-eyebrow {
  font-family: 'Oswald', sans-serif;
  font-size: 0.58rem; letter-spacing: 0.18em;
  text-transform: uppercase; color: #dc2626; margin: 0 0 0.25rem;
}
.modal-title { font-family: monospace; font-size: 1rem; font-weight: 700; margin: 0; }
.modal-close {
  width: 30px; height: 30px; border-radius: 8px;
  background: rgba(255,255,255,0.05); border: none;
  color: rgba(255,255,255,0.4); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s; flex-shrink: 0;
}
.modal-close:hover { background: rgba(255,255,255,0.1); color: #fff; }

.receipt-body {
  padding: 1.25rem 1.5rem;
  overflow-y: auto; flex: 1;
  font-family: 'Courier New', monospace; font-size: 0.78rem;
  color: rgba(255,255,255,0.7);
}
.receipt-logo-area { text-align: center; margin-bottom: 1rem; }
.receipt-logo { height: 50px; margin: 0 auto 0.5rem; display: block; object-fit: contain; }
.receipt-address { font-size: 0.65rem; color: rgba(255,255,255,0.25); }
.receipt-divider { text-align: center; color: rgba(255,255,255,0.1); margin: 0.75rem 0; font-size: 0.7rem; letter-spacing: 0.1em; }

.receipt-meta { display: flex; flex-direction: column; gap: 0.25rem; }
.meta-row { display: flex; justify-content: space-between; font-size: 0.72rem; }
.meta-val { color: #fff; font-weight: 600; }

.receipt-items { margin-bottom: 0.5rem; }
.items-heading { font-size: 0.65rem; font-weight: 700; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.12em; margin: 0 0 0.6rem; }
.item-row { margin-bottom: 0.5rem; }
.item-main { display: flex; gap: 0.4rem; }
.item-qty { color: rgba(255,255,255,0.35); min-width: 1.8rem; }
.item-name { flex: 1; color: #fff; }
.item-subtotal { color: rgba(255,255,255,0.7); font-weight: 600; }
.item-note { font-size: 0.65rem; color: #fbbf24; padding-left: 2.2rem; font-style: italic; margin-top: 0.15rem; }

.receipt-totals { display: flex; flex-direction: column; gap: 0.3rem; }
.total-row { display: flex; justify-content: space-between; font-size: 0.75rem; }
.total-discount { color: #f87171; }
.total-final { font-size: 0.9rem; font-weight: 900; color: #fff; padding-top: 0.4rem; border-top: 1px dashed rgba(255,255,255,0.1); margin-top: 0.25rem; }
.total-final span:last-child { color: #ef4444; }
.total-paid { color: rgba(255,255,255,0.5); }
.total-change span:last-child { color: #34d399; font-weight: 700; }

.receipt-info-card {
  margin-top: 1rem;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  display: flex; flex-direction: column; gap: 0.25rem;
}
.info-row { display: flex; justify-content: space-between; font-size: 0.7rem; }
.info-val { color: #fff; font-weight: 700; text-transform: uppercase; }
.info-paid   { color: #34d399; font-weight: 700; }
.info-pending{ color: #fbbf24; font-weight: 700; }

.modal-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(255,255,255,0.06);
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;
}
.btn-share {
  display: flex; align-items: center; justify-content: center; gap: 0.4rem;
  padding: 0.7rem; background: #16a34a; border: none;
  border-radius: 10px; color: #fff;
  font-family: 'Oswald', sans-serif; font-size: 0.7rem;
  letter-spacing: 0.1em; text-transform: uppercase;
  cursor: pointer; transition: background 0.15s;
}
.btn-share:hover:not(:disabled) { background: #15803d; }
.btn-share:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-close-modal {
  padding: 0.7rem; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
  color: rgba(255,255,255,0.5);
  font-family: 'Oswald', sans-serif; font-size: 0.7rem;
  letter-spacing: 0.1em; text-transform: uppercase;
  cursor: pointer; transition: all 0.15s;
}
.btn-close-modal:hover { background: rgba(255,255,255,0.08); color: #fff; }

/* ── Pay Modal ───────────────────────────────────────────────────── */
.pay-modal-box {
  background: #0f0f0f;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  width: 100%; max-width: 400px;
  overflow: hidden;
}
.pay-body { padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 1.1rem; }

.pay-customer {
  padding: 0.85rem 1rem;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px;
}
.pay-name { font-weight: 600; font-size: 0.9rem; margin: 0 0 0.2rem; }
.pay-phone { font-family: monospace; font-size: 0.75rem; color: rgba(255,255,255,0.35); margin: 0; }

.pay-total-strip {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.85rem 1rem;
  background: rgba(220,38,38,0.06);
  border: 1px solid rgba(220,38,38,0.15);
  border-radius: 10px;
}
.pay-total-label { font-size: 0.72rem; color: rgba(255,255,255,0.4); font-family: 'Oswald', sans-serif; letter-spacing: 0.1em; text-transform: uppercase; }
.pay-total-val { font-family: monospace; font-size: 1.15rem; font-weight: 800; color: #ef4444; }

.pay-section { display: flex; flex-direction: column; gap: 0.5rem; }
.pay-section-label { font-size: 0.6rem; font-family: 'Oswald', sans-serif; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(255,255,255,0.3); }

.pay-method-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
.pay-method-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.4rem;
  padding: 0.7rem; border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.02);
  color: rgba(255,255,255,0.4);
  font-family: 'Oswald', sans-serif; font-size: 0.75rem;
  letter-spacing: 0.08em; text-transform: uppercase;
  cursor: pointer; transition: all 0.15s;
}
.pay-method-btn:hover { border-color: rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); }
.pay-method-btn.active { background: rgba(220,38,38,0.12); border-color: #dc2626; color: #fff; }
.method-btn-icon { font-size: 1rem; }

.pay-amount-input {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #fff;
  font-family: monospace; font-size: 1rem;
  outline: none; width: 100%;
  transition: border-color 0.15s;
}
.pay-amount-input::placeholder { color: rgba(255,255,255,0.15); }
.pay-amount-input:focus { border-color: rgba(220,38,38,0.4); }

.change-box {
  display: flex; justify-content: space-between;
  padding: 0.6rem 0.85rem;
  border-radius: 8px; font-family: monospace; font-size: 0.8rem; font-weight: 700;
}
.change-ok  { background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); color: #4ade80; }
.change-err { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: #f87171; }

.pay-confirm-btn {
  width: 100%; padding: 0.85rem;
  background: #dc2626; border: none; border-radius: 12px;
  color: #fff; font-family: 'Oswald', sans-serif;
  font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase;
  cursor: pointer; transition: background 0.15s; font-weight: 500;
}
.pay-confirm-btn:hover:not(:disabled) { background: #b91c1c; }
.pay-confirm-btn:disabled { opacity: 0.35; cursor: not-allowed; }

/* ── Responsive ─────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .ao-root { padding: 1.25rem 1rem; }
  .ao-title { font-size: 1.4rem; }
  .ao-header { flex-direction: column; gap: 1rem; }
  .ao-header-right { width: 100%; flex-direction: column; align-items: stretch; }
  .search-input { width: 100%; }
  .date-nav { width: 100%; justify-content: space-between; }
  .ao-summary { gap: 1rem; flex-wrap: wrap; }
}

/* Hide number spinners */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
input[type="number"] { -moz-appearance: textfield; }
</style>