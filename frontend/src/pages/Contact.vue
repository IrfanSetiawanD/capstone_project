<template>
  <div class="min-h-screen pt-28 pb-32 bg-[#050505] text-white font-inter selection:bg-red-600/30 selection:text-white scroll-smooth">
    <div class="max-w-7xl mx-auto px-4 sm:px-8">
      
      <div class="text-center mb-16 space-y-3 animate-fade-up">
        <span class="text-xs font-bold tracking-[0.3em] text-[#DC2626] uppercase font-mono">// Visit Us</span>
        <h1 class="font-sora text-4xl md:text-5xl font-extrabold uppercase tracking-tight text-white">
          Lokasi & Kontak
        </h1>
        <p class="text-zinc-500 text-xs sm:text-sm max-w-sm mx-auto font-light">
          Kunjungi kedai kami langsung di Bekasi atau hubungi kontak resmi operasional kami.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-12">
        
        <div class="lg:col-span-6 space-y-4">
          
          <div class="bg-[#0F0F0F] border border-white/5 p-6 rounded-xl flex items-start gap-5 transition-colors hover:border-zinc-800">
            <div class="bg-white/5 p-3.5 rounded-lg text-[#DC2626] flex-shrink-0">
              <MapPin size="20" />
            </div>
            <div class="space-y-1.5">
              <h3 class="font-sora text-sm font-bold uppercase tracking-wider text-white">Alamat Kedai</h3>
              <p class="text-zinc-400 text-xs sm:text-sm font-light leading-relaxed">
                Masashimura - Jl. Pintu Air RT.003 RW.03 No.48<br />
                Harapan Mulya, Medan Satria, Kota Bekasi, Jawa Barat
              </p>
              <p class="text-[11px] text-amber-500 font-medium font-sora pt-1">📍 Tepat di depan Pengadilan Negeri Bekasi Kota</p>
            </div>
          </div>

          <div class="bg-[#0F0F0F] border border-white/5 p-6 rounded-xl flex items-start gap-5 transition-colors hover:border-zinc-800">
            <div class="bg-white/5 p-3.5 rounded-lg text-amber-500 flex-shrink-0">
              <Phone size="20" />
            </div>
            <div class="space-y-1.5">
              <h3 class="font-sora text-sm font-bold uppercase tracking-wider text-white">Telepon / WhatsApp</h3>
              <a href="https://wa.me/6285773615870" target="_blank" class="block text-zinc-400 text-xs sm:text-sm font-mono font-bold hover:text-amber-500 transition-colors">
                +62 857-7361-5870
              </a>
            </div>
          </div>

          <div class="bg-[#0F0F0F] border border-white/5 p-6 rounded-xl flex items-start gap-5 transition-colors hover:border-zinc-800">
            <div class="bg-white/5 p-3.5 rounded-lg text-[#DC2626] flex-shrink-0">
              <Clock size="20" />
            </div>
            <div class="space-y-1.5">
              <h3 class="font-sora text-sm font-bold uppercase tracking-wider text-white">Jam Operasional</h3>
              <p class="text-zinc-400 text-xs sm:text-sm font-light">
                Senin - Sabtu : <span class="font-mono text-white">11.00 - 22.30 WIB</span>
              </p>
              <p class="text-[10px] text-zinc-600 font-mono">*Hari Minggu</p>
            </div>
          </div>

          <div class="bg-[#0F0F0F] border border-white/5 p-6 rounded-xl flex items-start gap-5 transition-colors hover:border-zinc-800">
            <div class="bg-white/5 p-3.5 rounded-lg text-amber-500 flex-shrink-0">
              <Mail size="20" />
            </div>
            <div class="space-y-1.5">
              <h3 class="font-sora text-sm font-bold uppercase tracking-wider text-white">Surat Elektronik (Email)</h3>
              <a href="mailto:masashimura.id@gmail.com" class="block text-zinc-400 text-xs sm:text-sm font-mono hover:text-amber-500 transition-colors">
                masashimura.id@gmail.com
              </a>
            </div>
          </div>

        </div>

        <div class="lg:col-span-6 space-y-4">
          
          <div class="bg-[#0F0F0F] border border-white/5 p-6 rounded-xl space-y-4 shadow-xl">
            <h3 class="font-sora text-xs font-bold uppercase tracking-widest text-zinc-400">// Peta Lokasi Interaktif</h3>
            <div class="aspect-video w-full rounded-lg overflow-hidden border border-white/5 bg-zinc-900">
              <iframe
                :src="locationUrl"
                width="100%"
                height="100%"
                style="border: 0"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                class="grayscale opacity-80 hover:grayscale-0 hover:opacity-100 transition-all duration-500"
              />
            </div>
          </div>

          <div class="bg-gradient-to-b from-[#0F0F0F] to-[#050505] border border-white/5 p-6 sm:p-8 rounded-xl space-y-4 flex flex-col justify-between items-center text-center">
            <div class="space-y-1.5">
              <h3 class="font-sora text-base font-bold text-white uppercase tracking-wide">Pesan Online Sekarang</h3>
              <p class="text-zinc-500 text-xs max-w-xs mx-auto font-light leading-relaxed">
                Males keluar rumah? Jelajahi katalog lengkap produk terbaik kami dan pesan langsung lewat integrasi WhatsApp.
              </p>
            </div>
            <router-link
              to="/menu"
              class="w-full sm:w-auto bg-[#DC2626] hover:bg-red-700 text-white font-sora text-xs uppercase tracking-widest px-10 py-4 rounded-lg font-bold transition-all duration-300 text-center shadow-[0_4px_20px_rgba(220,38,38,0.2)]"
            >
              Buka Katalog Menu
            </router-link>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { MapPin, Phone, Clock, Mail } from "lucide-vue-next";
import { ref } from "vue";

// URL Embed Google Maps Resmi yang mengarah ke sekitar wilayah PN Bekasi / Harapan Mulya
const locationUrl = ref("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.2474247843616!2d106.9974506!3d-6.231077499999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e698d4a2a564acb%3A0x5647f35252d3d568!2sMasashimura!5e0!3m2!1sid!2sid!4v1781883172371!5m2!1sid!2sid");
</script>

<style scoped>
/* ⚙️ LIGHTWEIGHT PRESET ANIMATIONS */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>