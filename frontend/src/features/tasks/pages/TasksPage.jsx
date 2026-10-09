import PageHeader from '../../../components/PageHeader.jsx';

export default function TasksPage() {
  return (
    <section className="page-container">
      <PageHeader
        eyebrow="Espacio de trabajo"
        title="Tareas"
        description="Organiza el trabajo y sigue el progreso del equipo."
      />
      <div className="empty-state">
        <span className="empty-icon" aria-hidden="true">☷</span>
        <h2>Tu tablero está listo</h2>
        <p>Cuando conectemos el servicio de tareas, aquí podrás consultarlas y administrarlas.</p>
        <span className="coming-soon">La gestión de tareas se implementará en el siguiente paso</span>
      </div>
    </section>
  );
}
