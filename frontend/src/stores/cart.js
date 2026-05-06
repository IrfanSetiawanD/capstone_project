// src/stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const cart = ref({})

  const addToCart = (menu) => {
    if (!cart.value[menu.id]) {
      cart.value[menu.id] = { ...menu, quantity: 1 }
    } else {
      cart.value[menu.id].quantity += 1
    }
  }

  const updateQuantity = (menuId, delta) => {
    if (!cart.value[menuId]) return
    cart.value[menuId].quantity += delta

    if (cart.value[menuId].quantity <= 0) {
      removeFromCart(menuId)
    }
  }

  const removeFromCart = (menuId) => {
    delete cart.value[menuId]
  }

  const clearCart = () => {
    cart.value = {}
  }

  const cartItemCount = computed(() => 
    Object.values(cart.value).reduce((sum, item) => sum + item.quantity, 0)
  )

  const totalPrice = computed(() => 
    Object.values(cart.value).reduce((total, item) => 
      total + (item.price * item.quantity), 0
    )
  )

  const isEmpty = computed(() => Object.keys(cart.value).length === 0)

  return {
    cart,
    cartItemCount,
    totalPrice,
    isEmpty,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart
  }
})