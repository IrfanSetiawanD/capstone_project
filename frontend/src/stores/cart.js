// src/stores/cart.js

import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";
import { orderAPI } from "@/api";

export const useCartStore = defineStore("cart", () => {
  const cart = ref(JSON.parse(localStorage.getItem("cart") || "{}"));

  const isLoyal = ref(false);
  const discountPercent = ref(0);

  watch(
    cart,
    (value) => {
      localStorage.setItem("cart", JSON.stringify(value));
    },
    {
      deep: true,
    }
  );

  const addToCart = (menu) => {
    const cartKey = `${menu.id}-${Date.now()}`;

    cart.value[cartKey] = {
      ...menu,
      cartKey,
      quantity: 1,
      notes: "",
    };
  };

  const updateQuantity = (cartKey, delta) => {
    if (!cart.value[cartKey]) return;

    cart.value[cartKey].quantity += delta;

    if (cart.value[cartKey].quantity <= 0) {
      delete cart.value[cartKey];
    }
  };

  const removeFromCart = (cartKey) => {
    delete cart.value[cartKey];
  };

  const clearCart = () => {
    cart.value = {};
    isLoyal.value = false;
    discountPercent.value = 0;
  };

  const checkLoyalty = async (phone) => {
    if (!phone || phone.length < 9) {
      isLoyal.value = false;
      discountPercent.value = 0;
      return;
    }

    try {
      const { data } = await orderAPI.checkLoyalty(phone);

      isLoyal.value = data.is_loyal;
      discountPercent.value = data.discount_percent ?? 0;
    } catch (err) {
      console.error(err);

      isLoyal.value = false;
      discountPercent.value = 0;
    }
  };

  const cartItems = computed(() => Object.values(cart.value));

  const cartItemCount = computed(() =>
    cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
  );

  const subtotal = computed(() =>
    cartItems.value.reduce(
      (sum, item) => sum + Number(item.price) * item.quantity,
      0
    )
  );

  const discountAmount = computed(() => {
    if (!isLoyal.value) return 0;

    return subtotal.value * (discountPercent.value / 100);
  });

  const totalPrice = computed(() => subtotal.value - discountAmount.value);

  const isEmpty = computed(() => cartItems.value.length === 0);

  return {
    cart,

    isLoyal,
    discountPercent,

    cartItems,
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