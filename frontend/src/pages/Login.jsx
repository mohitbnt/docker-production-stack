import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setErr(''); setBusy(true)
    try {
      await login(email, password)
      const dest = location.state?.from?.pathname || '/dashboard'
      navigate(dest, { replace: true })
    } catch (e) {
      setErr(e.response?.data?.error || 'Login failed')
    } finally { setBusy(false) }
  }

  return (
    <div className="login-shell">
      <form className="card login-card stack" onSubmit={submit}>
        <h1>OpsPortal · Sign in</h1>
        <div>
          <label>Email</label>
          <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} autoFocus />
        </div>
        <div>
          <label>Password</label>
          <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        {err && <div className="error">{err}</div>}
        <button className="primary" disabled={busy} type="submit">{busy ? 'Signing in…' : 'Sign in'}</button>
        <div className="muted" style={{ fontSize: 12 }}>Internal use only · Contact IT for access.</div>
      </form>
    </div>
  )
}
