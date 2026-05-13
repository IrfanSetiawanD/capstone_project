// src/api/stats.js
import apiClient from './client'

export const statsAPI = {
  getDashboardSummary: () => {
    return apiClient.get('/stats/dashboard/')
  },

  getLoyalCustomers: (month = null) => {
    const params = month ? { month } : {}
    return apiClient.get('/stats/loyal-customers/', { params })
  },

  getMonthlyStats: (year = null) => {
    const params = year ? { year } : {}
    return apiClient.get('/stats/monthly/', { params })
  }
}