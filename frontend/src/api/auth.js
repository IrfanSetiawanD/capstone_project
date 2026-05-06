// src/api/auth.js
import api from './client'

// Login
export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials, {
      headers: { Authorization: undefined }   // penting untuk login
    })
    return response
  }
}

// Create User (untuk Owner)
export const userAPI = {
  createUser: (data) => {
    return api.post('/api/users/create/', data)
  }
}