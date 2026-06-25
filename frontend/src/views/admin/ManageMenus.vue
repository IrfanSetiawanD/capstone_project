<template>
  <div class="w-full p-4 sm:p-8 text-white max-w-7xl mx-auto box-border">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
      <div>
        <h1 class="font-oswald text-3xl uppercase tracking-tighter text-white">Kelola Menu</h1>
        <p class="text-white/40 text-sm">Manajemen inventaris dan kontrol status ketersediaan</p>
      </div>
      <button @click="openAddModal" class="bg-red-600 px-6 py-3 rounded-2xl text-white">
        + TAMBAH MENU
      </button>
    </div>

<MenuFormModal
  v-if="isDialogOpen"
  :editing-menu="editingMenu"
  @close="closeModal"
  @saved="handleSaved"
/>

    <div v-if="menus.length > 0" class="space-y-8">
      <div v-for="(group, categoryName) in groupedMenus" :key="categoryName" class="space-y-3">
        <h3 class="font-oswald text-lg uppercase tracking-wider text-red-600 px-2 border-l-2 border-red-600">{{ categoryName }}</h3>
        <div class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden shadow-2xl">
          <div class="overflow-x-auto w-full">
            <table class="w-full text-left border-collapse min-w-[650px]">
              <thead class="bg-white/5 text-white/40 text-xs font-oswald uppercase tracking-widest">
                <tr>
                  <th class="px-6 py-4">NAMA MENU</th>
                  <th class="px-6 py-4">HARGA</th>
                  <th class="px-6 py-4 text-center">STATUS STOK</th>
                  <th class="px-6 py-4 text-center">AKSI</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr v-for="menu in group" :key="menu.id" class="hover:bg-white/5 transition-colors">
                  <td class="px-6 py-4 font-medium">{{ menu.name }}</td>
                  <td class="px-6 py-4 font-mono">{{ formatPrice(menu.price) }}</td>
                  <td class="px-6 py-4 text-center">
                    <button
                      @click="toggleStock(menu)"
                      :class="menu.is_available ? 'bg-emerald-600/10 text-emerald-400' : 'bg-red-900/20 text-red-500 border border-red-500'"
                      class="px-3 py-1 rounded-lg text-[10px] font-bold uppercase transition-all"
                    >
                      {{ menu.is_available ? '🟢 READY' : '🔴 SOLDOUT' }}
                    </button>
                  </td>
                  <td class="px-6 py-4 text-center space-x-4">
                    <button @click="editMenu(menu)" class="text-blue-400 hover:text-blue-300 text-xs uppercase font-bold">Edit</button>
                    <button @click="deleteMenu(menu)" class="text-red-400 hover:text-red-300 text-xs uppercase font-bold">Hapus</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted, computed } from "vue";
import { toast } from "vue-sonner";
import apiClient from "@/api/client";
import MenuFormModal from "@/components/ui/forms/MenuForm.vue";

console.log("MenuFormModal =", MenuFormModal);
console.log("MODAL MOUNTED");

const menus = ref([]);
const isDialogOpen = ref(false);
const editingMenu = ref(null);
const router = useRouter();

const fetchMenus = async () => {
  try {
    const res = await apiClient.get("/menus/");
    menus.value = res.data;
  } catch (err) {
    toast.error("Gagal memuat data menu");
  }
};

const closeModal = () => {
  console.log("CLOSE MODAL DIPANGGIL");

  isDialogOpen.value = false;
  editingMenu.value = null;
};

const handleSaved = async () => {
  await fetchMenus();

  isDialogOpen.value = false;
  editingMenu.value = null;
};

const groupedMenus = computed(() => {
  return menus.value.reduce((groups, menu) => {
    // Cek bentuk asli field ini dari response GET /menus/ lo: kalau backend
    // mengembalikan category sebagai ID, ganti ke field nama kategori yang
    // sesuai (mis. menu.category_name) supaya label grup tidak jadi angka.
    const cat = menu.category || "LAINNYA";
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(menu);
    return groups;
  }, {});
});

const formatPrice = (p) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(p);

const toggleStock = async (menu) => {
  try {
    const newStatus = !menu.is_available;
    await apiClient.patch(`/menus/${menu.id}/`, { is_available: newStatus });
    menu.is_available = newStatus;
    toast.success(`Status ${menu.name} diubah`);
  } catch (err) {
    toast.error("Gagal update status");
  }
};

// ManageMenus.vue script setup
const deleteMenu = async (menu) => {
  if (!confirm("Yakin hapus menu? Foto juga akan terhapus.")) return;

  try {
    // Cukup panggil API, biarkan Django yang handle hapus di Cloudinary (lewat signal/view)
    await apiClient.delete(`/menus/${menu.id}/`);
    await fetchMenus();
    toast.success("Menu berhasil dihapus");
  } catch (err) {
    toast.error("Gagal menghapus menu");
  }
};

const openAddModal = () => {
  console.log("modal dibuka");
  editingMenu.value = null;
  isDialogOpen.value = true;
};

const editMenu = (menu) => {
  editingMenu.value = menu;
  isDialogOpen.value = true;
};

onMounted(async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    toast.error("Kamu belum login!");
    router.push("/login");
    return;
  }
  await fetchMenus();
});
</script>