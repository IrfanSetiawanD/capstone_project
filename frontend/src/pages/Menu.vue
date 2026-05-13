<template>
  <div class="min-h-screen pt-20 pb-40">
    <div class="max-w-7xl mx-auto px-6 md:px-12 py-12">
      <div class="text-center mb-12">
        <span class="font-caveat text-accent text-2xl mb-4 block">Menu Kami</span>
        <h1 class="font-oswald text-5xl md:text-6xl font-bold text-white mb-4 uppercase italic tracking-tighter">
          Pilih Favoritmu
        </h1>
      </div>

      <div class="flex flex-wrap gap-4 mb-8 justify-center">
        <button
          v-for="category in categories"
          :key="category"
          @click="selectedCategory = category"
          :class="[
            'px-6 py-2 rounded-sm font-oswald uppercase tracking-widest text-sm transition-all duration-300',
            selectedCategory === category 
              ? 'bg-primary text-white shadow-neo-red' 
              : 'bg-card/50 text-white/70 border border-white/10 hover:bg-white/5'
          ]"
        >
          {{ category === 'all' ? 'Semua' : category }}
        </button>
      </div>

      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-primary mr-3"></div>
        <p class="text-white/70 font-oswald uppercase tracking-widest inline-block">Memuat menu...</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <div
          v-for="menu in filteredMenus"
          :key="menu.id"
          class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden group hover:border-primary/30 transition-all duration-500"
        >
          <div class="w-full aspect-[1147/644] bg-gray-900 rounded-t-2xl overflow-hidden">
            <img 
              v-if="menu.image_url"
              :src="`http://127.0.0.1:8000${menu.image_url}`"
              class="w-full h-full object-cover"
              alt="menu image"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-white/30 text-sm font-light">
              No Image
            </div>
          </div>

          <div class="p-6">
            <h3 class="font-oswald text-xl font-bold text-white mb-2 uppercase tracking-tight">{{ menu.name }}</h3>
            <p class="text-white/50 text-sm mb-6 line-clamp-2 font-light leading-relaxed">{{ menu.description || 'Deskripsi menu' }}</p>
            
            <div class="flex items-end justify-between">
              <span class="font-oswald text-2xl font-bold text-primary tracking-tighter">
                {{ formatPrice(menu.price) }}
              </span>

              <button
                @click="addToCart(menu)"
                class="bg-primary text-white p-3 rounded-xl hover:bg-white hover:text-black transition-all duration-300 shadow-lg"
              >
                <Plus size="20" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Floating Cart Button -->
      <button
        v-if="cartStore.cartItemCount > 0"
        @click="isCartOpen = !isCartOpen"
        class="fixed bottom-10 right-10 z-50 bg-primary text-white rounded-2xl w-16 h-16 flex items-center justify-center shadow-[0_20px_50px_rgba(220,38,38,0.3)] hover:scale-110 hover:-rotate-6 transition-all duration-300"
      >
        <ShoppingCart size="28" />
        <span v-if="cartStore.cartItemCount > 0" 
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
          {{ cartStore.cartItemCount }}
        </span>
      </button>

      <!-- Cart -->
      <Cart
        v-if="isCartOpen"
        :format-price="formatPrice"
        @close="isCartOpen = false"
        @order="handleOrder"
      />

      <!-- Order Type Modal -->
      <OrderTypeModal
        :open="showOrderTypeModal"
        @confirm="confirmOrder"
        @cancel="showOrderTypeModal = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCartStore } from '@/stores/cart'
import { menuAPI } from '@/api'
import { toast } from 'vue-sonner'
import { ShoppingCart, Plus } from 'lucide-vue-next'

import Cart from '@/components/ui/Cart.vue'
import OrderTypeModal from '@/components/ui/OrderTypeModal.vue'

const cartStore = useCartStore()

const menus = ref([])
const loading = ref(true)
const selectedCategory = ref('all')
const isCartOpen = ref(false)
const showOrderTypeModal = ref(false)

const categories = ['all', 'Makanan', 'Minuman', 'Snacks']

const fetchMenus = async () => {
  try {
    loading.value = true
    const categoryParam = selectedCategory.value === 'all' ? null : selectedCategory.value
    const response = await menuAPI.getAll(categoryParam)
    menus.value = response.data || []
  } catch (error) {
    console.error(error)
    toast.error('Gagal memuat menu')
  } finally {
    loading.value = false
  }
}

const filteredMenus = computed(() => {
  if (selectedCategory.value === 'all') return menus.value
  return menus.value.filter(menu => menu.category === selectedCategory.value)
})

const addToCart = (menu) => {
  cartStore.addToCart(menu)
  toast.success(`${menu.name} masuk keranjang!`)
}

const handleOrder = () => {
  if (cartStore.isEmpty) {
    toast.error("Keranjang kosong!")
    return
  }
  showOrderTypeModal.value = true
}

const confirmOrder = async (data) => {
  const { orderType, paymentMethod } = data

  try {
    const payload = {
      phone: "628123456789",
      items: Object.values(cartStore.cart).map(item => ({
        id: item.id,
        name: item.name,
        quantity: item.quantity,
        price: item.price
      })),
      total_price: cartStore.totalPrice,
      order_type: orderType,
      payment_method: paymentMethod
    }

    const response = await orderAPI.create(payload)

    if (response.status === 201 || response.status === 200) {
      const orderItemsText = Object.values(cartStore.cart)
        .map(item => `• ${item.name} x${item.quantity}`)
        .join('%0A')

      const message = `*PESANAN MASASHIMURA*%0A` +
                      `--------------------------%0A` +
                      `Tipe: ${orderType === 'dine-in' ? 'Makan di Tempat' : 'Bawa Pulang'}%0A` +
                      `Pembayaran: ${paymentMethod.toUpperCase()}%0A%0A` +
                      `*Pesanan:*%0A${orderItemsText}%0A%0A` +
                      `*Total: Rp ${cartStore.totalPrice.toLocaleString('id-ID')}*%0A` +
                      `--------------------------%0A` +
                      `_Terima kasih!_`

      window.open(`https://wa.me/6285773615870?text=${message}`, '_blank')

      toast.success("Pesanan berhasil dikirim ke WhatsApp!")

      showOrderTypeModal.value = false
      isCartOpen.value = false
      cartStore.clearCart()
    }
  } catch (error) {
    console.error(error)
    toast.error("Gagal mengirim pesanan")
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price)
}

onMounted(fetchMenus)
watch(selectedCategory, fetchMenus)
</script>