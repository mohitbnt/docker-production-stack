import { useEffect, useState } from 'react'
import api from '../api/client.js'

const empty = { name: '', code: '', description: '' }

export default function Departments() {
  const [rows, setRows] = useState([])
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(empty)
  const [err, setErr] = useState('')

  const load = async () => { const r = await api.get('/departments'); setRows(r.data) }
  useEffect(() => { load().catch(() => {}) }, [])

  const openCreate = () => { setEditing(null); setForm(empty); setErr(''); setOpen(true) }
  const openEdit = (r) => { setEditing(r.id); setForm({ name: r.name, code: r.code, description: r.description || '' }); setErr(''); setOpen(true) }

  const save = async (e) => {
    e.preventDefault(); setErr('')
    try {
      if (editing) await api.put(`/departments/${editing}`, form)
      else await api.post('/departments', form)
      setOpen(false); await load()
    } catch (e) { setErr(e.response?.data?.error || 'Save failed') }
  }

  const remove = async (id) => {
    if (!confirm('Delete this department?')) return
    try { await api.delete(`/departments/${id}`); await load() }
    catch (e) { alert(e.response?.data?.error || 'Delete failed') }
  }

  return (
    <div className="stack">
      <div className="row">
        <h1 style={{ margin: 0 }}>Departments</h1>
        <div className="spacer" />
        <button className="primary" onClick={openCreate}>+ New department</button>
      </div>

      <table className="table">
        <thead><tr><th>Code</th><th>Name</th><th>Description</th><th>Employees</th><th style={{ width: 160 }}></th></tr></thead>
        <tbody>
          {rows.length === 0 && <tr><td colSpan={5} className="muted" style={{ textAlign: 'center', padding: 20 }}>No departments.</td></tr>}
          {rows.map((r) => (
            <tr key={r.id}>
              <td><span className="badge">{r.code}</span></td>
              <td>{r.name}</td>
              <td>{r.description || '—'}</td>
              <td>{r.employee_count ?? 0}</td>
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
            <h2>{editing ? 'Edit department' : 'New department'}</h2>
            <div><label>Code</label><input required value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} /></div>
            <div><label>Name</label><input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
            <div><label>Description</label><textarea rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
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
