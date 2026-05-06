// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAdmin = computed(() => user.value?.role === 'admin')
  const isOwner = computed(() => user.value?.role === 'owner')
  const isLoggedIn = computed(() => !!user.value)

  // ==================== LOGIN ====================
  const login = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.login(credentials)
      
      const { token, user: userData } = response.data

      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(userData))
      user.value = userData

      console.log('✅ Login berhasil:', userData)
      return userData
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login gagal'
      console.error('❌ Login error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // ==================== CHECK AUTH ====================
  const checkAuth = () => {
    const token = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (token && savedUser) {
      try {
        user.value = JSON.parse(savedUser)
        console.log('✅ User restored from localStorage:', user.value)
      } catch (e) {
        console.error('Failed to parse saved user')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }

  // Jalankan checkAuth saat store dibuat
  checkAuth()

  return {
    user,
    loading,
    error,
    isAdmin,
    isOwner,
    isLoggedIn,
    login,
    logout,
    checkAuth
  }
})