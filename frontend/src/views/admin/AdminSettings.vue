<template>
  <div class="max-w-5xl mx-auto p-6 space-y-8 text-white">

    <div>
      <h1 class="font-oswald text-4xl uppercase">
        System Settings
      </h1>

      <p class="text-white/40">
        Konfigurasi Loyalitas Masashimura
      </p>
    </div>

    <div
      class="bg-[#0b0b0b] rounded-2xl border border-white/10 p-8 space-y-8"
    >

      <div class="grid md:grid-cols-2 gap-6">

        <div>
          <label class="label">
            Minimal Order
          </label>

          <input
            v-model.number="settings.min_orders"
            type="number"
            class="input"
          />
        </div>

        <div>
          <label class="label">
            Diskon (%)
          </label>

          <input
            v-model.number="settings.discount_percent"
            type="number"
            class="input"
          />
        </div>

        <div>
          <label class="label">
            Minimal Belanja
          </label>

          <input
            v-model.number="settings.min_spending"
            type="number"
            class="input"
          />
        </div>

        <div>
          <label class="label">
            Periode (Hari)
          </label>

          <input
            v-model.number="settings.period_days"
            type="number"
            class="input"
          />
        </div>

      </div>

    </div>

    <div
      class="bg-[#0b0b0b] rounded-2xl border border-white/10 p-8 space-y-4"
    >

      <label class="label">
        Nomor WhatsApp
      </label>

      <input
        v-model="settings.admin_whatsapp"
        class="input"
      />

      <p class="text-xs text-white/30">
        gunakan format 628xxxxxxxxxx
      </p>

    </div>

    <button
      @click="saveSettings"
      :disabled="loading"
      class="w-full md:w-auto bg-red-600 hover:bg-red-500 transition px-10 py-4 rounded-xl font-bold uppercase"
    >
      {{ loading ? "Menyimpan..." : "Simpan Perubahan" }}
    </button>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { toast } from "vue-sonner";
import apiClient from "@/api/client";

const loading = ref(false);

const settings = ref({
  min_orders: 5,
  min_spending: 100000,
  period_days: 30,
  discount_percent: 10,
  admin_whatsapp: "",
});

const fetchSettings = async () => {
  try {
    const { data } = await apiClient.get(
      "/orders/loyalty-settings/"
    );

    settings.value = {
      ...data,
      admin_whatsapp:
        localStorage.getItem("admin_whatsapp") || "",
    };
  } catch (err) {
    console.error(err);

    toast.error("Gagal memuat konfigurasi");
  }
};

const saveSettings = async () => {
  loading.value = true;

  try {
    await apiClient.put(
      "/orders/loyalty-settings/",
      {
        min_orders: settings.value.min_orders,
        min_spending: settings.value.min_spending,
        period_days: settings.value.period_days,
        discount_percent: settings.value.discount_percent,
      }
    );

    localStorage.setItem(
      "admin_whatsapp",
      settings.value.admin_whatsapp
    );

    toast.success("Konfigurasi berhasil disimpan");
  } catch (err) {
    console.error(err);

    toast.error("Gagal menyimpan konfigurasi");
  } finally {
    loading.value = false;
  }
};

onMounted(fetchSettings);
</script>

<style scoped>

.label{
    display:block;
    margin-bottom:10px;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:.2em;
    color:rgba(255,255,255,.45);
    font-weight:700;
}

.input{
    width:100%;
    background:#151515;
    border:1px solid rgba(255,255,255,.08);
    padding:14px 18px;
    border-radius:14px;
    color:white;
    transition:.2s;
}

.input:focus{
    outline:none;
    border-color:#dc2626;
}

input::-webkit-inner-spin-button,
input::-webkit-outer-spin-button{
    -webkit-appearance:none;
    margin:0;
}

input[type=number]{
    -moz-appearance:textfield;
}

</style>