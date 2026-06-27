<template>
  <div class="w-full">
    <div class="max-w-7xl mx-auto space-y-8">

      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <p class="text-[10px] uppercase tracking-[0.3em] text-red-500 font-bold mb-2">Admin Panel</p>
          <h1 class="font-oswald text-4xl uppercase tracking-tight text-white">
            Loyal Customers
          </h1>
          <p class="text-white/30 text-xs mt-1.5">
            Syarat: min. 10 pesanan &amp; Rp 100.000 dalam 1 bulan
          </p>
        </div>
        <button
          @click="refreshData"
          class="px-5 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-xl flex items-center gap-2 text-xs font-bold uppercase tracking-widest transition-all text-white/60 hover:text-white"
        >
          <span class="text-sm">↺</span> Refresh
        </button>
      </div>

      <!-- Stats Summary -->
      <div class="grid grid-cols-3 gap-4">
        <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-5">
          <p class="text-[10px] uppercase tracking-widest text-white/30 font-bold mb-1">Total Member</p>
          <p class="font-oswald text-3xl font-bold text-white">{{ loyalty.loyalCustomers.length }}</p>
        </div>
        <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-5">
          <p class="text-[10px] uppercase tracking-widest text-white/30 font-bold mb-1">Loyal Member</p>
          <p class="font-oswald text-3xl font-bold text-emerald-400">{{ loyalCount }}</p>
        </div>
        <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-5">
          <p class="text-[10px] uppercase tracking-widest text-white/30 font-bold mb-1">Dapat Diskon</p>
          <p class="font-oswald text-3xl font-bold text-amber-400">{{ discountedCount }}</p>
        </div>
      </div>

      <!-- Loading -->
      <div
        v-if="loyalty.loading"
        class="text-center py-24 bg-[#0a0a0a] border border-white/5 rounded-2xl"
      >
        <div class="inline-block animate-spin rounded-full h-7 w-7 border-2 border-white/10 border-t-red-500 mb-4"></div>
        <p class="text-white/30 text-xs uppercase tracking-widest font-bold">Memuat data...</p>
      </div>

      <!-- Tabel -->
      <div v-else class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="border-b border-white/5">
              <tr class="text-[10px] uppercase font-bold tracking-[0.15em] text-white/25">
                <th class="px-6 py-5">Pelanggan</th>
                <th class="px-6 py-5">Periode</th>
                <th class="px-6 py-5 text-center">Pesanan</th>
                <th class="px-6 py-5 text-right">Total Belanja</th>
                <th class="px-6 py-5 text-center">Diskon</th>
                <th class="px-6 py-5 text-center">Status</th>
                <th class="px-6 py-5 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.04]">
              <tr
                v-for="customer in loyalty.loyalCustomers"
                :key="customer.phone"
                class="hover:bg-white/[0.015] transition-colors group"
              >
                <!-- Nomor HP -->
                <td class="px-6 py-5">
                  <p class="font-mono font-bold text-white text-sm tracking-wider">{{ customer.phone }}</p>
                </td>

                <!-- Periode -->
                <td class="px-6 py-5">
                  <p class="text-white/40 text-xs">{{ customer.month || "—" }}</p>
                </td>

                <!-- Jumlah Pesanan -->
                <td class="px-6 py-5 text-center">
                  <span class="font-oswald text-xl font-bold text-white">{{ customer.order_count || 0 }}</span>
                  <span class="text-white/20 text-xs ml-1">order</span>
                </td>

                <!-- Total Belanja -->
                <td class="px-6 py-5 text-right">
                  <span class="font-oswald font-bold text-amber-400">{{ formatPrice(customer.total_spent) }}</span>
                </td>

                <!-- Kolom Diskon -->
                <td class="px-6 py-5 text-center">
                  <div v-if="customer.special_discount_percentage != null" class="flex flex-col items-center gap-0.5">
                    <span class="font-oswald text-2xl font-bold text-red-500">{{ customer.special_discount_percentage }}%</span>
                    <span class="text-[9px] uppercase tracking-widest text-white/25 font-bold">Khusus</span>
                  </div>
                  <div v-else-if="customer.is_loyal" class="flex flex-col items-center gap-0.5">
                    <span class="font-oswald text-2xl font-bold text-emerald-400">{{ defaultDiscount }}%</span>
                    <span class="text-[9px] uppercase tracking-widest text-white/25 font-bold">Member</span>
                  </div>
                  <span v-else class="text-white/15 text-sm font-bold">—</span>
                </td>

                <!-- Status -->
                <td class="px-6 py-5 text-center">
                  <span
                    class="inline-block px-4 py-1.5 text-[10px] rounded-full font-bold uppercase tracking-widest border"
                    :class="customer.is_loyal
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                      : 'bg-white/5 text-white/30 border-white/10'"
                  >
                    {{ customer.is_loyal ? "Loyal" : "Regular" }}
                  </span>
                </td>

                <!-- Aksi -->
                <td class="px-6 py-5 text-center">
                  <button
                    @click="openDiscountModal(customer)"
                    :disabled="!customer.is_loyal"
                    class="px-4 py-2 text-[10px] font-bold uppercase tracking-widest rounded-lg transition-all"
                    :class="customer.is_loyal
                      ? 'bg-red-600/10 hover:bg-red-600 text-red-400 hover:text-white border border-red-600/30 hover:border-red-600'
                      : 'bg-transparent text-white/15 border border-white/5 cursor-not-allowed'"
                  >
                    {{ customer.special_discount_percentage != null ? 'Edit Diskon' : 'Beri Diskon' }}
                  </button>
                </td>
              </tr>

              <tr v-if="loyalty.loyalCustomers.length === 0">
                <td colspan="7" class="px-6 py-24 text-center">
                  <p class="text-white/20 text-sm font-medium">Belum ada data pelanggan</p>
                  <p class="text-white/10 text-xs mt-1">Data muncul setelah ada transaksi yang memenuhi syarat</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Diskon -->
    <transition
      enter-active-class="duration-200" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100"
      leave-active-class="duration-150" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="showDiscountModal"
        class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        @click.self="showDiscountModal = false"
      >
        <div class="bg-[#0f0f0f] border border-white/10 rounded-2xl p-6 w-full max-w-sm space-y-5">

          <div class="flex items-start justify-between">
            <div>
              <h3 class="font-oswald text-lg uppercase tracking-wide text-white">Atur Diskon Khusus</h3>
              <p class="text-xs text-white/30 mt-0.5 font-mono">{{ selectedCustomer?.phone }}</p>
            </div>
            <button @click="showDiscountModal = false" class="text-white/20 hover:text-white transition text-lg leading-none">✕</button>
          </div>

          <!-- Info diskon saat ini -->
          <div class="bg-white/5 rounded-xl p-4 space-y-1">
            <p class="text-[10px] uppercase tracking-widest text-white/30 font-bold">Diskon Saat Ini</p>
            <p class="font-oswald text-2xl font-bold" :class="selectedCustomer?.special_discount_percentage != null ? 'text-red-400' : 'text-emerald-400'">
              {{ selectedCustomer?.special_discount_percentage != null
                ? selectedCustomer.special_discount_percentage + '% (Khusus)'
                : defaultDiscount + '% (Member Default)' }}
            </p>
          </div>

          <div class="space-y-1.5">
            <label class="text-[10px] uppercase font-bold tracking-widest text-white/40">
              Diskon Baru (%)
            </label>
            <input
              v-model.number="discountInput"
              type="number"
              min="0"
              max="100"
              class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-red-600 transition"
              placeholder="Contoh: 25"
            />
            <p class="text-[10px] text-white/20 px-1">Kosongkan dan simpan untuk reset ke default {{ defaultDiscount }}%</p>
          </div>

          <div class="flex gap-3">
            <button
              @click="saveSpecialPrice"
              :disabled="isSaving"
              class="flex-1 bg-red-600 hover:bg-red-500 disabled:opacity-40 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition"
            >
              {{ isSaving ? 'Menyimpan...' : 'Simpan' }}
            </button>
            <button
              @click="showDiscountModal = false"
              class="flex-1 bg-white/5 hover:bg-white/10 text-white/60 hover:text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition"
            >
              Batal
            </button>
          </div>

          <button
            v-if="selectedCustomer?.special_discount_percentage != null"
            @click="removeSpecialPrice(selectedCustomer); showDiscountModal = false"
            class="w-full text-[10px] text-white/20 hover:text-red-400 transition text-center uppercase tracking-widest font-bold"
          >
            Cabut diskon khusus → kembali ke {{ defaultDiscount }}%
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useLoyaltyStore } from "@/stores/loyalty";
import { toast } from "vue-sonner";
import apiClient from "@/api/client";

const auth    = useAuthStore();
const loyalty = useLoyaltyStore();
const router  = useRouter();

const showDiscountModal = ref(false);
const selectedCustomer  = ref(null);
const discountInput     = ref(null);
const isSaving          = ref(false);
const defaultDiscount   = ref(0);

// Fetch dari endpoint admin yang return special_discount_percentage + settings
const fetchAdminLoyalData = async () => {
  try {
    const res = await apiClient.get("/orders/loyal-customers/");
    const data = res.data;
    // Response: { settings: { discount_percentage: 20 }, customers: [...] }
    if (data?.customers) {
      loyalty.loyalCustomers  = data.customers;
      defaultDiscount.value   = parseFloat(data.settings?.discount_percentage ?? 0);
    } else if (Array.isArray(data)) {
      loyalty.loyalCustomers = data;
    }
  } catch {
    // fallback ke endpoint publik jika admin endpoint gagal
    loyalty.fetchLoyalCustomers();
  }
};

const loyalCount     = computed(() => loyalty.loyalCustomers.filter(c => c.is_loyal).length);
const discountedCount = computed(() => loyalty.loyalCustomers.filter(c => c.special_discount_percentage != null).length);

const formatPrice = (price) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(price || 0);

const openDiscountModal = (customer) => {
  selectedCustomer.value  = customer;
  discountInput.value     = customer.special_discount_percentage ?? null;
  showDiscountModal.value = true;
};

const saveSpecialPrice = async () => {
  if (discountInput.value === null || discountInput.value === "") {
    toast.error("Masukkan persentase diskon");
    return;
  }
  isSaving.value = true;
  try {
    await apiClient.post(`/orders/give-special-price/${selectedCustomer.value.phone}/`, {
      discount_percentage: discountInput.value,
    });
    toast.success(`Diskon ${discountInput.value}% disimpan untuk ${selectedCustomer.value.phone}`);
    showDiscountModal.value = false;
    fetchAdminLoyalData();
  } catch {
    toast.error("Gagal menyimpan diskon");
  } finally {
    isSaving.value = false;
  }
};

const removeSpecialPrice = async (customer) => {
  try {
    await apiClient.delete(`/orders/give-special-price/${customer.phone}/`);
    toast.success(`Diskon khusus dicabut, kembali ke ${defaultDiscount.value}%`);
    fetchAdminLoyalData();
  } catch {
    toast.error("Gagal mencabut diskon");
  }
};

const refreshData = () => fetchAdminLoyalData();

onMounted(() => {
  if (!auth.user) { router.push("/login"); return; }
  fetchAdminLoyalData();
});
</script>