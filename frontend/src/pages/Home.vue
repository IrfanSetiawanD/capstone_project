<template>
  <div class="min-h-screen bg-[#050505]">
    <section
      class="relative h-screen flex items-center justify-center overflow-hidden"
      data-testid="hero-section"
    >
      <div
        class="absolute inset-0 bg-cover bg-center"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div
        class="absolute inset-0 bg-gradient-to-b from-background/40 to-background"
      />

      <div class="relative z-10 text-center px-6 max-w-4xl mx-auto">
        <h1
          class="font-oswald font-bold mb-6 tracking-tight"
          data-testid="hero-title"
        >
          <span
            class="text-white block text-2xl md:text-3xl mb-2 tracking-[0.2em] uppercase"
            >Welcome to</span
          >
          <img
            src="@/assets/masashimura-logo.png"
            alt="Masashimura Logo"
            class="w-[18rem] md:w-[28rem] lg:w-[32rem] mx-auto select-none"
          />
        </h1>
        <p
          class="text-lg md:text-xl text-white/80 mb-8 leading-relaxed max-w-2xl mx-auto"
          data-testid="hero-description"
        >
          Tempat nongkrong kekinian yang cozy dan terjangkau untuk pelajar,
          mahasiswa, dan pekerja di Bekasi.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/menu"
            class="bg-red-600 text-white hover:bg-red-700 font-oswald uppercase tracking-wider px-8 py-4 rounded transition-all text-center"
          >
            Lihat Menu
          </router-link>
          <router-link
            to="/contact"
            class="bg-transparent border border-white/20 text-white hover:bg-white/10 font-oswald uppercase tracking-wider px-8 py-4 rounded transition-all text-center"
          >
            Kontak Kami
          </router-link>
        </div>
      </div>
    </section>

    <section class="py-24 px-6 md:px-12" data-testid="about-section">
      <div
        class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center"
      >
        <div>
          <span class="font-caveat text-amber-500 text-2xl mb-4 block"
            >Tentang Kami</span
          >
          <h2
            class="font-oswald text-4xl md:text-5xl font-bold mb-6 text-white uppercase"
          >
            Premium tapi Terjangkau
          </h2>
          <p class="text-white/70 leading-relaxed mb-4">
            Masashimura adalah tempat nongkrong yang menggabungkan konsep
            premium dengan harga yang ramah di kantong. Berlokasi strategis di
            depan Pengadilan Negeri Bekasi, kami hadir untuk melayani pelajar,
            mahasiswa, pekerja pengadilan, dan pengunjung sidang.
          </p>
          <p class="text-white/70 leading-relaxed mb-6">
            Nama "Masashimura" sendiri bermakna "masa si murah" - sebuah tempat
            yang terasa premium namun tetap terjangkau.
          </p>
          <router-link
            to="/menu"
            class="text-red-500 font-oswald uppercase tracking-widest hover:underline"
          >
            Jelajahi Menu &rarr;
          </router-link>
        </div>
        <div class="relative">
          <div
            class="aspect-square rounded-2xl overflow-hidden border border-white/10"
          >
            <img
              :src="aboutImage"
              alt="Suasana Masashimura"
              class="w-full h-full object-cover"
            />
          </div>
          <div
            class="absolute -bottom-6 -right-6 bg-amber-500 text-black p-6 rounded-xl shadow-lg"
          >
            <p class="font-oswald text-3xl font-bold">100+</p>
            <p class="text-sm font-semibold">Pelanggan Puas</p>
          </div>
        </div>
      </div>
    </section>

    <section class="py-24 px-6 bg-[#0a0a0a]" data-testid="features-section">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="bg-[#111] p-8 rounded-2xl border border-white/5 hover:border-red-900 transition-colors"
          >
            <component :is="feature.icon" class="w-8 h-8 text-red-500 mb-4" />
            <h3 class="font-oswald text-xl font-bold mb-2 text-white">
              {{ feature.title }}
            </h3>
            <p class="text-white/60 text-sm">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { MapPin, Clock, Phone } from "lucide-vue-next";

const heroImage =
  "https://images.unsplash.com/photo-1759922221495-78755ac90d70?q=80&w=2070";
const aboutImage =
  "https://images.unsplash.com/photo-1762086931964-373bceb5a690?q=80&w=2070";

const features = [
  {
    icon: MapPin,
    title: "Lokasi Strategis",
    description: "Tepat di depan Pengadilan Negeri Bekasi.",
  },
  {
    icon: Clock,
    title: "Buka Senin - Sabtu",
    description: "Siap melayani dari pukul 11.00 - 22.30.",
  },
  {
    icon: Phone,
    title: "Pesan Online",
    description: "Order mudah via WhatsApp langsung.",
  },
];
</script>
