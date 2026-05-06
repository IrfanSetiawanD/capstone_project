// src/api/index.js
import api from './client'


// Import semua API modules
export { authAPI } from './auth'
export { menuAPI } from './menu'
export { orderAPI } from './order'
export { statsAPI } from './stats'
export { userAPI } from './auth'

// Export default axios instance
export default api