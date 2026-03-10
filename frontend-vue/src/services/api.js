import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// API endpoints
export const dashboardAPI = {
  // Get all dashboard data
  getAllData() {
    return api.get('/v1/dashboard/')
  },

  // Get data for specific category
  getCategoryData(category) {
    return api.get(`/v1/dashboard/${category}/`)
  }
}

export default api