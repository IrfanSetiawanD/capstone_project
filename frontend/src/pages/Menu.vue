<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useCartStore } from "../stores/cart";
import { useToast } from "vue-toastification";

const cartStore = useCartStore();
const toast = useToast();

const menus = ref([]);
const loading = ref(true);
const filter = ref("Semua");

const getMenus = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/menus/");
    menus.value = res.data;
  } catch (error) {
    toast.error("Gagal memuat menu");
  } finally {
    loading.value = false;
  }
};

// Fungsi Tambah dengan Feedback
const addToCart = (menu) => {
  cartStore.addToCart(menu);
  toast.success(`${menu.name} ditambah ke keranjang!`, {
    timeout: 2000,
    position: "bottom-right",
  });
};

// Logika Pengelompokan Kategori
const categories = computed(() => {
  const cats = menus.value.map((m) => m.category);
  return ["Semua", ...new Set(cats)];
});

const filteredMenus = computed(() => {
  if (filter.value === "Semua") return menus.value;
  return menus.value.filter((m) => m.category === filter.value);
});

onMounted(() => {
  getMenus();
});
</script>

<template>
  <div class="container mt-4">
    <h2 class="fw-bold mb-4">Daftar Menu</h2>

    <div class="mb-4 d-flex gap-2 overflow-auto pb-2">
      <button
        v-for="cat in categories"
        :key="cat"
        class="btn btn-sm rounded-pill px-3"
        :class="filter === cat ? 'btn-warning fw-bold' : 'btn-outline-dark'"
        @click="filter = cat"
      >
        {{ cat }}
      </button>
    </div>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-warning"></div>
    </div>

    <div class="row" v-else>
      <div
        v-for="menu in filteredMenus"
        :key="menu.id"
        class="col-md-4 col-6 mb-4"
      >
        <div class="card h-100 shadow-sm border-0 position-relative">
          <div class="card-body">
            <span class="badge bg-light text-dark mb-2 border">{{
              menu.category
            }}</span>
            <h5 class="card-title fw-bold text-truncate">{{ menu.name }}</h5>
            <p class="text-primary fw-bold mb-3">
              Rp {{ menu.price.toLocaleString() }}
            </p>

            <button
              class="btn btn-warning w-100 fw-bold"
              @click="addToCart(menu)"
              :disabled="menu.stock <= 0"
            >
              {{ menu.stock > 0 ? "+ Tambah" : "Habis" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
