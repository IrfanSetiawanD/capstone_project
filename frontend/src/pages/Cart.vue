<script setup>
import { useCartStore } from "../stores/cart";
import axios from "axios";

const cartStore = useCartStore();

const checkout = async () => {
  if (!cartStore.phone) {
    alert("Masukkan nomor HP Anda!");
    return;
  }
  if (cartStore.items.length === 0) {
    alert("Keranjang Anda kosong!");
    return;
  }

  try {
    const res = await axios.post("http://127.0.0.1:8000/api/order/", {
      phone: cartStore.phone,
      payment_method: "cash",
      items: cartStore.items,
    });

    alert("Pesanan berhasil dibuat! Anda akan diarahkan ke WhatsApp.");
    cartStore.clearCart();
    window.location.href = res.data.wa_link;
  } catch (error) {
    alert("Terjadi kesalahan saat checkout.");
  }
};
</script>

<template>
  <div class="container mt-5">
    <h2 class="fw-bold mb-4">🛒 Keranjang Belanja</h2>

    <div class="row">
      <div class="col-md-8">
        <div
          v-if="cartStore.items.length === 0"
          class="alert alert-light border p-5 text-center"
        >
          <p class="mb-3">Keranjang masih kosong.</p>
          <router-link to="/menu" class="btn btn-primary"
            >Lihat Menu</router-link
          >
        </div>

        <div
          v-for="item in cartStore.items"
          :key="item.menu_id"
          class="card mb-3 shadow-sm"
        >
          <div
            class="card-body d-flex justify-content-between align-items-center"
          >
            <div>
              <h6 class="mb-0 fw-bold">{{ item.name }}</h6>
              <small class="text-muted"
                >Rp {{ item.price.toLocaleString() }} x
                {{ item.quantity }}</small
              >
            </div>
            <div class="text-end">
              <div class="fw-bold">
                Rp {{ (item.price * item.quantity).toLocaleString() }}
              </div>
              <button
                class="btn btn-sm text-danger"
                @click="cartStore.removeFromCart(item.menu_id)"
              >
                Hapus
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm border-0 bg-light">
          <div class="card-body">
            <h5 class="fw-bold">Ringkasan</h5>
            <hr />
            <div class="d-flex justify-content-between mb-3">
              <span>Total Harga:</span>
              <span class="h4 fw-bold text-primary"
                >Rp {{ cartStore.totalPrice.toLocaleString() }}</span
              >
            </div>

            <label class="form-label small fw-bold text-uppercase"
              >Nomor WhatsApp</label
            >
            <input
              v-model="cartStore.phone"
              type="text"
              class="form-control mb-3"
              placeholder="Contoh: 08123456789"
            />

            <button
              class="btn btn-success w-100 py-2 fw-bold"
              @click="checkout"
              :disabled="cartStore.items.length === 0"
            >
              Checkout via WhatsApp
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
