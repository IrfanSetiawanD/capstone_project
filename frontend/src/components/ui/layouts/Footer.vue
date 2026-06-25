<template>
  <footer class="bg-[#0a0a0a] border-t border-white/5 py-12 text-white font-inter">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
        
        <div class="text-center md:text-left space-y-3">
          <img
            src="@/assets/masashimura-logo.png"
            alt="Logo Masashimura"
            loading="lazy"
            class="w-40 md:w-48 mx-auto md:mx-0 select-none pointer-events-none"
          />
          <p class="text-zinc-400 text-sm leading-relaxed max-w-sm">
            Tempat nongkrong kekinian, cozy, dan terjangkau di Bekasi. Nikmati varian menu jepang kustom terbaik.
          </p>
        </div>

        <div class="text-center md:text-left space-y-6">
          <div>
            <h3 class="font-oswald text-lg mb-4 text-white uppercase tracking-wider font-bold">
              Navigasi
            </h3>
            <div class="space-y-2">
              <router-link
                to="/"
                class="block text-sm text-zinc-400 hover:text-red-500 transition-colors"
              >Home</router-link>
              <router-link
                to="/menu"
                class="block text-sm text-zinc-400 hover:text-red-500 transition-colors"
              >Menu</router-link>
              <router-link
                to="/contact"
                class="block text-sm text-zinc-400 hover:text-red-500 transition-colors"
              >Kontak</router-link>
            </div>
          </div>

          <div>
            <h4 class="text-xs uppercase tracking-[0.15em] text-zinc-500 font-bold mb-3">Ikuti Kami</h4>
            <div class="flex items-center justify-center md:justify-start gap-4">
              <a 
                href="https://instagram.com/masashimura" 
                target="_blank" 
                rel="noopener noreferrer"
                class="w-9 h-9 bg-white/5 rounded-xl border border-white/5 flex items-center justify-center text-zinc-400 hover:text-red-500 hover:bg-white/10 transition-all shadow-md group"
                aria-label="Instagram Masashimura"
              >
                <Instagram size="16" />
              </a>
              <a 
                href="https://tiktok.com/@masashimura" 
                target="_blank" 
                rel="noopener noreferrer"
                class="w-9 h-9 bg-white/5 rounded-xl border border-white/5 flex items-center justify-center text-zinc-400 hover:text-red-500 hover:bg-white/10 transition-all shadow-md group"
                aria-label="TikTok Masashimura"
              >
                <Music4 size="16" />
              </a>
            </div>
          </div>
        </div>

        <div class="text-center md:text-left">
          <h3 class="font-oswald text-lg mb-4 text-white uppercase tracking-wider font-bold">
            Kontak Resmi
          </h3>
          <div class="space-y-3 text-sm text-zinc-400">
            <a
              href="mailto:management@masashimura.com"
              class="block hover:text-red-500 transition-colors font-mono tracking-tight"
            >
              ✉️ masashimura.id@gmail.com
            </a>
            <div class="pt-2 space-y-1">
              <p class="text-white font-medium">📍 Lokasi Kedai:</p>
              <p class="text-zinc-500 leading-relaxed text-xs">
                Depan Pengadilan Negeri Bekasi,<br />
                Kota Bekasi, Jawa Barat, Indonesia
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-12 pt-8 border-t border-white/5 text-center text-xs text-zinc-600 tracking-wider">
        <p>
          &copy; {{ currentYear }} Masashimura. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from "vue";
import { Instagram, Music4 } from "lucide-vue-next";

// Mencegah re-render tahun secara dinamis saat navigasi berubah
const currentYear = computed(() => new Date().getFullYear());
</script>