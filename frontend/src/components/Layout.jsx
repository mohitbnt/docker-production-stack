import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'

const nav = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/employees', label: 'Employees' },
  { to: '/departments', label: 'Departments' },
  { to: '/assets', label: 'Assets' },
  { to: '/profile', label: 'Profile' },
]

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">OpsPortal</div>
        {nav.map((n) => (
          <NavLink key={n.to} to={n.to} className={({ isActive }) => (isActive ? 'active' : '')}>
            {n.label}
          </NavLink>
        ))}
        <div className="sidebar-footer">v1.0.0 · Internal</div>
      </aside>
      <div>
        <div className="topbar">
          <div className="spacer" />
          <span className="muted">{user?.email}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
        <div className="main"><Outlet /></div>
      </div>
    </div>
  )
}
