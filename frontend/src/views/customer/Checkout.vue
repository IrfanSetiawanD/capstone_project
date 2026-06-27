<template>
  <div class="min-h-screen bg-[#050505] text-white pt-24 font-manrope pb-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12 py-6">
      <h2 class="font-oswald text-4xl font-bold uppercase tracking-tight mb-8">
        🛒 Checkout Pesanan
      </h2>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- KIRI: List Item -->
        <div class="lg:col-span-2 space-y-4">
          <div
            v-if="cartStore.isEmpty"
            class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-12 text-center"
          >
            <p class="text-white/40 mb-6">Keranjang kamu masih kosong nih.</p>
            <router-link
              to="/menu"
              class="inline-block bg-red-600 text-white font-oswald uppercase tracking-wider px-6 py-3 rounded-lg hover:bg-red-700 transition-all"
            >
              Lihat Menu
            </router-link>
          </div>

          <div
            v-for="item in Object.values(cartStore.cart)"
            :key="item.cartKey"
            class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl flex justify-between items-start gap-4"
          >
            <div class="min-w-0">
              <h6 class="font-bold text-lg mb-1 truncate">{{ item.name }}</h6>
              <span class="text-sm text-white/40">
                Rp {{ Number(item.price).toLocaleString("id-ID") }} x
                {{ item.quantity }}
              </span>
              <p v-if="item.notes" class="text-xs text-amber-400 italic mt-1">
                📋 "{{ item.notes }}"
              </p>
            </div>
            <div class="text-end flex-shrink-0">
              <div class="font-oswald text-xl font-bold text-amber-400">
                Rp {{ (Number(item.price) * item.quantity).toLocaleString("id-ID") }}
              </div>
              <button
                class="text-xs text-red-500 hover:text-red-400 mt-2 transition"
                @click="cartStore.removeFromCart(item.cartKey)"
              >
                Hapus
              </button>
            </div>
          </div>
        </div>

        <!-- KANAN: Form & Payment -->
        <div class="lg:col-span-1">
          <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 sticky top-24 space-y-6">
            <h5 class="font-oswald text-xl font-bold uppercase tracking-wider">
              Data Pemesan
            </h5>

            <!-- Nama -->
            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">Nama</label>
              <input
                v-model="name"
                type="text"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-600 outline-none transition-all"
                placeholder="Nama kamu"
              />
            </div>

            <!-- Nomor WA -->
            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">Nomor WhatsApp</label>
              <input
                v-model="phone"
                type="tel"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-600 outline-none transition-all"
                placeholder="Contoh: 08123456789"
              />
              <p v-if="checkingLoyalty" class="text-[10px] text-white/30 mt-1.5">Mengecek status member...</p>
              <p v-else-if="cartStore.isLoyal" class="text-[10px] text-emerald-400 mt-1.5">
                ✓ Selamat! Kamu dapat diskon member {{ cartStore.discountPercent }}%
              </p>
            </div>

            <!-- Metode Pembayaran -->
            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">Metode Pembayaran</label>
              <div class="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  @click="selectPayment('cash')"
                  :class="[
                    'py-3 rounded-xl text-sm font-bold uppercase tracking-wider border transition-all',
                    paymentMethod === 'cash'
                      ? 'bg-red-600 border-red-600 text-white'
                      : 'bg-white/5 border-white/10 text-white/60 hover:border-white/30',
                  ]"
                >
                  💵 Cash
                </button>
                <button
                  type="button"
                  @click="selectPayment('qris')"
                  :class="[
                    'py-3 rounded-xl text-sm font-bold uppercase tracking-wider border transition-all',
                    paymentMethod === 'qris'
                      ? 'bg-red-600 border-red-600 text-white'
                      : 'bg-white/5 border-white/10 text-white/60 hover:border-white/30',
                  ]"
                >
                  📱 QRIS
                </button>
              </div>
            </div>

            <!-- QRIS Section -->
            <transition
              enter-active-class="transition-all duration-300"
              enter-from-class="opacity-0 -translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition-all duration-200"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div v-if="paymentMethod === 'qris'" class="space-y-4">
                <!-- Gambar QRIS -->
                <div class="bg-white rounded-2xl p-4 flex flex-col items-center gap-3">
                  <p class="text-black text-[10px] uppercase font-bold tracking-widest">Scan QRIS untuk Bayar</p>
                  <img
                    src="https://res.cloudinary.com/dndonk7an/image/upload/v1782554914/qris_masashimura_v8yvxd.jpg"
                    alt="QRIS Masashimura"
                    class="w-full max-w-[220px] rounded-xl"
                  />
                  <p class="text-black/50 text-[10px] text-center">Bayar sesuai total, lalu upload bukti di bawah</p>
                </div>

                <!-- Upload Bukti Bayar -->
                <div>
                  <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">
                    Bukti Pembayaran QRIS
                  </label>

                  <!-- Preview setelah upload -->
                  <div v-if="proofPreviewUrl" class="relative mb-3">
                    <img
                      :src="proofPreviewUrl"
                      alt="Bukti Bayar"
                      class="w-full rounded-xl border border-emerald-500/30 object-cover max-h-48"
                    />
                    <button
                      @click="clearProof"
                      class="absolute top-2 right-2 w-7 h-7 rounded-full bg-black/70 text-white text-xs flex items-center justify-center hover:bg-red-600 transition"
                    >
                      ✕
                    </button>
                    <div v-if="isUploadingProof" class="absolute inset-0 bg-black/60 rounded-xl flex flex-col items-center justify-center gap-2">
                      <div class="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                      <p class="text-xs text-white/70">Mengupload...</p>
                    </div>
                    <div v-else-if="proofCloudinaryUrl" class="absolute bottom-2 left-2 bg-emerald-500/90 text-white text-[10px] font-bold px-2 py-1 rounded-lg">
                      ✓ Terverifikasi
                    </div>
                  </div>

                  <!-- Input upload -->
                  <label
                    v-if="!proofPreviewUrl"
                    class="flex flex-col items-center justify-center gap-2 w-full border-2 border-dashed border-white/10 hover:border-red-500/50 rounded-xl py-6 cursor-pointer transition-all group"
                  >
                    <span class="text-2xl group-hover:scale-110 transition-transform">📸</span>
                    <span class="text-xs text-white/40 group-hover:text-white/60 transition">Klik untuk upload foto bukti</span>
                    <span class="text-[10px] text-white/20">JPG, PNG — Maks 5MB</span>
                    <input
                      type="file"
                      accept="image/*"
                      class="hidden"
                      @change="handleProofUpload"
                    />
                  </label>

                  <p v-if="uploadError" class="text-xs text-red-400 mt-1">{{ uploadError }}</p>
                </div>
              </div>
            </transition>

            <hr class="border-white/5" />

            <!-- Ringkasan Harga -->
            <div class="space-y-2">
              <div class="flex justify-between items-center text-sm text-white/60">
                <span>Subtotal</span>
                <span>Rp {{ cartStore.subtotal.toLocaleString("id-ID") }}</span>
              </div>
              <div v-if="cartStore.isLoyal" class="flex justify-between items-center text-sm text-emerald-400">
                <span>Diskon Member ({{ cartStore.discountPercent }}%)</span>
                <span>- Rp {{ cartStore.discountAmount.toLocaleString("id-ID") }}</span>
              </div>
              <div class="flex justify-between items-center pt-2">
                <span class="text-white/60">Total Bayar</span>
                <span class="font-oswald text-2xl font-bold text-amber-400">
                  Rp {{ cartStore.totalPrice.toLocaleString("id-ID") }}
                </span>
              </div>
            </div>

            <!-- Tombol Buat Pesanan -->
            <button
              class="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-oswald uppercase tracking-widest py-4 rounded-xl font-bold transition-all"
              @click="checkout"
              :disabled="isCheckoutDisabled"
            >
              {{ isProcessing ? "Memproses..." : "Buat Pesanan" }}
            </button>

            <!-- Hint kalau QRIS belum upload -->
            <p v-if="paymentMethod === 'qris' && !proofCloudinaryUrl && !cartStore.isEmpty" class="text-[10px] text-white/30 text-center -mt-3">
              Upload bukti bayar dulu sebelum buat pesanan
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { useCartStore } from "@/stores/cart";
import { orderAPI } from "@/api";
import { toast } from "vue-sonner";

const cartStore     = useCartStore();
const router        = useRouter();

const name          = ref("");
const phone         = ref("");
const paymentMethod = ref("cash");
const isProcessing  = ref(false);
const checkingLoyalty = ref(false);

// QRIS proof state
const proofPreviewUrl    = ref("");
const proofCloudinaryUrl = ref("");
const isUploadingProof   = ref(false);
const uploadError        = ref("");

const ADMIN_WHATSAPP   = import.meta.env.VITE_ADMIN_WHATSAPP || "6285773615870";
const CLOUDINARY_CLOUD = "dndonk7an";
const CLOUDINARY_PRESET = "masashimura_preset";
const CLOUDINARY_FOLDER = "bukti-qris";

// ── Loyalty ───────────────────────────────────────────────────────────────────
let debounceTimer = null;
watch(phone, (newPhone) => {
  clearTimeout(debounceTimer);
  if (!newPhone || newPhone.length < 9) {
    cartStore.isLoyal = false;
    cartStore.discountPercent = 0;
    return;
  }
  checkingLoyalty.value = true;
  debounceTimer = setTimeout(async () => {
    await cartStore.checkLoyalty(newPhone);
    checkingLoyalty.value = false;
  }, 600);
});
onBeforeUnmount(() => clearTimeout(debounceTimer));

// ── Payment method ────────────────────────────────────────────────────────────
const selectPayment = (method) => {
  paymentMethod.value = method;
  if (method === 'cash') {
    clearProof();
  }
};

// ── QRIS proof upload ─────────────────────────────────────────────────────────
const handleProofUpload = async (e) => {
  const file = e.target.files?.[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = "Ukuran file maksimal 5MB";
    return;
  }

  uploadError.value    = "";
  proofPreviewUrl.value = URL.createObjectURL(file);
  isUploadingProof.value = true;
  proofCloudinaryUrl.value = "";

  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", CLOUDINARY_PRESET);
    formData.append("folder", CLOUDINARY_FOLDER);

    const res = await fetch(
      `https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD}/image/upload`,
      { method: "POST", body: formData }
    );

    if (!res.ok) throw new Error("Upload gagal");

    const data = await res.json();
    proofCloudinaryUrl.value = data.secure_url;
    toast.success("Bukti pembayaran berhasil diupload!");
  } catch (err) {
    uploadError.value = "Gagal upload bukti, coba lagi.";
    proofPreviewUrl.value = "";
    toast.error("Upload bukti gagal");
  } finally {
    isUploadingProof.value = false;
  }
};

const clearProof = () => {
  proofPreviewUrl.value    = "";
  proofCloudinaryUrl.value = "";
  uploadError.value        = "";
};

// ── Computed disabled state ───────────────────────────────────────────────────
const isCheckoutDisabled = computed(() => {
  if (cartStore.isEmpty || !phone.value || !name.value || isProcessing.value) return true;
  if (paymentMethod.value === 'qris' && !proofCloudinaryUrl.value) return true;
  return false;
});

// ── WA message ────────────────────────────────────────────────────────────────
const sendToWhatsApp = (orderNumber) => {
  const itemsText = Object.values(cartStore.cart)
    .map((item) => {
      const line = `   • ${item.name} x${item.quantity} — Rp ${(Number(item.price) * item.quantity).toLocaleString("id-ID")}`;
      return item.notes ? `${line}\n     📋 ${item.notes}` : line;
    })
    .join("\n");

  const loyaltyLine = cartStore.isLoyal
    ? `Diskon Member (${cartStore.discountPercent}%): -Rp ${cartStore.discountAmount.toLocaleString("id-ID")}\n`
    : "";

  // Taruh link bukti di tengah pesan (bukan di awal) supaya WA tidak auto-preview card Cloudinary
  const proofLine = proofCloudinaryUrl.value
    ? `\nBukti Bayar QRIS:\n${proofCloudinaryUrl.value}\n`
    : "";

  const message =
    `*ORDER BARU - MASASHIMURA*\n` +
    `===========================\n` +
    `No. Order  : *#${orderNumber}*\n` +
    `Nama       : ${name.value}\n` +
    `WhatsApp   : ${phone.value}\n` +
    `Pembayaran : ${paymentMethod.value === 'qris' ? 'QRIS' : 'Cash'}\n` +
    `===========================\n` +
    `*Pesanan:*\n` +
    `${itemsText}\n` +
    `===========================\n` +
    `${loyaltyLine}` +
    `*TOTAL: Rp ${cartStore.totalPrice.toLocaleString("id-ID")}*\n` +
    `${proofLine}` +
    `===========================\n` +
    `Mohon segera diproses, terima kasih!`;

  const waURL = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(message)}`;
  window.open(waURL, "_blank");
};

// ── Checkout ──────────────────────────────────────────────────────────────────
const checkout = async () => {
  if (!name.value)  return toast.error("Mohon isi nama kamu");
  if (!phone.value) return toast.error("Mohon isi nomor WhatsApp");
  if (paymentMethod.value === 'qris' && !proofCloudinaryUrl.value) {
    return toast.error("Upload bukti pembayaran QRIS dulu ya!");
  }

  isProcessing.value = true;
  try {
    const orderData = {
      source:         "web",
      customer:       { phone: phone.value, name: name.value },
      payment_method: paymentMethod.value,
      items: Object.values(cartStore.cart).map((item) => ({
        menu_id:  item.id,
        quantity: item.quantity,
        price:    item.price,
        notes:    item.notes || "",
      })),
    };

    const res         = await orderAPI.create(orderData);
    const orderNumber = res.data?.order_number ?? res.data?.id;

    toast.success("Pesanan berhasil dibuat!");
    sendToWhatsApp(orderNumber);

    cartStore.clearCart();
    name.value  = "";
    phone.value = "";
    clearProof();

    router.push("/");
  } catch (error) {
    console.error("Checkout gagal:", error);
    toast.error(
      "Gagal memproses pesanan: " +
      (error.response?.data?.detail || error.response?.data?.error || "Koneksi terputus")
    );
  } finally {
    isProcessing.value = false;
  }
};
</script>