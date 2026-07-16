// src/stores/orderNotifications.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { toast } from 'vue-sonner';
import apiClient from '@/api/client';
import { playNewOrderChime } from '@/utils/notificationSound';

const POLL_INTERVAL_MS = 8000;

export const useOrderNotificationsStore = defineStore('orderNotifications', () => {
  const lastSeenId   = ref(null);   // null = belum pernah bootstrap
  const unreadCount  = ref(0);      // buat badge di sidebar "Active Orders"
  let pollingTimer   = null;

const checkForNewOrders = async () => {
    try {
      const params = lastSeenId.value !== null ? { after_id: lastSeenId.value } : {};
      const { data } = await apiClient.get('/orders/notifications/', { params });

      // Amankan data: Kalau backend ngereturn array langsung, pakai data. 
      // Kalau ngereturn object { new_orders: [...] }, pakai data.new_orders.
      const orders = Array.isArray(data) ? data : (data.new_orders || []);

      // Panggilan pertama (lastSeenId masih null): cuma bootstrap cursor
      if (lastSeenId.value === null) {
        if (orders.length > 0) {
          // Cari ID paling besar dari data yang ada
          lastSeenId.value = Math.max(...orders.map(o => o.id));
        } else {
          // Kalau database masih kosong banget, set ke 0
          lastSeenId.value = 0; 
        }
        return;
      }

      // Kalau ada orderan baru (array tidak kosong)
      if (orders.length > 0) {
        playNewOrderChime();
        
        orders.forEach((o) => {
          toast.success(`Pesanan baru masuk — ${o.order_number}`, {
            description: `${o.customer_name} · Rp ${Number(o.total_price).toLocaleString('id-ID')}`,
            duration: 6000,
          });
        });
        
        unreadCount.value += orders.length;
        
        // Update cursor ke ID terbesar dari batch pesanan baru ini
        lastSeenId.value = Math.max(...orders.map(o => o.id));
      }

    } catch (err) {
      console.error('[order-notifications] polling gagal:', err);
    }
  };

  const startPolling = () => {
    if (pollingTimer) return; // udah jalan, jangan dobel
    checkForNewOrders();
    pollingTimer = setInterval(checkForNewOrders, POLL_INTERVAL_MS);
  };

  const stopPolling = () => {
    if (pollingTimer) {
      clearInterval(pollingTimer);
      pollingTimer = null;
    }
  };

  const clearUnread = () => {
    unreadCount.value = 0;
  };

  return { lastSeenId, unreadCount, startPolling, stopPolling, clearUnread, checkForNewOrders };
});
