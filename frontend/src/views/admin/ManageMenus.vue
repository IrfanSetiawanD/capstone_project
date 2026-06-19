<template>
  <div class="w-full p-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="font-oswald text-4xl uppercase tracking-tighter text-white">
          Kelola Menu
        </h1>
        <p class="text-white/40 text-sm">Manajemen inventaris dan harga</p>
      </div>
      <button
        @click="openAddModal"
        class="bg-red-600 hover:bg-red-500 px-6 py-3 rounded-2xl text-white font-oswald uppercase text-sm tracking-widest flex items-center gap-2 transition-colors"
      >
        <span>+</span> TAMBAH MENU
      </button>
    </div>

    <div
      v-if="menus.length === 0"
      class="bg-[#0a0a0a] border border-white/5 rounded-2xl p-12 text-center text-white/40"
    >
      <p class="mb-4">Belum ada menu yang dimuat.</p>
      <button @click="fetchMenus" class="text-red-500 underline text-sm">
        Segarkan Data
      </button>
    </div>

    <div v-else class="space-y-8">
      <div
        v-for="(group, categoryName) in groupedMenus"
        :key="categoryName"
        class="space-y-3"
      >
        <h3
          class="font-oswald text-lg uppercase tracking-wider text-red-600 px-2 border-l-2 border-red-600"
        >
          {{ categoryName }}
        </h3>

        <div
          class="bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden"
        >
          <table class="w-full text-left">
            <thead class="bg-white/5">
              <tr
                class="text-white/40 text-xs font-oswald uppercase tracking-widest"
              >
                <th class="px-8 py-4">NAMA MENU</th>
                <th class="px-8 py-4">KATEGORI</th>
                <th class="px-8 py-4 text-right">HARGA</th>
                <th class="px-8 py-4 text-center">STOCK</th>
                <th class="px-8 py-4 text-center">AKSI</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr
                v-for="menu in group"
                :key="menu.id"
                class="hover:bg-white/5 transition-colors"
              >
                <td class="px-8 py-4 font-medium">
                  {{ menu.name || menu.nama_menu }}
                </td>
                <td class="px-8 py-4">
                  <span
                    class="px-3 py-1 text-[10px] rounded-full bg-white/10 uppercase text-amber-400"
                  >
                    {{ displayCategory(menu.category) }}
                  </span>
                </td>
                <td class="px-8 py-4 text-right font-oswald text-amber-500">
                  {{ formatPrice(menu.price || menu.harga) }}
                </td>
                <td
                  class="px-8 py-4 text-center font-bold"
                  :class="menu.stock > 0 ? 'text-emerald-400' : 'text-red-500'"
                >
                  {{ menu.stock || 0 }}
                </td>
                <td class="px-8 py-4 text-center space-x-4">
                  <button
                    @click="editMenu(menu)"
                    class="text-blue-400 hover:text-blue-300 text-sm"
                  >
                    Edit
                  </button>
                  <button
                    @click="deleteMenu(menu.id)"
                    class="text-red-400 hover:text-red-300 text-sm"
                  >
                    Hapus
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <MenuFormModal
      :open="isDialogOpen"
      :editing-menu="editingMenu"
      @update:open="isDialogOpen = $event"
      @created="fetchMenus"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { menuAPI } from "@/api";
import { toast } from "vue-sonner";
import MenuFormModal from "@/components/ui/modals/MenuFormModal.vue";

const menus = ref([]);
const isDialogOpen = ref(false);
const editingMenu = ref(null);

const formatPrice = (price) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(price || 0);

const displayCategory = (cat) => {
  if (!cat) return "LAINNYA";
  if (typeof cat === "object" && cat.name) return cat.name;
  if (cat == 1) return "MAIN COURSE";
  if (cat == 2) return "DRINKS";
  return String(cat);
};

const groupedMenus = computed(() => {
  return menus.value.reduce((groups, menu) => {
    let cat = displayCategory(menu.category || menu.kategori).toUpperCase();
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(menu);
    return groups;
  }, {});
});

const fetchMenus = async () => {
  try {
    const res = await menuAPI.getAll();
    menus.value =
      res.data?.results || (Array.isArray(res.data) ? res.data : []);
  } catch (err) {
    toast.error("Gagal mengambil data menu");
  }
};

const openAddModal = () => {
  editingMenu.value = null;
  isDialogOpen.value = true;
};

const editMenu = (menu) => {
  editingMenu.value = menu;
  isDialogOpen.value = true;
};

const deleteMenu = async (id) => {
  if (!confirm("Yakin hapus menu ini?")) return;
  try {
    await menuAPI.delete(id);
    toast.success("Menu berhasil dihapus");
    fetchMenus();
  } catch (err) {
    toast.error("Gagal menghapus menu");
  }
};

onMounted(fetchMenus);
</script>
