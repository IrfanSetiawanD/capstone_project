<template>
  <div v-if="open" class="fixed inset-0 bg-black/70 flex items-center justify-center z-[100]">
    <div class="bg-[#0a0a0a] border border-white/10 rounded-3xl w-full max-w-md mx-4 overflow-hidden">
      <!-- Header -->
      <div class="px-8 py-6 border-b border-white/10">
        <h2 class="font-oswald text-2xl uppercase tracking-tight">Buat Akun Baru</h2>
        <p class="text-white/50 text-sm">Hanya Owner yang dapat membuat akun</p>
      </div>

      <form @submit.prevent="handleSubmit" class="p-8 space-y-6">
        <div>
          <label class="block text-sm text-white/70 mb-2">Username</label>
          <input
            v-model="form.username"
            type="text"
            required
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-500 outline-none"
            placeholder="adminbaru"
          />
        </div>

        <div>
          <label class="block text-sm text-white/70 mb-2">Email</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-500 outline-none"
            placeholder="adminbaru@masashimura.id"
          />
        </div>

        <div>
          <label class="block text-sm text-white/70 mb-2">Password</label>
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            required
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-500 outline-none"
          />
        </div>

        <div>
          <label class="block text-sm text-white/70 mb-2">Role</label>
          <select
            v-model="form.role"
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-red-500 outline-none"
          >
            <option value="admin">Admin</option>
            <option value="owner">Owner</option>
          </select>
        </div>

        <div class="flex gap-4 pt-4">
          <button
            type="button"
            @click="closeModal"
            class="flex-1 py-4 border border-white/20 rounded-2xl text-white/70 hover:bg-white/5 transition"
          >
            Batal
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 py-4 bg-red-600 hover:bg-red-500 rounded-2xl font-bold uppercase transition disabled:opacity-50"
          >
            {{ loading ? 'Membuat Akun...' : 'Buat Akun' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { toast } from 'vue-sonner'
import { userAPI } from '@/api'   // nanti kita buat

const props = defineProps({
  open: Boolean
})

const emit = defineEmits(['update:open', 'created'])

const form = ref({
  username: '',
  email: '',
  password: '',
  role: 'admin'
})

const loading = ref(false)
const showPassword = ref(false)

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    toast.error('Username dan password wajib diisi')
    return
  }

  loading.value = true

  try {
    await userAPI.createUser(form.value)
    toast.success(`Akun ${form.value.username} berhasil dibuat!`)
    emit('created')
    closeModal()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Gagal membuat akun')
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  emit('update:open', false)
  // Reset form
  form.value = { username: '', email: '', password: '', role: 'admin' }
}
</script>