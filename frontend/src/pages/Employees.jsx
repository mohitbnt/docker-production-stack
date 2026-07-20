import { useEffect, useState } from 'react'
import api from '../api/client.js'

const empty = { first_name: '', last_name: '', email: '', phone: '', position: '', department_id: '' }

export default function Employees() {
  const [rows, setRows] = useState([])
  const [departments, setDepartments] = useState([])
  const [q, setQ] = useState('')
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(empty)
  const [err, setErr] = useState('')

  const load = async () => {
    const [emp, dep] = await Promise.all([
      api.get('/employees', { params: q ? { q } : {} }),
      api.get('/departments'),
    ])
    setRows(emp.data); setDepartments(dep.data)
  }
  useEffect(() => { load().catch(() => {}) }, [q])

  const openCreate = () => { setEditing(null); setForm(empty); setErr(''); setOpen(true) }
  const openEdit = (r) => {
    setEditing(r.id)
    setForm({
      first_name: r.first_name, last_name: r.last_name, email: r.email,
      phone: r.phone || '', position: r.position || '',
      department_id: r.department_id || '',
    })
    setErr(''); setOpen(true)
  }

  const save = async (e) => {
    e.preventDefault(); setErr('')
    const payload = { ...form, department_id: form.department_id ? Number(form.department_id) : null }
    try {
      if (editing) await api.put(`/employees/${editing}`, payload)
      else await api.post('/employees', payload)
      setOpen(false); await load()
    } catch (e) { setErr(e.response?.data?.error || 'Save failed') }
  }

  const remove = async (id) => {
    if (!confirm('Delete this employee?')) return
    await api.delete(`/employees/${id}`)
    await load()
  }

  return (
    <div className="stack">
      <div className="row">
        <h1 style={{ margin: 0 }}>Employees</h1>
        <div className="spacer" />
        <button className="primary" onClick={openCreate}>+ New employee</button>
      </div>

      <div className="toolbar">
        <input placeholder="Search by name, email or position…" value={q} onChange={(e) => setQ(e.target.value)} />
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>Name</th><th>Email</th><th>Position</th><th>Department</th><th>Phone</th><th style={{ width: 160 }}></th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && <tr><td colSpan={6} className="muted" style={{ textAlign: 'center', padding: 20 }}>No employees found.</td></tr>}
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.first_name} {r.last_name}</td>
              <td>{r.email}</td>
              <td>{r.position || '—'}</td>
              <td>{r.department?.name || '—'}</td>
              <td>{r.phone || '—'}</td>
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
            <h2>{editing ? 'Edit employee' : 'New employee'}</h2>
            <div className="row" style={{ gap: 12 }}>
              <div style={{ flex: 1 }}>
                <label>First name</label>
                <input required value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} />
              </div>
              <div style={{ flex: 1 }}>
                <label>Last name</label>
                <input required value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
              </div>
            </div>
            <div>
              <label>Email</label>
              <input type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </div>
            <div className="row" style={{ gap: 12 }}>
              <div style={{ flex: 1 }}>
                <label>Phone</label>
                <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
              </div>
              <div style={{ flex: 1 }}>
                <label>Position</label>
                <input value={form.position} onChange={(e) => setForm({ ...form, position: e.target.value })} />
              </div>
            </div>
            <div>
              <label>Department</label>
              <select value={form.department_id} onChange={(e) => setForm({ ...form, department_id: e.target.value })}>
                <option value="">— None —</option>
                {departments.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
              </select>
            </div>
            {err && <div className="error">{err}</div>}
            <div className="row">
              <div className="spacer" />
              <button type="button" onClick={() => setOpen(false)}>Cancel</button>
              <button className="primary" type="submit">{editing ? 'Save' : 'Create'}</button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
