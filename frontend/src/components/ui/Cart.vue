<template>
  <div class="fixed inset-0 z-[60] flex justify-end">
    <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="$emit('close')"></div>
    
    <div class="relative w-full max-w-md bg-[#050505] h-full shadow-2xl flex flex-col border-l border-white/5">
      
      <div class="p-6 border-b border-white/5 flex justify-between items-center bg-[#0a0a0a]">
        <h2 class="font-oswald text-2xl font-bold text-primary uppercase tracking-wider">Keranjang</h2>
        <button @click="$emit('close')" class="text-white/30 hover:text-white transition-colors">
          <X size="24" />
        </button>
      </div>

      <div class="flex-grow overflow-y-auto p-6 space-y-6 bg-[#050505]">
        <div v-if="cartStore.isEmpty" class="text-center py-20">
          <p class="text-white/40 font-manrope font-light">Masih kosong nih :(</p>
          <router-link to="/menu" @click="$emit('close')" class="text-primary mt-4 inline-block underline font-oswald uppercase text-sm tracking-widest">
            Lihat Menu
          </router-link>
        </div>

        <div v-else v-for="item in cartStore.cart" :key="item.id" class="flex gap-4 group items-center">
          <!-- GAMBAR DI KERANJANG (FULL URL) -->
          <div class="w-20 h-20 bg-gray-900 rounded-xl overflow-hidden border border-white/5 shadow-lg flex-shrink-0">
            <img 
              v-if="item.image_url"
              :src="`http://127.0.0.1:8000${item.image_url}`"
              class="w-full h-full object-cover"
              alt="menu image"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-white/30 text-xs">
              No Image
            </div>
          </div>
          
          <div class="flex-grow min-w-0">
            <h4 class="font-oswald text-white uppercase text-sm mb-1 tracking-tight truncate">{{ item.name }}</h4>
            <p class="text-accent font-bold text-sm mb-3">{{ formatPrice(item.price) }}</p>
            
            <div class="flex items-center gap-3">
              <button 
                @click="cartStore.updateQuantity(item.id, -1)" 
                class="w-8 h-8 flex items-center justify-center border border-white/10 rounded-md hover:bg-white/5 text-white/70 hover:text-white transition-all">
                −
              </button>
              <span class="text-white font-oswald font-bold text-base w-6 text-center">{{ item.quantity }}</span>
              <button 
                @click="cartStore.updateQuantity(item.id, 1)" 
                class="w-8 h-8 flex items-center justify-center border border-white/10 rounded-md hover:bg-white/5 text-white/70 hover:text-white transition-all">
                +
              </button>
            </div>
          </div>
          
          <button 
            @click="cartStore.removeFromCart(item.id)" 
            class="text-white/10 hover:text-red-500 transition-colors p-2">
            <Trash2 size="18" />
          </button>
        </div>
      </div>

      <div v-if="!cartStore.isEmpty" class="p-6 border-t border-white/5 bg-[#0a0a0a]">
        <div class="flex justify-between items-center mb-6">
          <span class="text-white/50 uppercase tracking-[0.2em] text-xs font-manrope font-light">Total Pembayaran</span>
          <span class="text-3xl font-oswald font-bold text-accent tracking-tight">{{ formatPrice(cartStore.totalPrice) }}</span>
        </div>
        
        <button 
          @click="$emit('order')"
          class="w-full bg-primary text-background font-oswald uppercase py-4 rounded-sm font-bold tracking-[0.2em] hover:bg-white transition-all duration-300 shadow-[0_10px_30px_rgba(220,38,38,0.3)] hover:translate-y-[-3px]"
        >
          Pesan Sekarang (WA)
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { X, Trash2 } from 'lucide-vue-next'

const cartStore = useCartStore()

defineProps({
  formatPrice: Function
})

defineEmits(['close', 'order'])
</script>