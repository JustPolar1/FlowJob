import { Link } from 'react-router-dom';
import PageHeader from '../../../components/PageHeader.jsx';

export default function DashboardPage() {
  return (
    <section className="page-container">
      <PageHeader
        eyebrow="Tu espacio de trabajo"
        title="Resumen"
        description="Un lugar para organizar el trabajo y mantener al equipo en sintonía."
      />
      <div className="welcome-panel">
        <div className="welcome-copy">
          <span className="welcome-kicker">Bienvenido a FlowJob</span>
          <h2>El siguiente paso empieza aquí.</h2>
          <p>Consulta tus tareas y mantén visible el progreso del equipo desde un solo lugar.</p>
          <Link className="primary-link" to="/tareas">Ir a tareas <span aria-hidden="true">→</span></Link>
        </div>
        <div className="welcome-art" aria-hidden="true">
          <span className="art-card art-card-back">✓</span>
          <span className="art-card art-card-front"><i /><i /><i /></span>
          <span className="art-spark">✦</span>
        </div>
      </div>
      <div className="section-heading">
        <div>
          <h2>Tu espacio</h2>
          <p>Accesos rápidos a las áreas de FlowJob.</p>
        </div>
      </div>
      <div className="quick-links">
        <Link className="quick-link" to="/tareas">
          <span className="quick-icon tasks-icon" aria-hidden="true">☷</span>
          <span><strong>Administrar tareas</strong><small>Consulta y organiza el trabajo</small></span>
          <span className="quick-arrow" aria-hidden="true">↗</span>
        </Link>
        <Link className="quick-link" to="/equipo">
          <span className="quick-icon team-icon" aria-hidden="true">♧</span>
          <span><strong>Ver equipo</strong><small>Conoce a las personas del proyecto</small></span>
          <span className="quick-arrow" aria-hidden="true">↗</span>
        </Link>
      </div>
    </section>
  );
}
