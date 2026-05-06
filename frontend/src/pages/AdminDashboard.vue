<template>
  <div class="flex h-screen bg-[#050505] text-white font-manrope overflow-hidden">
    <AdminSidebar />

    <main class="flex-1 ml-0 lg:ml-64 p-8 md:p-12 relative z-10 overflow-y-auto custom-scroll">
      <div class="max-w-7xl mx-auto">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
          <div>
            <h1 class="font-oswald text-5xl uppercase tracking-tighter italic text-primary">Admin Dashboard</h1>
            <p class="text-white/40 text-sm font-light">Monitoring Bisnis Masashimura Bekasi</p>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
            <p class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald">Total Pendapatan</p>
            <h3 class="text-2xl font-oswald font-bold text-emerald-400">{{ formatPrice(stats.total_revenue) }}</h3>
          </div>
          <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
            <p class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald">Total Pesanan</p>
            <h3 class="text-2xl font-oswald font-bold text-white">{{ stats.total_orders }}</h3>
          </div>
          <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
            <p class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald">Menu Terlaris</p>
            <h3 class="text-lg font-oswald font-bold truncate">{{ stats.top_menus?.[0]?.name || 'Beef Yakiniku' }}</h3>
          </div>
          <div class="bg-[#0a0a0a] border border-white/5 p-6 rounded-2xl shadow-xl">
            <p class="text-white/40 text-[10px] uppercase tracking-widest mb-2 font-oswald">Pelanggan Loyal</p>
            <h3 class="text-2xl font-oswald font-bold text-white">{{ stats.loyal_users?.length || 3 }}</h3>
          </div>
        </div>

        <!-- DAFTAR MENU - VERSI DIPERBAIKI -->
<div class="mt-12">
  <div class="flex justify-between items-center mb-6">
    <h2 class="font-oswald text-3xl uppercase tracking-tighter">Daftar Menu</h2>
    <button @click="openAddModal" 
            class="bg-red-600 hover:bg-red-500 px-6 py-3 rounded-2xl text-white font-oswald uppercase text-sm tracking-widest flex items-center gap-2">
      <span class="text-xl">+</span> TAMBAH MENU
    </button>
  </div>

  <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full min-w-[800px]">
        <thead class="bg-white/5 sticky top-0">
          <tr class="text-white/40 text-xs font-oswald uppercase tracking-widest">
            <th class="px-8 py-5 text-left">NAMA MENU</th>
            <th class="px-8 py-5 text-left">KATEGORI</th>
            <th class="px-8 py-5 text-right">HARGA</th>
            <th class="px-8 py-5 text-center">STOCK</th>
            <th class="px-8 py-5 text-center">AKSI</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr v-for="menu in menus" :key="menu.id" class="hover:bg-white/5 transition-colors">
            <td class="px-8 py-5 font-medium">{{ menu.name }}</td>
            <td class="px-8 py-5">
              <span class="px-4 py-1 text-xs rounded-full bg-white/10">{{ menu.category }}</span>
            </td>
            <td class="px-8 py-5 text-right font-oswald text-lg">{{ formatPrice(menu.price) }}</td>
            <td class="px-8 py-5 text-center font-bold">{{ menu.stock || 0 }}</td>
            <td class="px-8 py-5 text-center space-x-4">
              <button @click="editMenu(menu)" class="text-blue-400 hover:text-blue-300">Edit</button>
              <button @click="deleteMenu(menu.id)" class="text-red-400 hover:text-red-300">Hapus</button>
            </td>
          </tr>

          <!-- Pesan kalau kosong -->
          <tr v-if="menus.length === 0">
            <td colspan="5" class="px-8 py-12 text-center text-white/40">
              Belum ada menu sama sekali.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

        <!-- Menu Form Modal -->
        <MenuFormModal
          :open="isDialogOpen"
          :editing-menu="editingMenu"
          @update:open="isDialogOpen = $event"
          @created="fetchMenus"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { menuAPI, statsAPI } from '@/api'
import { toast } from 'vue-sonner'
import { LogOut } from 'lucide-vue-next'

import MenuFormModal from '@/components/MenuFormModal.vue'
import AdminSidebar from '@/components/AdminSidebar.vue'

const auth = useAuthStore()
const router = useRouter()

const menus = ref([])
const stats = ref({
  total_revenue: 12450000,
  total_orders: 87,
  top_menus: [{ name: 'Beef Yakiniku' }],
  loyal_users: [1, 2, 3]
})
const isDialogOpen = ref(false)
const editingMenu = ref(null)

const formatPrice = (price) => 
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price || 0)

const fetchMenus = async () => {
  try {
    const res = await menuAPI.getAll()
    menus.value = res.data || []
  } catch (err) {
    console.error('Gagal fetch menu:', err)
    toast.error('Gagal mengambil data menu')
  }
}

const fetchAdminStats = async () => {
  try {
    const res = await statsAPI.getDashboardSummary()
    stats.value = res.data
  } catch (err) {
    console.warn('Stats endpoint belum ada')
  }
}

const openAddModal = () => {
  editingMenu.value = null
  isDialogOpen.value = true
}

const editMenu = (menu) => {
  editingMenu.value = menu
  isDialogOpen.value = true
}

const handleFormSubmit = async (formData) => {
  try {
    if (editingMenu.value) {
      await menuAPI.update(editingMenu.value.id, formData)
      toast.success('Menu berhasil diperbarui!')
    } else {
      await menuAPI.create(formData)
      toast.success('Menu baru berhasil ditambahkan!')
    }
    isDialogOpen.value = false
    fetchMenus()
  } catch (err) {
    console.error(err)
    toast.error('Gagal menyimpan menu')
  }
}

const deleteMenu = async (id) => {
  if (!confirm('Yakin hapus menu ini?')) return
  try {
    await menuAPI.delete(id)
    toast.success('Menu berhasil dihapus')
    fetchMenus()
  } catch (err) {
    toast.error('Gagal menghapus menu')
  }
}

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}

onMounted(() => {
  if (!auth.user) {
    router.push('/login')
    return
  }
  fetchMenus()
  fetchAdminStats()
})
</script>