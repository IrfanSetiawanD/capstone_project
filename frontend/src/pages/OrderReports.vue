<template>
  <div class="flex min-h-screen bg-[#050505] text-white">
    <AdminSidebar />

    <main class="flex-1 ml-64 p-8 md:p-12 overflow-x-hidden font-manrope">
      <div class="max-w-7xl mx-auto">
        
        <div class="flex flex-col md:flex-row justify-between items-end mb-12 gap-6">
          <div>
            <h1 class="font-oswald text-5xl uppercase italic tracking-tighter">Menu Reports</h1>
            <p class="text-white/40 text-sm font-light mt-1">Analisis performa produk dan tren penjualan bulanan</p>
          </div>
          
          <div class="flex gap-4">
            <div class="relative group">
              <select class="appearance-none bg-[#0a0a0a] border border-white/10 rounded-xl px-6 py-3 text-xs font-oswald uppercase tracking-widest outline-none focus:border-primary transition-all pr-12">
                <option>April 2026</option>
                <option>Maret 2026</option>
                <option>Februari 2026</option>
              </select>
              <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-white/20">
                <ChevronDown size="14" />
              </div>
            </div>

            <button class="flex items-center gap-2 bg-white/5 border border-white/10 px-6 py-3 rounded-xl text-[10px] font-oswald uppercase tracking-widest hover:bg-white/10 transition-all">
              <Download size="14" class="text-primary" /> Export PDF
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          
          <div class="bg-[#0a0a0a] border border-white/5 p-10 rounded-3xl h-[450px] flex flex-col hover:border-primary/20 transition-all duration-500">
            <div class="flex justify-between items-start mb-12">
              <h3 class="font-oswald uppercase text-white/40 text-xs tracking-widest flex items-center gap-2">
                <TrendingUp size="16" class="text-primary" /> Tren Penjualan Mingguan
              </h3>
              <span class="text-[10px] bg-primary/10 text-primary px-2 py-1 rounded">+12.5%</span>
            </div>
            
            <div class="flex-grow flex items-end justify-between gap-3 px-2">
              <div v-for="(h, index) in [20, 50, 80, 40, 90, 70, 100]" :key="index" 
                   :style="{ height: h + '%' }" 
                   class="w-full bg-gradient-to-t from-primary/10 to-primary/80 rounded-t-sm relative group">
                <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-white text-black text-[10px] font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                  Rp {{ (h * 10000).toLocaleString('id-ID') }}
                </div>
              </div>
            </div>
            
            <div class="flex justify-between mt-8 text-[10px] font-oswald text-white/20 uppercase tracking-[0.2em] px-1">
              <span>Sen</span><span>Sel</span><span>Rab</span><span>Kam</span><span>Jum</span><span>Sab</span><span>Min</span>
            </div>
          </div>

          <div class="bg-[#0a0a0a] border border-white/5 p-10 rounded-3xl flex flex-col hover:border-accent/20 transition-all duration-500">
            <h3 class="font-oswald uppercase text-white/40 text-xs tracking-widest mb-10 flex items-center gap-2">
              <Award size="16" class="text-accent" /> Menu Paling Laku
            </h3>
            
            <div class="space-y-10">
              <div v-for="item in popularMenus" :key="item.name" class="space-y-3">
                <div class="flex justify-between text-sm items-end">
                  <span class="font-oswald text-white uppercase tracking-tight">{{ item.name }}</span>
                  <span class="text-accent font-bold text-xs">{{ item.value }}%</span>
                </div>
                <div class="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-accent h-full transition-all duration-1000 ease-out" :style="{ width: item.value + '%' }"></div>
                </div>
              </div>
            </div>

            <div class="mt-auto pt-10">
              <div class="p-4 bg-accent/5 border border-accent/10 rounded-xl">
                <p class="text-[11px] text-accent/60 leading-relaxed italic font-light">
                  *Data ini dihitung berdasarkan pesanan yang statusnya sudah "Completed" di sistem admin.
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminSidebar from '@/components/AdminSidebar.vue'
import { TrendingUp, Award, Download, ChevronDown } from 'lucide-vue-next'

// Logic menu terpopuler tetap gw pertahanin tapi gw bikin lebih dinamis
const popularMenus = ref([
  { name: 'Beef Yakiniku Masashimura', value: 92 },
  { name: 'Es Teh Masashi Gede', value: 85 },
  { name: 'Ayam Goreng Sambal Matah', value: 70 },
  { name: 'Chicken Teriyaki', value: 65 }
])
</script>