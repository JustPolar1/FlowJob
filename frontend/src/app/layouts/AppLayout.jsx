import { Link, NavLink, Outlet } from 'react-router-dom';
import { navigationItems } from '../navigation.js';

export default function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" to="/tareas" aria-label="FlowJob, ir a tareas">
          <span className="brand-mark" aria-hidden="true">F</span>
          <span>flowjob</span>
        </Link>
        <p className="sidebar-label">Espacio de trabajo</p>
        <nav className="main-nav" aria-label="Navegación principal">
          {navigationItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `nav-link${isActive ? ' is-active' : ''}`}
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span className="avatar avatar-small" aria-hidden="true">F</span>
          <span className="profile-copy">
            <strong>FlowJob</strong>
            <span>Equipo de trabajo</span>
          </span>
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
