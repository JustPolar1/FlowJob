import { useCallback, useEffect, useState } from 'react';
import PageHeader from '../../../components/PageHeader.jsx';
import { getTasks } from '../services/taskApi.js';

function statusClass(status) {
  if (status === 'Terminada') return 'task-status-completed';
  if (status === 'En proceso') return 'task-status-progress';
  return 'task-status-pending';
}

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reloadKey, setReloadKey] = useState(0);

  const loadTasks = useCallback(async (signal) => {
    setLoading(true);
    setError('');
    try {
      setTasks(await getTasks({ signal }));
    } catch (loadError) {
      if (loadError.name !== 'AbortError') setError(loadError.message);
    } finally {
      if (!signal.aborted) setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    loadTasks(controller.signal);
    return () => controller.abort();
  }, [loadTasks, reloadKey]);

  return (
    <section className="page-container">
      <PageHeader
        eyebrow="Espacio de trabajo"
        title="Tareas"
        description="Organiza el trabajo y sigue el progreso del equipo."
      />
      {loading && <p className="tasks-feedback" role="status">Cargando tareas…</p>}

      {!loading && error && (
        <div className="tasks-feedback tasks-error" role="alert">
          <p>{error}</p>
          <button className="secondary-button" onClick={() => setReloadKey((key) => key + 1)}>
            Reintentar
          </button>
        </div>
      )}

      {!loading && !error && tasks.length === 0 && (
        <div className="empty-state">
          <span className="empty-icon" aria-hidden="true">☷</span>
          <h2>Aún no hay tareas</h2>
          <p>Cuando el equipo registre tareas, aparecerán aquí.</p>
        </div>
      )}

      {!loading && !error && tasks.length > 0 && (
        <div className="task-list" aria-label="Lista de tareas">
          {tasks.map((task) => (
            <article className="task-card" key={task.id}>
              <div className="task-card-heading">
                <div className="task-title-group">
                  <span className="task-id">Tarea #{task.id}</span>
                  <h2>{task.title}</h2>
                </div>
                <span className={`task-badge ${statusClass(task.status)}`}>{task.status}</span>
              </div>
              {task.description && <p className="task-description">{task.description}</p>}
              <div className="task-card-footer">
                <span className="task-priority"><span aria-hidden="true">◆</span> Prioridad {task.priority}</span>
                <span className="task-assignee">
                  {task.assignee_id == null ? 'Sin asignar' : `Integrante #${task.assignee_id}`}
                </span>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
