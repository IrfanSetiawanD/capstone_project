import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
    phone: "",
  }),
  getters: {
    totalPrice: (state) =>
      state.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    totalItems: (state) => state.items.reduce((sum, i) => sum + i.quantity, 0),
  },
  actions: {
    addToCart(menu) {
      const found = this.items.find((i) => i.menu_id === menu.id);
      if (found) {
        found.quantity++;
      } else {
        this.items.push({
          menu_id: menu.id,
          name: menu.name,
          price: menu.price,
          quantity: 1,
        });
      }
    },
    removeFromCart(id) {
      this.items = this.items.filter((i) => i.menu_id !== id);
    },
    clearCart() {
      this.items = [];
      this.phone = "";
    },
  },
});
