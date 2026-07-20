import { useEffect, useState } from 'react'
import api from '../api/client.js'

const empty = { tag: '', name: '', category: '', status: 'available', assigned_to_id: '', purchased_at: '' }

const STATUS = ['available', 'assigned', 'in_repair', 'retired']

export default function Assets() {
  const [rows, setRows] = useState([])
  const [employees, setEmployees] = useState([])
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(empty)
  const [err, setErr] = useState('')

  const load = async () => {
    const [a, e] = await Promise.all([api.get('/assets'), api.get('/employees')])
    setRows(a.data); setEmployees(e.data)
  }
  useEffect(() => { load().catch(() => {}) }, [])

  const openCreate = () => { setEditing(null); setForm(empty); setErr(''); setOpen(true) }
  const openEdit = (r) => {
    setEditing(r.id)
    setForm({
      tag: r.tag, name: r.name, category: r.category || '',
      status: r.status, assigned_to_id: r.assigned_to_id || '',
      purchased_at: r.purchased_at ? r.purchased_at.slice(0, 10) : '',
    })
    setErr(''); setOpen(true)
  }

  const save = async (e) => {
    e.preventDefault(); setErr('')
    const payload = {
      ...form,
      assigned_to_id: form.assigned_to_id ? Number(form.assigned_to_id) : null,
      purchased_at: form.purchased_at || null,
    }
    try {
      if (editing) await api.put(`/assets/${editing}`, payload)
      else await api.post('/assets', payload)
      setOpen(false); await load()
    } catch (e) { setErr(e.response?.data?.error || 'Save failed') }
  }

  const remove = async (id) => {
    if (!confirm('Delete this asset?')) return
    await api.delete(`/assets/${id}`); await load()
  }

  const statusBadge = (s) => {
    const cls = s === 'available' ? 'success' : s === 'assigned' ? '' : s === 'in_repair' ? 'warning' : 'danger'
    return <span className={`badge ${cls}`}>{s}</span>
  }

  return (
    <div className="stack">
      <div className="row">
        <h1 style={{ margin: 0 }}>Assets</h1>
        <div className="spacer" />
        <button className="primary" onClick={openCreate}>+ New asset</button>
      </div>
      <table className="table">
        <thead><tr><th>Tag</th><th>Name</th><th>Category</th><th>Status</th><th>Assigned to</th><th>Purchased</th><th style={{ width: 160 }}></th></tr></thead>
        <tbody>
          {rows.length === 0 && <tr><td colSpan={7} className="muted" style={{ textAlign: 'center', padding: 20 }}>No assets.</td></tr>}
          {rows.map((r) => (
            <tr key={r.id}>
              <td><span className="badge">{r.tag}</span></td>
              <td>{r.name}</td>
              <td>{r.category || '—'}</td>
              <td>{statusBadge(r.status)}</td>
              <td>{r.assigned_to ? `${r.assigned_to.first_name} ${r.assigned_to.last_name}` : '—'}</td>
              <td>{r.purchased_at ? r.purchased_at.slice(0, 10) : '—'}</td>
              <td>
                <div className="row">
                  <button onClick={() => openEdit(r)}>Edit</button>
                  <button className="danger" onClick={() => remove(r.id)}>Delete</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {open && (
        <div className="modal-backdrop" onClick={() => setOpen(false)}>
          <form className="modal stack" onClick={(e) => e.stopPropagation()} onSubmit={save}>
            <h2>{editing ? 'Edit asset' : 'New asset'}</h2>
            <div className="row" style={{ gap: 12 }}>
              <div style={{ flex: 1 }}><label>Tag</label><input required value={form.tag} onChange={(e) => setForm({ ...form, tag: e.target.value })} /></div>
              <div style={{ flex: 2 }}><label>Name</label><input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
            </div>
            <div className="row" style={{ gap: 12 }}>
              <div style={{ flex: 1 }}><label>Category</label><input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} /></div>
              <div style={{ flex: 1 }}>
                <label>Status</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                  {STATUS.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>
            <div>
              <label>Assigned to</label>
              <select value={form.assigned_to_id} onChange={(e) => setForm({ ...form, assigned_to_id: e.target.value })}>
                <option value="">— None —</option>
                {employees.map((e) => <option key={e.id} value={e.id}>{e.first_name} {e.last_name} ({e.email})</option>)}
              </select>
            </div>
            <div><label>Purchased at</label><input type="date" value={form.purchased_at} onChange={(e) => setForm({ ...form, purchased_at: e.target.value })} /></div>
            {err && <div className="error">{err}</div>}
            <div className="row"><div className="spacer" />
              <button type="button" onClick={() => setOpen(false)}>Cancel</button>
              <button className="primary" type="submit">{editing ? 'Save' : 'Create'}</button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
