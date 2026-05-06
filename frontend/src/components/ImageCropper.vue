<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-[99999] bg-black/90 backdrop-blur-sm flex items-center justify-center p-4" @click.stop>
      <div class="w-full max-w-2xl bg-[#121212] p-6 rounded-lg border border-white/10 shadow-2xl">
        <h3 class="text-white text-center mb-4 font-oswald uppercase tracking-widest text-yellow-500">
          Potong Foto Menu (1147 × 644)
        </h3>
        
        <div class="relative w-full h-[400px] bg-black overflow-hidden rounded-md border border-white/5">
          <cropper
            ref="cropperRef"
            class="h-full w-full"
            :src="image"
            :stencil-props="{ aspectRatio: 1147 / 644 }"
          />
        </div>

        <div class="mt-6 flex gap-4">
          <button
            type="button"
            @click="onCancel"
            class="flex-1 py-3 bg-white/10 text-white uppercase text-xs font-bold rounded hover:bg-white/20 transition-all"
          >
            Batal
          </button>
          <button
            type="button"
            @click="handleGenerate"
            class="flex-[2] py-3 bg-yellow-600 text-black uppercase text-xs font-bold rounded hover:bg-yellow-500 transition-all"
          >
            Simpan Potongan
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'

const props = defineProps({ image: String })
const emit = defineEmits(['crop-complete', 'cancel'])
const cropperRef = ref(null)

const handleGenerate = () => {
  const { canvas } = cropperRef.value.getResult()
  if (canvas) {
    const resized = document.createElement('canvas')
    resized.width = 1147
    resized.height = 644
    const ctx = resized.getContext('2d')
    ctx.drawImage(canvas, 0, 0, 1147, 644)

    resized.toBlob((blob) => {
      if (blob) emit('crop-complete', blob)
    }, 'image/jpeg', 0.92)
  }
}

const onCancel = () => emit('cancel')
</script>