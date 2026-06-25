<template>
  <div class="min-h-screen bg-[#050505] text-white font-inter overflow-x-hidden selection:bg-red-600/30 selection:text-white scroll-smooth">
    
    <!-- ⏳ LOADING STATE MINIMALIS -->
    <div v-if="isLoading" class="h-screen w-screen flex flex-col justify-center items-center bg-[#050505] text-zinc-500 font-mono text-xs tracking-widest uppercase">
      <div class="animate-spin w-5 h-5 border-2 border-[#DC2626] border-t-transparent rounded-full mb-3"></div>
      Loading Content...
    </div>

    <template v-else>
      <!-- 🛒 1. HERO SECTION (100vh) -->
      <section class="relative h-screen flex items-center justify-center px-4 sm:px-8 overflow-hidden">
        <!-- Parallax Latar Belakang -->
        <div class="absolute inset-0 bg-cover bg-center opacity-15 scale-105 pointer-events-none transform translate-y-[var(--scroll-offset)] transition-transform duration-100" :style="{ backgroundImage: `url(${cms.hero_food_image || defaultHeroFood})` }" />
        <div class="absolute inset-0 bg-gradient-to-t from-[#050505] via-transparent to-transparent" />

        <div class="relative z-10 max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center h-full pt-16">
          <!-- Teks Kiri -->
          <div class="lg:col-span-7 space-y-6 text-center lg:text-left animate-fade-up">
            <h1 class="font-sora text-4xl sm:text-6xl font-extrabold tracking-tight uppercase leading-none text-white whitespace-pre-line">
              {{ cms.hero_headline }}
            </h1>
            <p class="text-sm sm:text-base text-zinc-400 max-w-md mx-auto lg:mx-0 font-light leading-relaxed">
              {{ cms.hero_subheadline }}
            </p>
            <div class="pt-4 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <router-link to="/menu" class="bg-[#DC2626] hover:bg-red-700 text-white font-sora text-xs uppercase tracking-widest px-8 py-4 rounded-lg font-bold transition-all duration-300 transform hover:-translate-y-0.5 text-center">
                Lihat Menu
              </router-link>
              <router-link to="/contact" class="bg-transparent border border-white/10 hover:bg-white/5 text-white font-sora text-xs uppercase tracking-widest px-8 py-4 rounded-lg font-bold transition-all duration-300 text-center">
                Kontak Kami
              </router-link>
            </div>
          </div>

          <!-- Foto Makanan Besar Kanan -->
          <div class="lg:col-span-5 flex justify-center lg:justify-end animate-fade-in">
            <div class="relative w-full max-w-sm aspect-square bg-[#0F0F0F] border border-white/5 rounded-2xl overflow-hidden shadow-2xl">
              <img :src="cms.hero_food_image || defaultHeroFood" alt="Hero Food CDN" class="w-full h-full object-cover pointer-events-none" />
            </div>
          </div>
        </div>
      </section>

      <!-- 🕶️ 2. MARQUEE TEXT ACCENT -->
      <section class="py-6 bg-[#0F0F0F] border-y border-white/5 overflow-hidden flex items-center pointer-events-none">
        <div class="whitespace-nowrap flex gap-8 animate-marquee text-zinc-600 font-sora text-xs font-bold tracking-[0.2em] uppercase opacity-40">
          <span v-for="n in 4" :key="n">
            {{ cms.marquee_text }} &nbsp;&nbsp;&nbsp;&nbsp;
          </span>
        </div>
      </section>

      <!-- 🔥 3. BEST SELLER SECTION -->
      <section class="py-[120px] px-4 max-w-7xl mx-auto space-y-16">
        <div class="text-center space-y-2">
          <h2 class="font-sora text-2xl sm:text-3xl font-extrabold uppercase tracking-tight">Menu Terlaris 🔥</h2>
          <p class="text-xs text-zinc-500 max-w-xs mx-auto">Varian paling favorit yang sering dipesan squad tongkrongan.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="(item, idx) in bestSellers" :key="idx" class="bg-[#0F0F0F] border border-white/5 rounded-xl overflow-hidden group hover:border-zinc-800 transition-all duration-300 hover:scale-[1.03] hover:shadow-[0_10px_30px_rgba(0,0,0,0.5)]">
            <div class="relative aspect-[16/10] overflow-hidden bg-zinc-900">
              <img :src="item.image" :alt="item.name" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            </div>
            <div class="p-6 space-y-4">
              <h3 class="font-sora text-base font-bold uppercase text-white">{{ item.name }}</h3>
              <p class="text-zinc-500 text-xs font-light line-clamp-2 leading-relaxed">{{ item.desc }}</p>
              <div class="flex items-center justify-between pt-2">
                <p class="font-mono text-xs font-bold text-[#DC2626]">Rp {{ item.price.toLocaleString() }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 🏮 4. TENTANG MASASHIMURA -->
      <section class="py-[120px] bg-[#0F0F0F] border-y border-white/5 px-4">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <!-- Left Foto Outlet -->
          <div class="rounded-xl overflow-hidden border border-white/5 aspect-video sm:aspect-square">
            <img :src="cms.about_image || defaultAboutImage" alt="Suasana Masashimura" class="w-full h-full object-cover" />
          </div>
          <!-- Right Teks Deskripsi -->
          <div class="space-y-8">
            <div class="space-y-4">
              <h2 class="font-sora text-2xl sm:text-3xl font-extrabold uppercase tracking-tight text-white">Tentang Masashimura</h2>
              <p class="text-zinc-400 text-xs sm:text-sm font-light leading-relaxed">
                {{ cms.about_text }}
              </p>
            </div>
            
            <!-- Clean Metrics Area -->
            <div class="grid grid-cols-3 gap-6 pt-6 border-t border-white/5 text-center sm:text-left">
              <div>
                <p class="font-sora text-xl sm:text-2xl font-extrabold text-[#DC2626]">{{ cms.metric_1 }}</p>
                <p class="text-[10px] text-zinc-500 uppercase tracking-wider">Berdiri</p>
              </div>
              <div>
                <p class="font-sora text-xl sm:text-2xl font-extrabold text-white">{{ cms.metric_2 }}</p>
                <p class="text-[10px] text-zinc-500 uppercase tracking-wider">Varian Menu</p>
              </div>
              <div>
                <p class="font-sora text-xl sm:text-2xl font-extrabold text-amber-500">{{ cms.metric_3 }}</p>
                <p class="text-[10px] text-zinc-500 uppercase tracking-wider">Rating Toko</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 🧱 5. THE MASASHIMURA CORE (Dinamis Auto-Layout Bento Grid) -->
      <section class="py-[120px] px-4 max-w-7xl mx-auto space-y-16">
        <div class="text-center space-y-2">
          <h2 class="font-sora text-2xl sm:text-3xl font-extrabold uppercase tracking-tight">Sistem Core Kenyamanan 🧱</h2>
          <p class="text-xs text-zinc-500 max-w-xs mx-auto">Fasilitas dasar operasional harian yang lo dapetin di kedai.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 grid-flow-row-dense gap-4 max-w-4xl mx-auto text-sm font-sora font-bold uppercase">
          <div 
            v-for="(bento, index) in bentoFacilities" 
            :key="index"
            :class="[
              bento.size === 'large' ? 'md:col-span-2 md:row-span-2 p-8 min-h-[280px]' : 'p-6 min-h-[132px]',
              'bg-[#0F0F0F] border border-white/5 rounded-xl flex flex-col justify-between transition-all duration-300 hover:border-[#DC2626] group'
            ]"
          >
            <!-- Baris Atas / Icon Luar -->
            <div :class="[bento.size === 'large' ? 'text-[#DC2626]' : 'text-[#DC2626] flex justify-end', 'transition-transform duration-300 group-hover:-translate-y-1']">
              <component :is="iconMap[bento.icon_name] || iconMap['Coffee']" :size="bento.size === 'large' ? 24 : 18" />
            </div>

            <!-- Baris Bawah / Teks Fasilitas -->
            <span :class="bento.size === 'large' ? 'tracking-wide text-lg text-white' : 'text-zinc-300'">
              {{ bento.title }}
            </span>
          </div>
        </div>
      </section>

      <!-- 📸 6. GALLERY & EVENT OUTLET (Dinamis Maksimal 6 Foto dengan Title) -->
      <section class="py-[120px] bg-[#0F0F0F] border-y border-white/5 px-4">
        <div class="max-w-7xl mx-auto space-y-16">
          <div class="text-center space-y-1">
            <h2 class="font-sora text-2xl sm:text-3xl font-extrabold uppercase tracking-tight">Gallery MASASHIMURA 📸</h2>
            <p class="text-xs text-zinc-500 max-w-xs mx-auto">Kumpulan dokumentasi keseruan event dan suasana tongkrongan.</p>
          </div>
          
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div v-for="(img, i) in displayedGallery" :key="i" class="relative aspect-square rounded-xl overflow-hidden border border-white/5 bg-zinc-900 group shadow-lg">
              <img :src="img.image_url" :alt="img.title || 'Event Masashimura'" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
              <!-- Hover Overlay Title Text -->
              <div class="absolute inset-0 bg-black/75 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">
                <p class="text-xs font-sora font-bold uppercase tracking-wider text-white">{{ img.title || 'Event Masashimura' }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ⭐ 7. AUTOMATIC REVIEW SLIDER -->
      <section class="py-[120px] px-4 max-w-4xl mx-auto overflow-hidden">
        <div class="text-center space-y-2 mb-12">
          <h2 class="font-sora text-2xl sm:text-3xl font-extrabold uppercase tracking-tight">Review Pelanggan ⭐</h2>
        </div>
        <div class="relative min-h-[140px] flex items-center justify-center">
          <transition-group name="slide-fade" tag="div" class="w-full">
            <div v-for="(review, index) in reviews" v-show="index === currentReviewIndex" :key="index" class="bg-[#0F0F0F] border border-white/5 p-8 rounded-xl space-y-4 text-center mx-auto max-w-2xl">
              <p class="text-zinc-300 text-xs sm:text-sm font-light italic leading-relaxed">"{{ review.text }}"</p>
              <div class="text-xs font-mono">
                <span class="text-white font-bold">{{ review.name }}</span>
                <span class="text-zinc-600"> • {{ review.status }}</span>
              </div>
            </div>
          </transition-group>
        </div>
      </section>

      <!-- 🎯 8. CALL TO ACTION (CTA) -->
      <section class="py-[140px] px-4 bg-[#050505] text-center border-t border-white/5">
        <div class="max-w-xl mx-auto space-y-6">
          <h2 class="font-sora text-3xl sm:text-5xl font-extrabold tracking-tight uppercase">Udah Laper?</h2>
          <p class="text-zinc-500 text-xs sm:text-sm font-light max-w-xs mx-auto">Yuk cobain menu favorit masashimura.</p>
          <div class="pt-4">
            <router-link to="/menu" class="inline-block bg-[#DC2626] hover:bg-red-700 text-white font-sora text-xs uppercase tracking-widest px-12 py-4.5 rounded-lg font-bold transition-all duration-300 text-center">
              Pesan Sekarang
            </router-link>
          </div>
        </div>
      </section>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { 
  Coffee, Wifi, Zap, Utensils, DollarSign, Moon, Shield, Tv, 
  Music, Gamepad2, Beer, BatteryCharging, Heart, Award, Smartphone 
} from "lucide-vue-next";
import axios from "axios";

const isLoading = ref(true);
const scrollY = ref(0);
const currentReviewIndex = ref(0);
let reviewInterval = null;

// State Utama CMS
const cms = ref({
  hero_headline: "",
  hero_subheadline: "",
  hero_food_image: null,
  marquee_text: "",
  about_text: "",
  about_image: null,
  metric_1: "",
  metric_2: "",
  metric_3: ""
});

const defaultHeroFood = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=600";
const defaultAboutImage = "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=1000";

const bestSellers = ref([]);
const bentoFacilities = ref([]);
const galleryData = ref([]);
const reviews = ref([]);

// Mapping Icon Lucide
const iconMap = {
  Coffee, Wifi, Zap, Utensils, DollarSign, Moon, Shield, Tv, 
  Music, Gamepad2, Beer, BatteryCharging, Heart, Award, Smartphone
};

// Computed property untuk membatasi tampilan gallery maksimal 6 foto teratas
const displayedGallery = computed(() => {
  return galleryData.value.slice(0, 6);
});

const fetchBestSellers = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/menus/bestsellers/");
    if (res.data && res.data.length > 0) {
      bestSellers.value = res.data.map(item => ({
        name: item.name,
        desc: item.description || item.desc || "Menu favorit pilihan squad Masashimura.",
        price: item.price,
        image: item.image || "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=500"
      }));
    } else {
      bestSellers.value = [
        { name: "Mie Nyemek Masashimura", desc: "Mie kuah kental super gurih racikan bumbu warkop rahasia.", price: 18000, image: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=500" },
        { name: "Nasi Goreng Gila", desc: "Nasi goreng aroma smoky wok khas abang-abang kafe.", price: 22000, image: "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?q=80&w=500" },
        { name: "Kopi Susu Gula Aren", desc: "Double shot espresso robusta dicampur susu murni creamy.", price: 15000, image: "https://images.unsplash.com/photo-1541167760496-1628856ab772?q=80&w=500" }
      ];
    }
  } catch (err) {
    console.error("Gagal memuat data menu terlaris:", err);
  }
};

const fetchGoogleReviews = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/homepage/reviews/maps/");
    if (res.data && res.data.length > 0) {
      reviews.value = res.data;
    } else {
      reviews.value = [
        { name: "Irfan Setya", status: "Maps Local Guide", text: "Gokil bener WiFi Masashimura, harganya ramah banget di kantong mahasiswa semester tua!" },
        { name: "Helen S", status: "Maps Reviewer", text: "Tiap kali nyari tempat nongkrong yang gak bising tapi estetik minimalis, nemunya Masashimura." }
      ];
    }
  } catch (err) {
    console.error("Gagal mengambil data review Google Maps:", err);
  }
};

const fetchBentoAndGallery = async () => {
  try {
    const [bentoRes, galleryRes] = await Promise.all([
      axios.get("http://127.0.0.1:8000/api/homepage/bento/"),
      axios.get("http://127.0.0.1:8000/api/homepage/gallery/")
    ]);
    
    if (bentoRes.data && bentoRes.data.length > 0) {
      bentoFacilities.value = bentoRes.data;
    } else {
      // Fallback Bento Grid jika kosong di DB
      bentoFacilities.value = [
        { title: "Nyaman Maksimal", icon_name: "Coffee", size: "large" },
        { title: "Free WiFi", icon_name: "Wifi", size: "normal" },
        { title: "Banyak Colokan", icon_name: "Zap", size: "normal" },
        { title: "Nongkrong Sampai Larut Malam", icon_name: "Moon", size: "normal" }
      ];
    }
    
    if (galleryRes.data && galleryRes.data.length > 0) {
      galleryData.value = galleryRes.data;
    } else {
      // Fallback Gallery default link asset
      galleryData.value = [
        { title: "Nobar Seru Squad", image_url: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=400" },
        { title: "Suasana Malam Kedai", image_url: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=400" },
        { title: "Live Akustik Session", image_url: "https://images.unsplash.com/photo-1541167760496-1628856ab772?q=80&w=400" }
      ];
    }
  } catch (err) {
    console.error("Gagal mengambil data bento/gallery:", err);
  }
};

const fetchCMSData = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/homepage/config/current/");
    if (res.data) {
      const d = res.data;
      cms.value = {
        hero_headline: d.hero_headline?.trim() ? d.hero_headline : "Warkop Level Up\nMasashimura",
        hero_subheadline: d.hero_subheadline?.trim() ? d.hero_subheadline : "Tempat nongkrong kasual modern di Bekasi dengan cita rasa nikmat dan harga yang sangat bersahabat.",
        hero_food_image: d.hero_food_image,
        marquee_text: d.marquee_text?.trim() ? d.marquee_text : "MASA SIH MURAH? • WARKOP EVOLUTION • GOOD FOOD • GOOD VIBES • SINCE 2021",
        about_text: d.about_text?.trim() ? d.about_text : "Masashimura adalah sebuah usaha kuliner personal asal Bekasi yang didirikan pada tahun 2021. Mengusung konsep tempat makan dan nongkrong yang kasual, Masashimura hadir menjadi jawaban bagi para pencinta kuliner, pelajar, mahasiswa, hingga anak muda.",
        about_image: d.about_image,
        metric_1: d.metric_1?.trim() ? d.metric_1 : "2021",
        metric_2: d.metric_2?.trim() ? d.metric_2 : "50+",
        metric_3: d.metric_3?.trim() ? d.metric_3 : "★★★★★"
      };
    }
  } catch (err) {
    console.error("CMS API disconnect, using local text defaults:", err);
  }
};

const handleScroll = () => {
  scrollY.value = window.scrollY;
  document.documentElement.style.setProperty('--scroll-offset', `${scrollY.value * 0.15}px`);
};

// Penggabungan Siklus OnMounted Tunggal Terintegrasi
onMounted(async () => {
  window.addEventListener("scroll", handleScroll);
  
  // Ambil seluruh data secara berkala
  await Promise.all([
    fetchCMSData(),
    fetchBestSellers(),
    fetchGoogleReviews(),
    fetchBentoAndGallery()
  ]);
  
  isLoading.value = false;

  reviewInterval = setInterval(() => {
    if (reviews.value.length > 0) {
      currentReviewIndex.value = (currentReviewIndex.value + 1) % reviews.value.length;
    }
  }, 5000);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
  if (reviewInterval) clearInterval(reviewInterval);
});
</script>

<style scoped>
/* Marquee Animation */
@keyframes marquee {
  0% { transform: translateX(0%); }
  100% { transform: translateX(-50%); }
}
.animate-marquee {
  display: flex;
  width: max-content;
  animation: marquee 35s linear infinite;
}

/* Stagger & Fade Presets */
.animate-fade-up {
  animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.animate-fade-in {
  animation: fadeIn 1s ease-out forwards;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide Slider Review CSS */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.6s ease;
  position: absolute;
  width: 100%;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(15px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}
</style> 