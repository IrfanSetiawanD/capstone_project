// src/api/order.js
import apiClient from './client'

export const orderAPI = {
  getAll: () => apiClient.get('/orders/'),

  getById: (id) => apiClient.get(`/orders/${id}/`),

  create: (orderData) => apiClient.post('/orders/', orderData),

  getLoyalCustomers: () => apiClient.get('/orders/loyal/'),

  getOrderReports: (params = {}) => apiClient.get('/orders/reports/', { params })
}