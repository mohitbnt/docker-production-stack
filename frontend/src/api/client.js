import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({ baseURL, timeout: 15000 })

let accessToken = localStorage.getItem('access_token') || null
let refreshToken = localStorage.getItem('refresh_token') || null

export function setTokens(access, refresh) {
  accessToken = access
  refreshToken = refresh
  if (access) localStorage.setItem('access_token', access)
  else localStorage.removeItem('access_token')
  if (refresh) localStorage.setItem('refresh_token', refresh)
  else localStorage.removeItem('refresh_token')
}

export function getAccessToken() { return accessToken }
export function getRefreshToken() { return refreshToken }

api.interceptors.request.use((cfg) => {
  if (accessToken && !cfg.headers.Authorization) {
    cfg.headers.Authorization = `Bearer ${accessToken}`
  }
  return cfg
})

let refreshing = null

async function performRefresh() {
  if (!refreshToken) throw new Error('no refresh token')
  const res = await axios.post(`${baseURL}/auth/refresh`, {}, {
    headers: { Authorization: `Bearer ${refreshToken}` },
  })
  setTokens(res.data.access_token, refreshToken)
  return res.data.access_token
}

api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const original = err.config || {}
    const status = err.response?.status
    if (status === 401 && !original._retry && refreshToken && !original.url.endsWith('/auth/refresh')) {
      original._retry = true
      try {
        refreshing = refreshing || performRefresh()
        const newAccess = await refreshing
        refreshing = null
        original.headers.Authorization = `Bearer ${newAccess}`
        return api(original)
      } catch (e) {
        refreshing = null
        setTokens(null, null)
      }
    }
    return Promise.reject(err)
  }
)

export default api
