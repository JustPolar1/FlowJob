import PageHeader from '../../../components/PageHeader.jsx';

export default function TeamPage() {
  return (
    <section className="page-container">
      <PageHeader
        eyebrow="Personas"
        title="Equipo"
        description="Consulta quién forma parte del espacio de trabajo."
      />
      <div className="empty-state compact-empty-state">
        <span className="empty-icon" aria-hidden="true">♧</span>
        <h2>Integrantes del equipo</h2>
        <p>La lista aparecerá aquí cuando conectemos el servicio de integrantes.</p>
      </div>
    </section>
  );
}
