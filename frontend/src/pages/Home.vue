<template>
  <div>
    <div
      class="p-5 mb-4 bg-dark text-white rounded-0 shadow-sm"
      style="
        background:
          linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
          url(&quot;https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=1350&q=80&quot;);
        background-size: cover;
        background-position: center;
        min-height: 400px;
        display: flex;
        align-items: center;
      "
    >
      <div class="container py-5 text-center">
        <h1 class="display-3 fw-bold text-warning">MASHASIMURA</h1>
        <p class="fs-4">
          Citarasa Autentik, Harga Warung. Nikmati hidangan terbaik kami
          langsung dari dapur ahli.
        </p>
        <router-link to="/menu" class="btn btn-warning btn-lg px-4 fw-bold"
          >Pesan Sekarang</router-link
        >
      </div>
    </div>

    <div class="container my-5">
      <div class="row text-center">
        <div class="col-md-4">
          <div class="p-3">
            <h2 class="h1">🥬</h2>
            <h4>Bahan Segar</h4>
            <p class="text-muted">
              Kami menggunakan bahan organik dan daging kualitas pilihan setiap
              harinya.
            </p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3">
            <h2 class="h1">👨‍🍳</h2>
            <h4>Chef Berpengalaman</h4>
            <p class="text-muted">
              Dimasak dengan standar kebersihan tinggi dan resep rahasia
              keluarga.
            </p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3">
            <h2 class="h1">🚀</h2>
            <h4>Cepat & Mudah</h4>
            <p class="text-muted">
              Pesan lewat web, ambil di tempat atau kirim via koordinasi
              WhatsApp.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
