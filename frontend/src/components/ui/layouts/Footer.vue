<template>
  <footer class="bg-[#0a0a0a] border-t border-white/5 py-12">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="text-center md:text-left">
          <img
            src="@/assets/masashimura-logo.png"
            alt="Logo Masashimura"
            loading="lazy"
            class="w-40 md:w-48 mb-4 mx-auto md:mx-0 select-none"
          />
          <p class="text-gray-400 text-sm leading-relaxed">
            Tempat nongkrong kekinian, cozy, dan terjangkau di Bekasi.
          </p>
        </div>

        <div>
          <h3
            class="font-oswald text-lg mb-4 text-white uppercase tracking-wider"
          >
            Navigasi
          </h3>
          <div class="space-y-2">
            <router-link
              to="/"
              class="block text-sm text-gray-400 hover:text-red-500 transition-colors"
              >Home</router-link
            >
            <router-link
              to="/menu"
              class="block text-sm text-gray-400 hover:text-red-500 transition-colors"
              >Menu</router-link
            >
            <router-link
              to="/contact"
              class="block text-sm text-gray-400 hover:text-red-500 transition-colors"
              >Kontak</router-link
            >
          </div>
        </div>

        <div>
          <h3
            class="font-oswald text-lg mb-4 text-white uppercase tracking-wider"
          >
            Kontak
          </h3>
          <div class="space-y-2 text-sm text-gray-400">
            <a
              href="https://wa.me/6285773615870"
              target="_blank"
              rel="noopener noreferrer"
              class="block hover:text-emerald-500 transition-colors"
            >
              WhatsApp: +62 857-7361-5870
            </a>
            <p>Depan Pengadilan Negeri Bekasi</p>
            <p>Kota Bekasi, Jawa Barat</p>
          </div>
        </div>
      </div>

      <div
        class="mt-12 pt-8 border-t border-white/5 text-center text-sm text-gray-600"
      >
        <p>
          &copy; {{ new Date().getFullYear() }} Masashimura. All rights
          reserved.
        </p>
      </div>
    </div>
  </footer>
</template>
