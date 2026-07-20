import { createContext, useContext, useEffect, useState } from 'react'
import api, { setTokens, getAccessToken } from '../api/client.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    (async () => {
      if (!getAccessToken()) { setLoading(false); return }
      try {
        const r = await api.get('/auth/me')
        setUser(r.data)
      } catch { setUser(null) }
      setLoading(false)
    })()
  }, [])

  const login = async (email, password) => {
    const r = await api.post('/auth/login', { email, password })
    setTokens(r.data.access_token, r.data.refresh_token)
    setUser(r.data.user)
    return r.data.user
  }

  const logout = async () => {
    try { await api.post('/auth/logout') } catch { /* ignore */ }
    setTokens(null, null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() { return useContext(AuthContext) }
