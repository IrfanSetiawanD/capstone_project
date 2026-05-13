<template>
  <div class="min-h-screen">
    <section class="relative h-screen flex items-center justify-center overflow-hidden" data-testid="hero-section">
      <div
        class="absolute inset-0 bg-cover bg-center"
        :style="{ backgroundImage: `url(${heroImage})` }"
      />
      <div class="absolute inset-0 bg-gradient-to-b from-background/30 to-background" />
      <div class="absolute inset-0 bg-noise" />

      <div class="relative z-10 text-center px-6 max-w-4xl mx-auto">
        <div class="mb-6 inline-block"></div>
        <h1 class="font-oswald font-bold mb-6 tracking-tight" data-testid="hero-title">
          <span class="text-white block text-3xl md:text-4xl mb-2">
            WELCOME TO
          </span>

          <img
            src="@/assets/masashimura-logo.png"
            alt="Masashimura"
            class="w-[18rem] md:w-[26rem] lg:w-[32rem] mx-auto select-none"
          />
        </h1>
        <p class="text-lg md:text-xl text-white/80 mb-8 leading-relaxed max-w-2xl mx-auto" data-testid="hero-description">
          Tempat nongkrong kekinian yang cozy dan terjangkau untuk pelajar, mahasiswa, dan pekerja di Bekasi
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/menu"
            class="bg-primary text-white hover:bg-primary/90 font-oswald uppercase tracking-wider px-8 py-4 rounded-sm shadow-neo-yellow hover:translate-y-[2px] hover:shadow-neo-yellow-hover transition-all text-center"
            data-testid="hero-cta-menu"
          >
            Lihat Menu
          </router-link>
          <router-link
            to="/contact"
            class="bg-transparent border border-white/20 text-white hover:bg-white/5 font-oswald uppercase tracking-wider px-8 py-4 rounded-sm transition-all text-center"
            data-testid="hero-cta-contact"
          >
            Kontak Kami
          </router-link>
        </div>
      </div>
    </section>

    <section class="py-24 md:py-32 px-6 md:px-12" data-testid="about-section">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <span class="font-caveat text-accent text-2xl mb-4 block">Tentang Kami</span>
            <h2 class="font-oswald text-4xl md:text-5xl font-bold mb-6 text-white" data-testid="about-title">
              PREMIUM TAPI TERJANGKAU
            </h2>
            <p class="text-white/70 leading-relaxed mb-4" data-testid="about-description">
              Masashimura adalah tempat nongkrong yang menggabungkan konsep premium dengan harga yang ramah di kantong.
              Berlokasi strategis di depan Pengadilan Negeri Bekasi, kami hadir untuk melayani pelajar, mahasiswa,
              pekerja pengadilan, dan pengunjung sidang.
            </p>
            <p class="text-white/70 leading-relaxed mb-6">
              Nama "Masashimura" sendiri bermakna "masa si murah" - sebuah tempat yang terlihat dan terasa premium
              namut tetap terjangkau untuk semua kalangan.
            </p>
            <router-link
              to="/menu"
              class="inline-block bg-primary text-white hover:bg-primary/90 font-oswald uppercase tracking-wider px-6 py-3 rounded-sm shadow-neo-yellow hover:translate-y-[2px] hover:shadow-neo-yellow-hover transition-all text-center"
              data-testid="about-cta"
            >
              Jelajahi Menu
            </router-link>
          </div>
          <div class="relative">
            <div class="aspect-square rounded-2xl overflow-hidden border border-white/10">
              <img :src="aboutImage" alt="Masashimura Ambiance" class="w-full h-full object-cover" />
            </div>
            <div class="absolute -bottom-6 -right-6 bg-accent text-black p-6 rounded-xl shadow-lg">
              <p class="font-oswald text-3xl font-bold">100+</p>
              <p class="text-sm">Pelanggan Puas</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-24 md:py-32 px-6 md:px-12 bg-card/30" data-testid="features-section">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <span class="font-caveat text-accent text-2xl mb-4 block">Kenapa Memilih Kami</span>
          <h2 class="font-oswald text-4xl md:text-5xl font-bold text-white" data-testid="features-title">
            KEUNGGULAN MASASHIMURA
          </h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="bg-secondary/30 p-8 rounded-2xl border border-white/5 hover:bg-secondary/50 transition-colors group"
            :data-testid="`feature-card-${index}`"
          >
            <div class="mb-4 group-hover:scale-110 transition-transform">
              <component :is="feature.icon" class="w-8 h-8 text-accent" />
            </div>
            <h3 class="font-oswald text-xl font-bold mb-3 text-white">{{ feature.title }}</h3>
            <p class="text-white/70 text-sm leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="py-24 md:py-32 px-6 md:px-12" data-testid="cta-section">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="font-oswald text-4xl md:text-5xl font-bold mb-6 text-white">
          SIAP UNTUK NONGKRONG?
        </h2>
        <p class="text-white/70 text-lg mb-8">
          Lihat menu lengkap kami dan pesan sekarang juga via WhatsApp!
        </p>
        <router-link
          to="/menu"
          class="inline-block bg-primary text-white hover:bg-primary/90 font-oswald uppercase tracking-wider px-8 py-4 rounded-sm shadow-neo-yellow hover:translate-y-[2px] hover:shadow-neo-yellow-hover transition-all text-center"
          data-testid="cta-button"
        >
          Pesan Sekarang
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { MapPin, Clock, Phone } from 'lucide-vue-next'

  const heroImage = 'https://images.unsplash.com/photo-1759922221495-78755ac90d70?crop=entropy&cs=srgb&fm=jpg&q=85';
  const aboutImage = 'https://images.unsplash.com/photo-1762086931964-373bceb5a690?crop=entropy&cs=srgb&fm=jpg&q=85';

const features = [
  {
    icon: MapPin,
    title: 'Lokasi Strategis',
    description: 'Tepat di depan Pengadilan Negeri Bekasi, mudah dijangkau',
  },
  {
    icon: Clock,
    title: 'Buka Senin - Sabtu',
    description: 'Siap melayani Anda dari pagi hingga malam',
  },
  {
    icon: Phone,
    title: 'Pesan Online',
    description: 'Order mudah via WhatsApp langsung dari website',
  },
]
</script>