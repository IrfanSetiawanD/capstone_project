<template>
  <div class="fixed inset-0 z-[60] flex justify-end">
    <div
      class="absolute inset-0 bg-black/80 backdrop-blur-sm"
      @click="$emit('close')"
    ></div>

    <div
      class="relative w-full max-w-md bg-[#050505] h-full shadow-2xl flex flex-col border-l border-white/5"
    >
      <!-- HEADER PANEL -->
      <div
        class="p-6 border-b border-white/5 flex justify-between items-center bg-[#0a0a0a]"
      >
        <h2
          class="font-oswald text-2xl font-bold text-red-600 uppercase tracking-wider"
        >
          Keranjang
        </h2>
        <button
          @click="$emit('close')"
          class="text-white/30 hover:text-white transition-colors cursor-pointer"
        >
          <X size="24" />
        </button>
      </div>

      <!-- LIST ITEM BELANJAAN -->
      <div
        class="flex-grow overflow-y-auto p-6 space-y-6 bg-[#050505] custom-scroll"
      >
        <div v-if="cartStore.isEmpty" class="text-center py-20">
          <p class="text-white/40 font-inter font-light">
            Masih kosong nih :(
          </p>
          <router-link
            to="/menu"
            @click="$emit('close')"
            class="text-red-500 mt-4 inline-block underline font-oswald uppercase text-sm tracking-widest"
          >
            Lihat Menu
          </router-link>
        </div>

        <div
          v-else
          v-for="item in Object.values(cartStore.cart)"
          :key="item.cartKey"
          class="flex gap-4 group items-start"
        >
          <!-- Thumbnail Gambar Produk -->
          <div
            class="w-20 h-20 bg-gray-900 rounded-xl overflow-hidden border border-white/5 shadow-lg flex-shrink-0"
          >
            <img
              v-if="item.image_url"
              :src="getMediaUrl(item.image_url)"
              class="w-full h-full object-cover pointer-events-none"
              alt="menu image"
            />
            <div
              v-else
              class="w-full h-full flex items-center justify-center text-white/30 text-xs"
            >
              No Image
            </div>
          </div>

          <!-- Detail Menu + Kolom Input Catatan -->
          <div class="flex-grow min-w-0 space-y-1">
            <h4
              class="font-oswald text-white uppercase text-sm tracking-tight truncate"
            >
              {{ item.name }}
            </h4>

            <p class="text-amber-400 font-bold text-sm">
              {{ formatPrice(item.price * item.quantity) }}
            </p>

            <!-- LIVE INPUT CATATAN -->
            <div class="pt-1 pb-2">
              <input
                v-model="item.notes"
                type="text"
                placeholder="Catatan Menu"
                class="w-full bg-white/5 border border-white/10 rounded-md py-1.5 px-3 text-[11px] font-mono text-zinc-400 focus:border-red-600 outline-none transition"
              />
            </div>

            <!-- Kontrol Jumlah Porsi (Plus/Minus) -->
            <div class="flex items-center gap-3">
              <button
                @click="cartStore.updateQuantity(item.cartKey, -1)"
                class="w-8 h-8 flex items-center justify-center border border-white/10 rounded-md hover:bg-white/5 text-white/70 hover:text-white transition-all cursor-pointer"
              >
                −
              </button>
              <span
                class="text-white font-oswald font-bold text-base w-6 text-center"
              >
                {{ item.quantity }}
              </span>
              <button
                @click="cartStore.updateQuantity(item.cartKey, 1)"
                class="w-8 h-8 flex items-center justify-center border border-white/10 rounded-md hover:bg-white/5 text-white/70 hover:text-white transition-all cursor-pointer"
              >
                +
              </button>
            </div>
          </div>

          <!-- Tombol Hapus Baris Dari Keranjang -->
          <button
            @click="cartStore.removeFromCart(item.cartKey)"
            class="text-white/10 hover:text-red-500 transition-colors p-2 cursor-pointer self-center"
          >
            <Trash2 size="18" />
          </button>
        </div>
      </div>

      <!-- RINGKASAN NOTA PEMBAYARAN -->
      <div
        v-if="!cartStore.isEmpty"
        class="p-6 border-t border-white/5 bg-[#0a0a0a]"
      >
        <div class="flex justify-between items-center mb-6">
          <span
            class="text-white/50 uppercase tracking-[0.2em] text-xs font-inter font-light"
          >
            Total Pembayaran
          </span>
          <span
            class="text-3xl font-oswald font-bold text-amber-400 tracking-tight"
          >
            {{ formatPrice(cartStore.totalPrice) }}
          </span>
        </div>

        <router-link to="/checkout" @click="$emit('close')" class="block text-center w-full bg-red-600 text-black font-oswald uppercase py-4 rounded-sm font-bold tracking-[0.2em] hover:bg-white hover:text-black transition-all duration-300 shadow-[0_10px_30px_rgba(220,38,38,0.3)]" >
          Pesan Sekarang
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from "@/stores/cart";
import { getMediaUrl } from "@/api";
import { X, Trash2 } from "lucide-vue-next";

const cartStore = useCartStore();

defineProps({
  formatPrice: Function,
});

defineEmits(["close"]);
</script>