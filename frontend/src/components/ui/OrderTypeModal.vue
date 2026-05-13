<template>
  <div v-if="open" class="fixed inset-0 z-[70] flex items-center justify-center bg-black/90 backdrop-blur-md">
    <div class="bg-[#0a0a0a] w-full max-w-md rounded-3xl p-8">
      
      <h2 class="text-2xl font-oswald text-center mb-8">Konfirmasi Pesanan</h2>

      <!-- Tipe Pesanan -->
      <div class="mb-8">
        <p class="text-white/60 text-sm mb-3 font-medium">Tipe Pesanan</p>
        <div class="grid grid-cols-2 gap-3">
          <button 
            @click="orderType = 'dine-in'"
            :class="orderType === 'dine-in' ? 'bg-primary text-white border-primary' : 'bg-white/5 hover:bg-white/10 border-white/10'"
            class="border-2 py-6 rounded-2xl text-lg font-medium transition-all flex flex-col items-center gap-1">
            🍽️<br>Dine In
          </button>
          <button 
            @click="orderType = 'takeaway'"
            :class="orderType === 'takeaway' ? 'bg-primary text-white border-primary' : 'bg-white/5 hover:bg-white/10 border-white/10'"
            class="border-2 py-6 rounded-2xl text-lg font-medium transition-all flex flex-col items-center gap-1">
            📦<br>Takeaway
          </button>
        </div>
      </div>

      <!-- Metode Pembayaran -->
      <div class="mb-8">
        <p class="text-white/60 text-sm mb-3 font-medium">Metode Pembayaran</p>
        <div class="flex gap-3">
          <button 
            @click="paymentMethod = 'cash'"
            :class="paymentMethod === 'cash' ? 'bg-white text-black' : 'bg-white/5 hover:bg-white/10'"
            class="flex-1 py-5 rounded-2xl font-medium transition-all">
            💵 Cash
          </button>
          <button 
            @click="paymentMethod = 'qris'"
            :class="paymentMethod === 'qris' ? 'bg-white text-black' : 'bg-white/5 hover:bg-white/10'"
            class="flex-1 py-5 rounded-2xl font-medium transition-all">
            📱 QRIS
          </button>
        </div>
      </div>

      <!-- QRIS Preview (hanya muncul kalau pilih QRIS) -->
      <div v-if="paymentMethod === 'qris'" class="mb-8 bg-white/5 p-5 rounded-2xl text-center">
        <p class="text-sm text-white/70 mb-3">Scan QRIS ini untuk pembayaran</p>
        <img src="https://i.ibb.co/0jKzYkZ/qris-masashimura.png" 
             alt="QRIS Masashimura" 
             class="w-56 mx-auto rounded-xl" />
      </div>

      <!-- Nomor WhatsApp -->
      <div class="mb-8">
        <label class="block text-white/60 text-sm mb-2">Nomor WhatsApp Kamu</label>
        <input 
          v-model="customerPhone" 
          type="tel" 
          placeholder="628xxxxxxxxxx" 
          class="w-full bg-white/5 border border-white/10 rounded-2xl px-5 py-4 text-white focus:border-primary outline-none"
        />
      </div>

      <!-- Tombol -->
      <div class="flex gap-3">
        <button 
          @click="$emit('cancel')" 
          class="flex-1 py-4 border border-white/20 rounded-2xl text-white/70 hover:text-white">
          Batal
        </button>
        <button 
          @click="confirm"
          :disabled="!orderType || !paymentMethod || !customerPhone"
          class="flex-1 py-4 bg-primary text-white rounded-2xl font-bold disabled:opacity-50">
          Kirim Pesanan ke WA
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ open: Boolean })
const emit = defineEmits(['cancel', 'confirm'])

const orderType = ref(null)      // dine-in / takeaway
const paymentMethod = ref(null)  // cash / qris
const customerPhone = ref('')

const confirm = () => {
  if (!orderType.value || !paymentMethod.value || !customerPhone.value) return

  emit('confirm', {
    orderType: orderType.value,
    paymentMethod: paymentMethod.value,
    customerPhone: customerPhone.value
  })
}
</script>