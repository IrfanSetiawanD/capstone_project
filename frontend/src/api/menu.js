// src/api/menu.js
import apiClient from './client'

export const menuAPI = {
  getAll: () => {
    return apiClient.get('/menus/', { 
      headers: { Authorization: undefined }   // ← Bypass token sementara
    })
  },

  create: (formData) => {
    return apiClient.post('/menus/', formData, {
      headers: { 
        'Content-Type': 'multipart/form-data',
        Authorization: undefined   // ← Bypass token
      }
    })
  },

  update: (id, formData) => {
    return apiClient.put(`/menus/${id}/`, formData, {
      headers: { 
        'Content-Type': 'multipart/form-data',
        Authorization: undefined 
      }
    })
  },

  delete: (id) => {
    return apiClient.delete(`/menus/${id}/`, {
      headers: { Authorization: undefined }
    })
  }
}