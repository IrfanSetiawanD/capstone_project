<template>
  <div class="w-full">
    <div class="max-w-7xl mx-auto">
      <div
        class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6"
      >
        <div>
          <h1
            class="font-oswald text-5xl uppercase italic tracking-tighter text-red-600"
          >
            Loyal Customers
          </h1>
          <p class="text-white/40 text-sm font-light mt-1">
            Pelanggan setia • Minimal 10 pesanan & Rp 100.000 dalam 1 bulan
          </p>
        </div>

        <button
          @click="refreshData"
          class="px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl flex items-center gap-2 text-sm transition-all text-white font-oswald uppercase tracking-widest text-xs"
        >
          <span>🔄</span> Refresh Data
        </button>
      </div>

      <div
        v-if="loyalty.loading"
        class="text-center py-20 bg-[#0a0a0a] border border-white/5 rounded-2xl"
      >
        <div
          class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-red-500 mb-4"
        ></div>
        <p class="text-white/40 font-oswald uppercase tracking-widest text-xs">
          Mengambil data dari Django...
        </p>
      </div>

      <div
        v-else
        class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden shadow-xl"
      >
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead
              class="bg-white/[0.02] border-b border-white/5 text-[10px] uppercase font-oswald tracking-[0.2em] text-white/30"
            >
              <tr>
                <th class="px-8 py-6">Nomor Telepon</th>
                <th class="px-8 py-6">Periode</th>
                <th class="px-8 py-6 text-center">Jumlah Pesanan</th>
                <th class="px-8 py-6 text-right">Total Belanja</th>
                <th class="px-8 py-6 text-center">Status</th>
                <th class="px-8 py-6 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr
                v-for="customer in loyalty.loyalCustomers"
                :key="customer.phone"
                class="hover:bg-white/[0.01] transition-colors"
              >
                <td
                  class="px-8 py-5 font-bold font-oswald tracking-wider text-white"
                >
                  {{ customer.phone }}
                </td>
                <td class="px-8 py-5 text-white/40 text-sm">
                  {{ customer.month || "-" }}
                </td>
                <td class="px-8 py-5 text-center">
                  <span class="text-xl font-bold text-white">{{
                    customer.order_count || 0
                  }}</span>
                </td>
                <td
                  class="px-8 py-5 text-right font-bold text-lg text-amber-500 font-oswald"
                >
                  {{ formatPrice(customer.total_spent) }}
                </td>
                <td class="px-8 py-5 text-center">
                  <span
                    :class="
                      customer.is_loyal
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                    "
                    class="inline-block px-5 py-1.5 text-xs rounded-full font-bold uppercase tracking-widest"
                  >
                    {{ customer.is_loyal ? "LOYAL MEMBER" : "REGULAR" }}
                  </span>
                </td>
                <td class="px-8 py-5 text-center">
                  <button
                    @click="openDiscountModal(customer)"
                    :disabled="!customer.is_loyal"
                    class="px-6 py-2.5 text-xs font-bold uppercase tracking-widest rounded-xl transition-all font-oswald bg-red-600 hover:bg-red-500 text-white disabled:bg-white/5 disabled:text-white/30"
                  >
                    Beri Harga Khusus
                  </button>
                </td>
              </tr>

              <tr v-if="loyalty.loyalCustomers.length === 0">
                <td colspan="6" class="px-8 py-24 text-center text-white/30">
                  <p class="text-lg">Belum ada pelanggan loyal</p>
                  <p class="text-sm mt-2">
                    Data akan muncul setelah ada transaksi yang memenuhi syarat
                  </p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="showDiscountModal"
  class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
  <div class="bg-[#0f0f0f] border border-white/10 rounded-2xl p-6 w-full max-w-sm space-y-5">
    <h3 class="font-oswald text-lg uppercase tracking-wide text-white">
      Beri Harga Khusus
    </h3>
    <p class="text-xs text-white/40">{{ selectedCustomer?.phone }}</p>

    <div class="space-y-1">
      <label class="text-[10px] uppercase font-bold tracking-widest text-white/40">
        Persentase Diskon (%)
      </label>
      <input
        v-model.number="discountInput"
        type="number"
        min="0"
        max="100"
        class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-red-600 transition"
        placeholder="Contoh: 15"
      />
    </div>

    <div class="flex gap-3">
      <button @click="saveSpecialPrice" :disabled="isSaving"
        class="flex-1 bg-red-600 hover:bg-red-500 disabled:opacity-40 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition">
        {{ isSaving ? 'Menyimpan...' : 'Simpan' }}
      </button>
      <button @click="showDiscountModal = false"
        class="flex-1 bg-white/5 hover:bg-white/10 text-white font-bold py-3 rounded-xl text-xs uppercase tracking-wider transition">
        Batal
      </button>
    </div>

    <!-- Cabut harga khusus jika sudah ada -->
    <button v-if="selectedCustomer?.special_discount_percentage != null"
      @click="removeSpecialPrice(selectedCustomer); showDiscountModal = false"
      class="w-full text-xs text-red-400 hover:text-red-300 transition text-center">
      Cabut harga khusus
    </button>
  </div>
</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useLoyaltyStore } from "@/stores/loyalty";
import { toast } from "vue-sonner";
import apiClient from "@/api/client";

const auth    = useAuthStore();
const loyalty = useLoyaltyStore();
const router  = useRouter();

// State modal diskon
const showDiscountModal = ref(false);
const selectedCustomer  = ref(null);
const discountInput     = ref(null);
const isSaving          = ref(false);

const formatPrice = (price) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(price || 0);

// FIX: sebelumnya template memanggil "giveSpecialPrice" tapi fungsi
// yang didefinisikan bernama "openDiscountModal" — tombol jadi
// ReferenceError saat diklik dan modal tidak pernah terbuka.
// Sekarang nama di template & script sudah konsisten.
const openDiscountModal = (customer) => {
  selectedCustomer.value  = customer;
  discountInput.value     = customer.special_discount_percentage ?? null;
  showDiscountModal.value = true;
};

const saveSpecialPrice = async () => {
  if (!discountInput.value && discountInput.value !== 0) {
    toast.error("Masukkan persentase diskon");
    return;
  }
  isSaving.value = true;
  try {
    await apiClient.post(`/orders/give-special-price/${selectedCustomer.value.phone}/`, {
      discount_percentage: discountInput.value,
    });
    toast.success(`Harga khusus ${discountInput.value}% disimpan untuk ${selectedCustomer.value.phone}`);
    showDiscountModal.value = false;
    loyalty.fetchLoyalCustomers();
  } catch {
    toast.error("Gagal menyimpan harga khusus");
  } finally {
    isSaving.value = false;
  }
};

const removeSpecialPrice = async (customer) => {
  try {
    await apiClient.delete(`/orders/give-special-price/${customer.phone}/`);
    toast.success("Harga khusus dicabut");
    loyalty.fetchLoyalCustomers();
  } catch {
    toast.error("Gagal mencabut harga khusus");
  }
};

const refreshData = () => loyalty.fetchLoyalCustomers();

onMounted(() => {
  if (!auth.user) { router.push("/login"); return; }
  loyalty.fetchLoyalCustomers();
});
</script>