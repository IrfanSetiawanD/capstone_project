<template>
  <div v-if="open" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/90 backdrop-blur-md p-4">
    <div class="bg-[#0a0a0a] w-full max-w-2xl rounded-2xl overflow-hidden border border-white/10 shadow-2xl flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="px-8 py-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
        <h2 class="text-2xl font-oswald uppercase tracking-wider text-white italic">
          {{ editingMenu ? 'Edit Menu' : 'Tambah Menu Baru' }}
        </h2>
        <button @click="closeModal" class="text-white/40 hover:text-red-400 text-3xl">✕</button>
      </div>

      <form @submit.prevent="handleSubmit" class="p-8 space-y-6 overflow-y-auto flex-1">
        <div>
          <label class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald">Nama Menu</label>
          <input v-model="form.name" type="text" required class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white" />
        </div>

        <div>
          <label class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald">Deskripsi</label>
          <textarea v-model="form.description" rows="3" class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white"></textarea>
        </div>

        <div class="grid grid-cols-2 gap-6">
          <div>
            <label class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald">Kategori</label>
            <select v-model="form.category" required class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white">
              <option value="">Pilih Kategori</option>
              <option value="Makanan">Makanan</option>
              <option value="Minuman">Minuman</option>
              <option value="Snacks">Snacks</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald">Harga (Rp)</label>
            <input v-model="form.price" type="number" required class="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-3 text-white" />
          </div>
        </div>

        <!-- Foto + Crop -->
        <div>
          <label class="block text-[10px] uppercase tracking-widest text-white/40 mb-2 font-oswald">Foto Menu</label>
          
          <div v-if="previewImage" class="mb-4 border border-white/10 rounded-xl overflow-hidden">
            <img :src="previewImage" class="w-full h-48 object-cover" />
          </div>

          <button type="button" @click="triggerCropper"
                  class="w-full py-4 border border-dashed border-white/20 hover:border-primary rounded-xl text-white/60 hover:text-white">
            {{ previewImage ? 'Ganti Foto (Crop Ulang)' : 'Pilih Foto Menu' }}
          </button>
        </div>

        <div class="flex gap-4 pt-6">
          <button type="button" @click="closeModal" class="flex-1 py-4 border border-white/10 hover:bg-white/5 text-white/40 hover:text-white rounded-sm font-oswald uppercase text-xs tracking-widest">Batal</button>
          <button type="submit" :disabled="loading" class="flex-1 py-4 bg-primary hover:bg-red-600 text-white font-oswald uppercase tracking-widest font-bold rounded-sm disabled:opacity-50">
            {{ loading ? 'Menyimpan...' : (editingMenu ? 'Simpan Perubahan' : 'Tambahkan Menu') }}
          </button>
        </div>
      </form>
    </div>

    <!-- Cropper Modal -->
    <ImageCropperModal
      v-if="showCropper"
      :image="selectedImage"
      @crop-complete="onCropComplete"
      @cancel="showCropper = false"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { toast } from 'vue-sonner'
import { menuAPI } from '@/api'           // ← Tambahan ini
import ImageCropperModal from './ImageCropper.vue'

const props = defineProps({
  open: Boolean,
  editingMenu: Object
})

const emit = defineEmits(['update:open', 'created'])

const form = ref({ name: '', description: '', category: '', price: '', image: null })
const previewImage = ref(null)
const loading = ref(false)
const showCropper = ref(false)
const selectedImage = ref(null)

const resetForm = () => {
  form.value = { name: '', description: '', category: '', price: '', image: null }
  previewImage.value = null
}

watch(() => props.editingMenu, (menu) => {
  if (menu) {
    form.value = { ...menu }
    previewImage.value = menu.image_url || null
  } else resetForm()
}, { immediate: true })

const triggerCropper = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      selectedImage.value = URL.createObjectURL(file)
      showCropper.value = true
    }
  }
  input.click()
}

const onCropComplete = (croppedBlob) => {
  showCropper.value = false
  form.value.image = croppedBlob
  previewImage.value = URL.createObjectURL(croppedBlob)
  toast.success('Foto berhasil dipotong!')
}

// ======================== INTEGRASI KE DB ========================
const handleSubmit = async () => {
  if (!form.value.name || !form.value.price) {
    toast.error('Nama dan harga wajib diisi')
    return
  }

  loading.value = true
  const formData = new FormData()
  formData.append('name', form.value.name)
  formData.append('description', form.value.description || '')
  formData.append('category', form.value.category || '')
  formData.append('price', form.value.price)
  if (form.value.stock !== undefined) formData.append('stock', form.value.stock)

  if (form.value.image) {
    formData.append('image', form.value.image)
  }

  try {
    if (props.editingMenu) {
      await menuAPI.update(props.editingMenu.id, formData)
      toast.success('Menu berhasil diperbarui!')
    } else {
      await menuAPI.create(formData)
      toast.success('Menu baru berhasil ditambahkan!')
    }
    emit('created')
    closeModal()
  } catch (err) {
    console.error(err)
    toast.error('Gagal menyimpan menu ke database')
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  emit('update:open', false)
  setTimeout(resetForm, 300)
}
</script>