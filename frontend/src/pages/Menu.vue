<template>
  <div class="min-h-screen pt-28 pb-32 bg-[#050505] text-white font-inter">
    <div class="max-w-7xl mx-auto px-4 sm:px-8">

      <div class="text-center mb-16 space-y-3 animate-fade-up">
        <span class="text-xs font-bold tracking-[0.3em] text-[#DC2626] uppercase font-mono">// Fresh Ingredients</span>
        <h1 class="font-sora text-4xl md:text-5xl font-extrabold uppercase tracking-tight text-white">Daftar Menu Kuliner</h1>
        <p class="text-zinc-500 text-xs sm:text-sm max-w-sm mx-auto font-light">
          Cita rasa premium perpaduan nuansa Jepang dengan kehangatan lokal yang ramah di kantong.
        </p>
      </div>

      <div class="flex flex-wrap gap-3 mb-16 justify-center text-xs font-sora font-bold uppercase tracking-wider">
        <button v-for="category in categories" :key="category.value"
          @click="selectedCategory = category.value"
          :class="['px-6 py-3 rounded-lg border transition-all duration-300 cursor-pointer', 
          selectedCategory === category.value ? 'bg-[#DC2626] text-white border-[#DC2626] shadow-[0_4px_20px_rgba(220,38,38,0.25)]' : 'bg-[#0F0F0F] text-zinc-400 border-white/5 hover:border-zinc-800 hover:text-white']">
          {{ category.label }}
        </button>
      </div>

      <div v-if="loading" class="text-center py-24 text-zinc-500 font-mono text-xs tracking-widest uppercase">
        <div class="inline-block animate-spin rounded-full h-5 w-5 border-2 border-[#DC2626] border-t-transparent mr-3 align-middle"></div>
        Memuat data menu...
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <div v-for="menu in filteredMenus" :key="menu.id" 
          class="bg-[#0F0F0F] border border-white/5 rounded-xl overflow-hidden group hover:border-zinc-800 transition-all duration-300 hover:scale-[1.02] flex flex-col justify-between relative">
          
          <div v-if="!menu.is_available" class="absolute inset-0 z-10 flex items-center justify-center bg-black/70 backdrop-blur-sm rounded-xl">
            <span class="font-oswald text-2xl font-bold tracking-widest text-red-500 border border-red-500 px-4 py-2">HABIS</span>
          </div>

          <div class="w-full aspect-[16/10] bg-zinc-900 overflow-hidden relative border-b border-white/5">
            <img v-if="menu.image_url" :src="getMediaUrl(menu.image_url)" 
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105 pointer-events-none" alt="Menu" />
            <div v-else class="w-full h-full flex items-center justify-center text-zinc-600 text-xs font-mono uppercase tracking-widest">No Image</div>
          </div>

          <div class="p-6 space-y-4 flex-1 flex flex-col justify-between">
            <div class="space-y-1.5">
              <h3 class="font-sora text-base font-bold text-white uppercase tracking-wide group-hover:text-[#DC2626] transition-colors">{{ menu.name }}</h3>
              <p class="text-zinc-500 text-xs font-light line-clamp-2 leading-relaxed">{{ menu.description || "Deskripsi racikan menu andalan spesial Masashimura." }}</p>
            </div>

            <div class="flex items-center justify-between pt-4 border-t border-white/5">
              <span class="font-mono text-sm font-bold text-amber-500">{{ formatPrice(menu.price) }}</span>
              <button @click="addToCart(menu)" :disabled="!menu.is_available"
                class="bg-white/5 hover:bg-[#DC2626] text-white p-3 rounded-lg transition-all duration-300 cursor-pointer border border-white/5 disabled:bg-gray-800 disabled:opacity-50">
                <Plus size="16" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <button v-if="cartStore.cartItemCount > 0" @click="isCartOpen = true"
        class="fixed bottom-10 right-10 z-50 bg-[#DC2626] text-white rounded-xl w-14 h-14 flex items-center justify-center shadow-[0_15px_40px_rgba(220,38,38,0.3)] hover:scale-105 transition-all">
        <ShoppingCart size="22" />
        <span class="absolute -top-1 -right-1 bg-white text-black text-[9px] font-bold w-4 h-4 rounded-full flex items-center justify-center">{{ cartStore.cartItemCount }}</span>
      </button>

      <Cart v-if="isCartOpen" @close="isCartOpen = false" :format-price="formatPrice" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "@/stores/auth";
import { menuAPI, getMediaUrl } from "@/api";
import { toast } from "vue-sonner";
import { ShoppingCart, Plus } from "lucide-vue-next";
import Cart from "@/components/ui/Cart.vue";

const cartStore = useCartStore();
const authStore = useAuthStore();
const menus = ref([]);
const loading = ref(true);
const selectedCategory = ref("all");
const isCartOpen = ref(false);

const categories = [
  { label: "Semua", value: "all" },
  { label: "Main Menu", value: "Makanan" },
  { label: "Dimsum & Cemilan", value: "Snacks" },
  { label: "Minuman Signature", value: "Minuman" },
];

const fetchMenus = async () => {
  try {
    loading.value = true;
    const response = await menuAPI.getAll();
    menus.value = response.data || [];
  } catch (error) {
    toast.error("Gagal memuat daftar menu.");
  } finally {
    loading.value = false;
  }
};

const filteredMenus = computed(() => {
  let list = selectedCategory.value === "all" ? menus.value : menus.value.filter(m => m.category === selectedCategory.value);
  return list.sort((a, b) => b.is_available - a.is_available);
});

const addToCart = (menu) => {
  if (!menu.is_available) return toast.error("Menu ini sedang habis!");
  cartStore.addToCart(menu);
  toast.success(`${menu.name} ditambahkan ke keranjang!`);
};

const formatPrice = (p) => new Intl.NumberFormat("id-ID", { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(p);

onMounted(fetchMenus);
</script>

<style scoped>
.animate-fade-up { animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes fadeUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
</style>