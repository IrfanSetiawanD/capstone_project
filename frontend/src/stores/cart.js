// src/stores/cart.js
import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";
import axios from "axios";

export const useCartStore = defineStore("cart", () => {
  // --- STATE ---
  const cart = ref(JSON.parse(localStorage.getItem("cart") || "{}"));
  const isLoyal = ref(false);
  const discountPercent = ref(0);

  // --- PERSISTENCE ---
  watch(
    cart,
    (newCart) => {
      localStorage.setItem("cart", JSON.stringify(newCart));
    },
    { deep: true },
  );

  // --- ACTIONS ---
  const addToCart = (menu) => {
    if (!cart.value[menu.id]) {
      cart.value[menu.id] = { ...menu, quantity: 1 };
    } else {
      cart.value[menu.id].quantity += 1;
    }
  };

  const updateQuantity = (menuId, delta) => {
    if (!cart.value[menuId]) return;
    cart.value[menuId].quantity += delta;
    if (cart.value[menuId].quantity <= 0) {
      removeFromCart(menuId);
    }
  };

  const removeFromCart = (menuId) => {
    delete cart.value[menuId];
  };

  const clearCart = () => {
    cart.value = {};
    isLoyal.value = false;
    discountPercent.value = 0;
  };

  // Fungsi untuk memanggil API Django yang baru kita buat
  const checkLoyalty = async (phone) => {
    try {
      const response = await axios.get(`/api/orders/check-loyalty/`, {
        params: { phone },
      });
      isLoyal.value = response.data.is_loyal;
      discountPercent.value = response.data.discount_percent;
    } catch (error) {
      console.error("Gagal mengecek status loyalitas:", error);
      isLoyal.value = false;
      discountPercent.value = 0;
    }
  };

  // --- GETTERS ---
  const cartItemCount = computed(() =>
    Object.values(cart.value).reduce((sum, item) => sum + item.quantity, 0),
  );

  const subtotal = computed(() =>
    Object.values(cart.value).reduce(
      (total, item) => total + Number(item.price) * item.quantity,
      0,
    ),
  );

  // Menghitung potongan harga
  const discountAmount = computed(() =>
    isLoyal.value ? (subtotal.value * discountPercent.value) / 100 : 0,
  );

  // Menghitung harga akhir setelah diskon
  const totalPrice = computed(() => subtotal.value - discountAmount.value);

  const isEmpty = computed(() => Object.keys(cart.value).length === 0);

  return {
    cart,
    isLoyal,
    discountPercent,
    cartItemCount,
    subtotal,
    discountAmount,
    totalPrice,
    isEmpty,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    checkLoyalty,
  };
});
