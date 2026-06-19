<template>
  <div class="min-h-screen pt-20 bg-[#050505]">
    <div class="max-w-7xl mx-auto px-6 md:px-12 py-12">
      <div class="text-center mb-12">
        <span class="font-caveat text-red-500 text-2xl mb-4 block"
          >Hubungi Kami</span
        >
        <h1
          class="font-oswald text-5xl md:text-6xl font-bold text-white mb-4 uppercase"
        >
          Lokasi & Kontak
        </h1>
        <p class="text-white/70 text-lg">
          Kunjungi kami atau hubungi untuk informasi lebih lanjut
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div class="space-y-6">
          <ContactItem icon="MapPin" title="ALAMAT" color="text-red-500">
            <p class="text-white/70 leading-relaxed">
              Masashimura - Jl. Pintu Air RT.003 RW.03 No.48<br />
              Harapan Mulya, Medan Satria<br />
              Kota Bekasi, Jawa Barat
            </p>
          </ContactItem>

          <ContactItem icon="Phone" title="TELEPON" color="text-amber-500">
            <a
              href="https://wa.me/6285773615870"
              class="text-amber-500 hover:underline"
            >
              +62 857-7361-5870
            </a>
          </ContactItem>

          <ContactItem icon="Clock" title="JAM BUKA" color="text-red-500">
            <p class="text-white/70">Senin - Sabtu : 11.00 - 22.30</p>
          </ContactItem>

          <ContactItem icon="Mail" title="EMAIL" color="text-amber-500">
            <a
              href="mailto:masashimura.id@gmail.com"
              class="text-amber-500 hover:underline"
            >
              masashimura.id@gmail.com
            </a>
          </ContactItem>
        </div>

        <div class="space-y-6">
          <div class="bg-[#0a0a0a] p-8 rounded-2xl border border-white/5">
            <h3 class="font-oswald text-2xl font-bold text-white mb-4">
              PETA LOKASI
            </h3>
            <div
              class="aspect-video rounded-lg overflow-hidden border border-white/10"
            >
              <iframe
                :src="locationUrl"
                width="100%"
                height="100%"
                style="border: 0"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              />
            </div>
          </div>

          <div
            class="bg-gradient-to-br from-red-900/20 to-amber-900/20 p-8 rounded-2xl border border-white/10"
          >
            <h3 class="font-oswald text-2xl font-bold text-white mb-4">
              PESAN ONLINE
            </h3>
            <p class="text-white/80 mb-6">
              Ingin memesan sekarang? Lihat menu lengkap kami dan pesan langsung
              via WhatsApp!
            </p>
            <router-link
              to="/menu"
              class="inline-block bg-red-600 hover:bg-red-700 text-white font-oswald uppercase tracking-wider px-8 py-4 rounded transition-all"
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
import { MapPin, Phone, Clock, Mail } from "lucide-vue-next";
import { defineComponent, h } from "vue";

// Reusable Contact Item Component
const ContactItem = defineComponent({
  props: ["icon", "title", "color"],
  setup(props, { slots }) {
    const icons = { MapPin, Phone, Clock, Mail };
    return () =>
      h(
        "div",
        { class: "bg-[#0a0a0a] p-8 rounded-2xl border border-white/5" },
        [
          h("div", { class: "flex items-start gap-4" }, [
            h("div", { class: "bg-white/5 p-3 rounded-lg" }, [
              h(icons[props.icon], { class: props.color, size: 24 }),
            ]),
            h("div", [
              h(
                "h3",
                { class: "font-oswald text-xl font-bold text-white mb-2" },
                props.title,
              ),
              slots.default?.(),
            ]),
          ]),
        ],
      );
  },
});

// Ganti URL ini dengan URL Embed dari Google Maps Anda
const locationUrl =
  "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.3056094595786!2d106.97230000000001!3d-6.223800000000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sMasashimura!5e0!3m2!1sid!2sid!4v1234567890";
</script>
