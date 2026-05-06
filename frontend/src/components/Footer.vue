<template>
  <footer class="bg-card/50 border-t border-white/5 py-12">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Logo & Deskripsi -->
        <div class="text-center md:text-left">
          <img
            src="@/assets/masashimura-logo.png"
            alt="Logo Masashimura"
            loading="lazy"
            class="w-40 md:w-48 mb-4 mx-auto md:mx-0 select-none"
          />
          <p class="text-muted-foreground text-sm">
            Tempat nongkrong kekinian, cozy, dan terjangkau di Bekasi.
          </p>
        </div>

        <!-- Navigasi -->
        <div>
          <h3 class="font-oswald text-lg mb-4 text-white">NAVIGASI</h3>
          <div class="space-y-2">
            <router-link to="/" class="block text-sm text-muted-foreground hover:text-primary transition-colors">
              Home
            </router-link>
            <router-link to="/Menu" class="block text-sm text-muted-foreground hover:text-primary transition-colors">
              Menu
            </router-link>
            <router-link to="/Contact" class="block text-sm text-muted-foreground hover:text-primary transition-colors">
              Kontak
            </router-link>
          </div>
        </div>

        <!-- Kontak -->
        <div>
          <h3 class="font-oswald text-lg mb-4 text-white">KONTAK</h3>
          <div class="space-y-2 text-sm text-muted-foreground">
            <p>WhatsApp: +62 857-7361-5870</p>
            <p>Depan Pengadilan Negeri Bekasi</p>
            <p>Kota Bekasi, Jawa Barat</p>
          </div>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t border-white/5 text-center text-sm text-muted-foreground">
        <p>&copy; 2026 Masashimura. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Tidak perlu logic khusus untuk sekarang
</script>