import { useState } from 'react'
import api from '../api/client.js'
import { useAuth } from '../contexts/AuthContext.jsx'

export default function Profile() {
  const { user, setUser } = useAuth()
  const [name, setName] = useState(user?.name || '')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState(''); const [err, setErr] = useState('')

  const save = async (e) => {
    e.preventDefault(); setMsg(''); setErr('')
    try {
      const payload = { name }
      if (password) payload.password = password
      const r = await api.put('/profile', payload)
      setUser(r.data); setPassword(''); setMsg('Profile updated.')
    } catch (e) { setErr(e.response?.data?.error || 'Update failed') }
  }

  return (
    <div className="stack" style={{ maxWidth: 520 }}>
      <h1 style={{ margin: 0 }}>Profile</h1>
      <div className="card stack">
        <div><label>Email</label><input value={user?.email || ''} disabled /></div>
        <div><label>Role</label><input value={user?.role || ''} disabled /></div>
        <form className="stack" onSubmit={save}>
          <div><label>Display name</label><input value={name} onChange={(e) => setName(e.target.value)} /></div>
          <div>
            <label>New password (leave empty to keep current)</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} />
          </div>
          {msg && <div style={{ color: 'var(--success)', fontSize: 13 }}>{msg}</div>}
          {err && <div className="error">{err}</div>}
          <div className="row"><div className="spacer" /><button className="primary" type="submit">Save</button></div>
        </form>
      </div>
    </div>
  )
}
