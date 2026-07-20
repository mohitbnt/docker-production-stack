import { useEffect, useState } from 'react'
import api from '../api/client.js'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [err, setErr] = useState('')

  useEffect(() => {
    api.get('/dashboard/stats')
      .then((r) => setStats(r.data))
      .catch((e) => setErr(e.response?.data?.error || 'Failed to load stats'))
  }, [])

  return (
    <div className="stack">
      <h1 style={{ margin: 0 }}>Dashboard</h1>
      {err && <div className="error">{err}</div>}
      {!stats && !err && <div className="muted">Loading…</div>}
      {stats && (
        <div className="stats-grid">
          <div className="card stat">
            <div className="label">Total Employees</div>
            <div className="value">{stats.total_employees}</div>
          </div>
          <div className="card stat">
            <div className="label">Total Departments</div>
            <div className="value">{stats.total_departments}</div>
          </div>
          <div className="card stat">
            <div className="label">Total Assets</div>
            <div className="value">{stats.total_assets}</div>
          </div>
          <div className="card stat">
            <div className="label">Cache</div>
            <div className="value" style={{ fontSize: 18 }}>
              {stats.cached ? <span className="badge success">HIT</span> : <span className="badge warning">MISS</span>}
            </div>
            <div className="muted" style={{ marginTop: 6, fontSize: 12 }}>
              generated_at: {stats.generated_at}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
