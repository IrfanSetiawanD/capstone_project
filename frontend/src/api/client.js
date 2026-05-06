// src/api/client.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request Interceptor - Khusus untuk Django TokenAuthentication
apiClient.interceptors.request.use(
  (config) => {
    // Jangan kirim token saat login
    if (config.url.includes('/auth/login/')) {
      return config
    }

    const token = localStorage.getItem('token')
    if (token) {
      // Django TokenAuthentication pakai format ini:
      config.headers.Authorization = `Token ${token}`
      console.log('🔑 Token dikirim:', `Token ${token.substring(0, 15)}...`)
    } else {
      console.warn('⚠️ Tidak ada token di localStorage')
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response Interceptor
apiClient.interceptors.response.use(
  response => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    if (error.response?.status === 401) {
      console.warn('Token tidak valid atau expired')
    }
    return Promise.reject(error)
  }
)

export default apiClient