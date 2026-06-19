<template>
  <form
    @submit.prevent="handleSubmit"
    class="p-8 space-y-6 overflow-y-auto flex-1 custom-scroll"
  >
    <div>
      <label
        class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald"
        >Nama Menu</label
      >
      <input
        v-model="form.name"
        type="text"
        required
        class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white outline-none focus:border-red-600"
      />
    </div>

    <div>
      <label
        class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald"
        >Deskripsi</label
      >
      <textarea
        v-model="form.description"
        rows="3"
        class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white outline-none focus:border-red-600"
      ></textarea>
    </div>

    <div class="grid grid-cols-2 gap-6">
      <div>
        <label
          class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald"
          >Kategori</label
        >
        <select
          v-model="form.category"
          required
          class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white outline-none focus:border-red-600"
        >
          <option value="">Pilih Kategori</option>
          <option value="Makanan">Makanan</option>
          <option value="Minuman">Minuman</option>
          <option value="Snacks">Snacks</option>
        </select>
      </div>
      <div>
        <label
          class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald"
          >Harga (Rp)</label
        >
        <input
          v-model="form.price"
          type="number"
          required
          class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white outline-none focus:border-red-600"
        />
      </div>
    </div>

    <div>
      <label
        class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald"
        >Foto Menu</label
      >
      <div
        v-if="previewImage"
        class="mb-4 border border-white/10 rounded-xl overflow-hidden"
      >
        <img :src="previewImage" class="w-full h-48 object-cover" />
      </div>
      <button
        type="button"
        @click="triggerCropper"
        class="w-full py-4 border border-dashed border-white/20 hover:border-red-600 rounded-xl text-white/60 hover:text-white transition-all"
      >
        {{ previewImage ? "Ganti Foto (Crop Ulang)" : "Pilih Foto Menu" }}
      </button>
    </div>

    <div class="flex gap-4 pt-6">
      <button
        type="button"
        @click="$emit('cancel')"
        class="flex-1 py-4 border border-white/10 hover:bg-white/5 text-white/40 hover:text-white rounded-sm font-oswald uppercase text-xs tracking-widest transition"
      >
        Batal
      </button>
      <button
        type="submit"
        :disabled="loading"
        class="flex-1 py-4 bg-red-600 hover:bg-red-500 text-white font-oswald uppercase tracking-widest font-bold rounded-sm disabled:opacity-50 transition"
      >
        {{
          loading
            ? "Menyimpan..."
            : editingMenu
              ? "Simpan Perubahan"
              : "Tambahkan Menu"
        }}
      </button>
    </div>

    <ImageCropper
      v-if="showCropper"
      :image="selectedImage"
      @crop-complete="onCropComplete"
      @cancel="showCropper = false"
    />
  </form>
</template>

<script setup>
import { ref, watch } from "vue";
import { toast } from "vue-sonner";
import { menuAPI } from "@/api";
import ImageCropper from "../ImageCropper.vue";

const props = defineProps({ editingMenu: Object });
const emit = defineEmits(["created", "cancel"]);

const form = ref({
  name: "",
  description: "",
  category: "",
  price: "",
  image: null,
});
const previewImage = ref(null);
const loading = ref(false);
const showCropper = ref(false);
const selectedImage = ref(null);

const resetForm = () => {
  form.value = {
    name: "",
    description: "",
    category: "",
    price: "",
    image: null,
  };
  previewImage.value = null;
};

watch(
  () => props.editingMenu,
  (menu) => {
    if (menu) {
      form.value = { ...menu };
      previewImage.value = menu.image_url || null;
    } else resetForm();
  },
  { immediate: true },
);

const triggerCropper = () => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      selectedImage.value = URL.createObjectURL(file);
      showCropper.value = true;
    }
  };
  input.click();
};

const onCropComplete = (croppedBlob) => {
  showCropper.value = false;
  form.value.image = croppedBlob;
  previewImage.value = URL.createObjectURL(croppedBlob);
  toast.success("Foto berhasil dipotong!");
};

const handleSubmit = async () => {
  if (!form.value.name || !form.value.price) {
    toast.error("Nama dan harga wajib diisi");
    return;
  }
  loading.value = true;
  const formData = new FormData();
  formData.append("name", form.value.name);
  formData.append("description", form.value.description || "");
  formData.append("category", form.value.category || "");
  formData.append("price", form.value.price);
  if (form.value.image) formData.append("image", form.value.image);

  try {
    if (props.editingMenu) {
      await menuAPI.update(props.editingMenu.id, formData);
      toast.success("Menu berhasil diperbarui!");
    } else {
      await menuAPI.create(formData);
      toast.success("Menu baru berhasil ditambahkan!");
    }
    emit("created");
  } catch (err) {
    toast.error("Gagal menyimpan menu ke database");
  } finally {
    loading.value = false;
  }
};
</script>
