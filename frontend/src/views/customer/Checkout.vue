<template>
  <div class="min-h-screen bg-[#050505] text-white pt-24 font-manrope">
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
            :key="item.id"
            class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl flex justify-between items-center"
          >
            <div>
              <h6 class="font-bold text-lg mb-1">{{ item.name }}</h6>
              <span class="text-sm text-white/40">
                Rp {{ Number(item.price).toLocaleString("id-ID") }} x
                {{ item.quantity }}
              </span>
            </div>
            <div class="text-end">
              <div class="font-oswald text-xl font-bold text-amber-400">
                Rp
                {{
                  (Number(item.price) * item.quantity).toLocaleString("id-ID")
                }}
              </div>
              <button
                class="text-xs text-red-500 hover:text-red-400 mt-2 transition"
                @click="cartStore.removeFromCart(item.id)"
              >
                Hapus
              </button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div
            class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 sticky top-24"
          >
            <h5
              class="font-oswald text-xl font-bold uppercase tracking-wider mb-4"
            >
              Ringkasan
            </h5>
            <hr class="border-white/5 mb-6" />

            <div class="flex justify-between items-center mb-6">
              <span class="text-white/60">Total Harga:</span>
              <span class="font-oswald text-2xl font-bold text-amber-400">
                Rp {{ cartStore.totalPrice.toLocaleString("id-ID") }}
              </span>
            </div>

            <div class="mb-6">
              <label
                class="block text-[10px] uppercase text-white/40 mb-2 tracking-widest font-bold"
              >
                Nomor WhatsApp Anda
              </label>
              <input
                v-model="phone"
                type="tel"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-600 outline-none transition-all"
                placeholder="Contoh: 08123456789"
              />
            </div>

            <button
              class="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-oswald uppercase tracking-widest py-4 rounded-xl font-bold transition-all"
              @click="checkout"
              :disabled="cartStore.isEmpty || !phone || isProcessing"
            >
              {{ isProcessing ? "Memproses..." : "Checkout via WhatsApp" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCartStore } from "@/stores/cart";
import { orderAPI } from "@/api";
import { toast } from "vue-sonner";

const cartStore = useCartStore();
const phone = ref("");
const isProcessing = ref(false);

const checkout = async () => {
  if (!phone.value) {
    toast.error("Mohon isi nomor WhatsApp Anda");
    return;
  }

  isProcessing.value = true;
  try {
    const orderData = {
      phone: phone.value,
      payment_method: "cash",
      final_price: cartStore.totalPrice,
      items: Object.values(cartStore.cart).map((item) => ({
        menu_id: item.id,
        quantity: item.quantity,
        price: item.price,
      })),
    };

    const res = await orderAPI.create(orderData);

    toast.success("Pesanan berhasil dibuat!");
    cartStore.clearCart();

    // Redirect ke link WA jika ada
    if (res.data?.wa_link) {
      window.location.href = res.data.wa_link;
    } else {
      // Fallback jika tidak ada link, arahkan ke halaman utama
      window.location.href = "/";
    }
  } catch (error) {
    console.error("Checkout gagal:", error);
    toast.error("Gagal memproses pesanan. Silakan hubungi admin.");
  } finally {
    isProcessing.value = false;
  }
};
</script>
