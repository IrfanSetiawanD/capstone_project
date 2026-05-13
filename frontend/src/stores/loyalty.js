// src/stores/loyalty.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { statsAPI } from '@/api'

export const useLoyaltyStore = defineStore('loyalty', () => {
  const loyalCustomers = ref([])
  const loading = ref(false)

  const fetchLoyalCustomers = async () => {
    loading.value = true

    try {
      const response = await statsAPI.getLoyalCustomers()
      loyalCustomers.value = response.data
    } catch (error) {
      console.warn('⚠️ Endpoint loyal-customers belum ada (404) - pakai dummy data')

      // Dummy data sementara
      loyalCustomers.value = [
        {
          phone: "6281234567890",
          month: "Mei 2026",
          order_count: 15,
          total_spent: 2450000,
          is_loyal: true
        },
        {
          phone: "6289876543210",
          month: "Mei 2026",
          order_count: 12,
          total_spent: 1850000,
          is_loyal: true
        }
      ]
    } finally {
      loading.value = false
    }
  }

  return {
    loyalCustomers,
    loading,
    fetchLoyalCustomers
  }
})