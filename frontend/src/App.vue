<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow sticky-top">
    <div class="container">
      <router-link class="navbar-brand fw-bold text-warning" to="/"
        >🍜 MASHASIMURA</router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/menu">Daftar Menu</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/contact">Lokasi</router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link btn btn-outline-warning ms-lg-2 px-3"
              to="/cart"
            >
              🛒 {{ cartStore.totalItems }} Item
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-info ms-lg-3" to="/dashboard"
              >📊 Owner AI</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup>
import { useCartStore } from "./stores/cart";
const cartStore = useCartStore();
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
