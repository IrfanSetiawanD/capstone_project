<template>
  <div class="min-h-screen bg-[#050505] text-white pt-24 font-manrope pb-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12 py-6">
      <h2 class="font-oswald text-4xl font-bold uppercase tracking-tight mb-8">
        🛒 Checkout Pesanan
      </h2>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
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
                Rp
                {{ (Number(item.price) * item.quantity).toLocaleString("id-ID") }}
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

        <div class="lg:col-span-1">
          <div
            class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 sticky top-24 space-y-6"
          >
            <h5 class="font-oswald text-xl font-bold uppercase tracking-wider">
              Data Pemesan
            </h5>

            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">
                Nama
              </label>
              <input
                v-model="name"
                type="text"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-600 outline-none transition-all"
                placeholder="Nama kamu"
              />
            </div>

            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">
                Nomor WhatsApp
              </label>
              <input
                v-model="phone"
                type="tel"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-600 outline-none transition-all"
                placeholder="Contoh: 08123456789"
              />
              <p v-if="checkingLoyalty" class="text-[10px] text-white/30 mt-1.5">
                Mengecek status member...
              </p>
              <p v-else-if="cartStore.isLoyal" class="text-[10px] text-emerald-400 mt-1.5">
                ✓ Selamat! Kamu dapat diskon member {{ cartStore.discountPercent }}%
              </p>
            </div>

            <div>
              <label class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold">
                Metode Pembayaran
              </label>
              <div class="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  @click="paymentMethod = 'cash'"
                  :class="[
                    'py-3 rounded-xl text-sm font-bold uppercase tracking-wider border transition-all',
                    paymentMethod === 'cash'
                      ? 'bg-red-600 border-red-600 text-white'
                      : 'bg-white/5 border-white/10 text-white/60 hover:border-white/30',
                  ]"
                >
                  Cash
                </button>
                <button
                  type="button"
                  @click="paymentMethod = 'qris'"
                  :class="[
                    'py-3 rounded-xl text-sm font-bold uppercase tracking-wider border transition-all',
                    paymentMethod === 'qris'
                      ? 'bg-red-600 border-red-600 text-white'
                      : 'bg-white/5 border-white/10 text-white/60 hover:border-white/30',
                  ]"
                >
                  QRIS
                </button>
              </div>
            </div>

            <hr class="border-white/5" />

            <div class="space-y-2">
              <div class="flex justify-between items-center text-sm text-white/60">
                <span>Subtotal</span>
                <span>Rp {{ cartStore.subtotal.toLocaleString("id-ID") }}</span>
              </div>
              <div
                v-if="cartStore.isLoyal"
                class="flex justify-between items-center text-sm text-emerald-400"
              >
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

            <button
              class="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-oswald uppercase tracking-widest py-4 rounded-xl font-bold transition-all"
              @click="checkout"
              :disabled="cartStore.isEmpty || !phone || !name || isProcessing"
            >
              {{ isProcessing ? "Memproses..." : "Buat Pesanan" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { useCartStore } from "@/stores/cart";
import { orderAPI } from "@/api";
import { toast } from "vue-sonner";

const cartStore = useCartStore();
const router = useRouter();

const name = ref("");
const phone = ref("");
const paymentMethod = ref("cash");
const isProcessing = ref(false);
const checkingLoyalty = ref(false);

const ADMIN_WHATSAPP = import.meta.env.VITE_ADMIN_WHATSAPP || "6285773615870";

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

const sendToWhatsApp = (orderNumber) => {
  const itemsText = Object.values(cartStore.cart)
    .map((item) => {
      const line = `• ${item.name} x${item.quantity}`;
      return item.notes ? `${line} (Note: ${item.notes})` : line;
    })
    .join("\n");

  const message =
    `*ORDER BARU MASASHIMURA #${orderNumber}*\n` +
    `--------------------------\n` +
    `Nama: ${name.value}\n` +
    `No. WA: ${phone.value}\n` +
    `Pembayaran: ${paymentMethod.value.toUpperCase()}\n\n` +
    `*Item Pesanan:*\n${itemsText}\n\n` +
    `*Total: Rp ${cartStore.totalPrice.toLocaleString("id-ID")}*\n` +
    `--------------------------\n` +
    `Mohon segera diproses ya 🙏`;

  const waURL = `https://wa.me/${ADMIN_WHATSAPP}?text=${encodeURIComponent(message)}`;
  window.open(waURL, "_blank");
};

const checkout = async () => {
  if (!name.value) {
    toast.error("Mohon isi nama kamu");
    return;
  }
  if (!phone.value) {
    toast.error("Mohon isi nomor WhatsApp Anda");
    return;
  }

  isProcessing.value = true;
  try {
    const orderData = {
  source: "web",
  customer: {
    phone: phone.value,
    name: name.value,
  },
  payment_method: paymentMethod.value,
  items: Object.values(cartStore.cart).map((item) => {

    const finalPrice = Math.ceil((Number(item.price) * 1.01) / 500) * 500;
    
    return {
      menu_id: item.id,
      quantity: item.quantity,
      price: finalPrice, // Menggunakan harga markup
      notes: item.notes || "",
    };
  }),
};

    const res = await orderAPI.create(orderData);
    // FIX: OrderSerializer mengembalikan "id" & "order_number",
    // bukan "order_id" — sebelumnya selalu undefined.
    const orderNumber = res.data?.order_number ?? res.data?.id;

    toast.success("Pesanan berhasil dibuat!");
    sendToWhatsApp(orderNumber);

    cartStore.clearCart();
    name.value = "";
    phone.value = "";

    // Pindah halaman tanpa hard reload
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