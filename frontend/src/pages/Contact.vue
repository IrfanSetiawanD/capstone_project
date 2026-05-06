<template>
  <div class="min-h-screen pt-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <span class="font-caveat text-accent text-2xl mb-4 block">Hubungi Kami</span>
        <h1 class="font-oswald text-5xl md:text-6xl font-bold text-white mb-4" data-testid="contact-title">
          LOKASI & KONTAK
        </h1>
        <p class="text-white/70 text-lg">Kunjungi kami atau hubungi untuk informasi lebih lanjut</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <!-- Left Column - Contact Info -->
        <div class="space-y-6">
          <!-- Alamat -->
          <div class="bg-card/50 p-8 rounded-2xl border border-white/5" data-testid="contact-info-address">
            <div class="flex items-start gap-4">
              <div class="bg-primary/10 p-3 rounded-lg">
                <MapPin class="text-primary" size="24" />
              </div>
              <div>
                <h3 class="font-oswald text-xl font-bold text-white mb-2">ALAMAT</h3>
                <p class="text-white/70 leading-relaxed">
                  Masashimura - Jl. Pintu Air RT.003 RW.03 No.48, RT.003/RW.003<br />
                  Harapan Mulya, Kecamatan Medan Satria<br />
                  Kota Bekasi, Jawa Barat
                </p>
              </div>
            </div>
          </div>

          <!-- Telepon -->
          <div class="bg-card/50 p-8 rounded-2xl border border-white/5" data-testid="contact-info-phone">
            <div class="flex items-start gap-4">
              <div class="bg-accent/10 p-3 rounded-lg">
                <Phone class="text-accent" size="24" />
              </div>
              <div>
                <h3 class="font-oswald text-xl font-bold text-white mb-2">TELEPON</h3>
                <p class="text-white/70">
                  WhatsApp: 
                  <a 
                    href="https://wa.me/6285773615870" 
                    class="text-accent hover:underline"
                  >
                    +62 857-7361-5870
                  </a>
                </p>
              </div>
            </div>
          </div>

          <!-- Jam Buka -->
          <div class="bg-card/50 p-8 rounded-2xl border border-white/5" data-testid="contact-info-hours">
            <div class="flex items-start gap-4">
              <div class="bg-primary/10 p-3 rounded-lg">
                <Clock class="text-primary" size="24" />
              </div>
              <div>
                <h3 class="font-oswald text-xl font-bold text-white mb-2">JAM BUKA</h3>
                <div class="text-white/70 space-y-1">
                  <p>Senin - Sabtu : 11.00 - 22.30</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Email -->
          <div class="bg-card/50 p-8 rounded-2xl border border-white/5" data-testid="contact-info-email">
            <div class="flex items-start gap-4">
              <div class="bg-accent/10 p-3 rounded-lg">
                <Mail class="text-accent" size="24" />
              </div>
              <div>
                <h3 class="font-oswald text-xl font-bold text-white mb-2">EMAIL</h3>
                <p class="text-white/70">
                  <a 
                    href="mailto:masashimura.id@gmail.com" 
                    class="text-accent hover:underline"
                  >
                    masashimura.id@gmail.com
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Map & CTA -->
        <div class="space-y-6">
          <!-- Google Maps -->
          <div class="bg-card/50 p-8 rounded-2xl border border-white/5" data-testid="map-container">
            <h3 class="font-oswald text-2xl font-bold text-white mb-4">PETA LOKASI</h3>
            <div class="aspect-video rounded-lg overflow-hidden border border-white/10">
              <iframe
                :src="locationUrl"
                width="100%"
                height="100%"
                style="border: 0"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                title="Lokasi Masashimura"
              />
            </div>
            <p class="text-white/60 text-sm mt-4">
              Lokasi strategis di depan Pengadilan Negeri Bekasi, mudah diakses dari berbagai arah.
            </p>
          </div>

          <!-- Pesan Online CTA -->
          <div class="bg-gradient-to-br from-primary/20 to-accent/20 p-8 rounded-2xl border border-white/10">
            <h3 class="font-oswald text-2xl font-bold text-white mb-4">PESAN ONLINE</h3>
            <p class="text-white/80 mb-6">
              Ingin memesan sekarang? Lihat menu lengkap kami dan pesan langsung via WhatsApp!
            </p>
            <router-link
              to="/menu"
              class="inline-block bg-primary text-white hover:bg-primary/90 font-oswald uppercase tracking-wider px-6 py-3 rounded-sm shadow-neo-yellow hover:translate-y-[2px] hover:shadow-neo-yellow-hover transition-all"
              data-testid="order-cta"
            >
              Lihat Menu
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { MapPin, Phone, Clock, Mail } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

// URL Google Maps embed
const locationUrl = 'https://www.google.com/maps?q=-6.230906846479352,106.99747205246018&z=17&output=embed'
</script>