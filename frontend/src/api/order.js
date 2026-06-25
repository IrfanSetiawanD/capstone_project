import apiClient from "./client";

export const orderAPI = {
  getAll: () => apiClient.get("/orders/list/"),
  getById: (id) => apiClient.get(`/orders/${id}/`),
  create: (orderData) => apiClient.post("/orders/", orderData),

  // Dipakai untuk silent loyalty check di Checkout.vue (lihat stores/cart.js -> checkLoyalty)
  checkLoyalty: (phone) =>
    apiClient.get("/orders/check-loyalty/", { params: { phone } }),

  getLoyalCustomers: () => apiClient.get("/orders/loyal/"),
  getOrderReports: (params = {}) =>
    apiClient.get("/orders/reports/", { params }),

  // Dipakai oleh ActiveOrders.vue
  getActiveOrders: (targetDate) =>
    apiClient.get("/active-orders/", { params: { target_date: targetDate } }),
};