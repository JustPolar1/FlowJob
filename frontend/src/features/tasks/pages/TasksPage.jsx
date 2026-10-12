import { useCallback, useEffect, useState } from 'react';
import PageHeader from '../../../components/PageHeader.jsx';
import { createTask, getMembers, getTasks, updateTask } from '../services/taskApi.js';

const EMPTY_FORM = {
  title: '',
  description: '',
  assignee_id: '',
  status: 'Pendiente',
  priority: 'Media',
};

function statusClass(status) {
  if (status === 'Terminada') return 'task-status-completed';
  if (status === 'En proceso') return 'task-status-progress';
  return 'task-status-pending';
}

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [membersLoading, setMembersLoading] = useState(false);
  const [membersError, setMembersError] = useState('');
  const [error, setError] = useState('');
  const [reloadKey, setReloadKey] = useState(0);
  const [formOpen, setFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);
  const [statusFilter, setStatusFilter] = useState('');
  const [assigneeFilter, setAssigneeFilter] = useState('');

  const loadTasks = useCallback(async (signal) => {
    setLoading(true);
    setError('');
    try {
      setTasks(await getTasks({
        signal,
        status: statusFilter,
        assigneeId: assigneeFilter,
      }));
    } catch (loadError) {
      if (loadError.name !== 'AbortError') setError(loadError.message);
    } finally {
      if (!signal.aborted) setLoading(false);
    }
  }, [statusFilter, assigneeFilter]);

  useEffect(() => {
    const controller = new AbortController();
    loadTasks(controller.signal);
    return () => controller.abort();
  }, [loadTasks, reloadKey]);

  useEffect(() => {
    const controller = new AbortController();
    setMembersLoading(true);
    setMembersError('');
    getMembers({ signal: controller.signal })
      .then(setMembers)
      .catch((loadError) => {
        if (loadError.name !== 'AbortError') setMembersError(loadError.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setMembersLoading(false);
      });
    return () => controller.abort();
  }, []);

  function openCreateForm() {
    setEditingTask(null);
    setForm(EMPTY_FORM);
    setFormError('');
    setFormOpen(true);
  }

  function openEditForm(task) {
    setEditingTask(task);
    setForm({
      title: task.title,
      description: task.description ?? '',
      assignee_id: task.assignee_id == null ? '' : String(task.assignee_id),
      status: task.status,
      priority: task.priority,
    });
    setFormError('');
    setFormOpen(true);
  }

  function closeForm() {
    setFormOpen(false);
    setEditingTask(null);
    setFormError('');
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!form.title.trim()) {
      setFormError('El título es obligatorio.');
      return;
    }

    const payload = {
      title: form.title.trim(),
      description: form.description.trim() || null,
      assignee_id: form.assignee_id === '' ? null : Number(form.assignee_id),
      status: form.status,
      priority: form.priority,
    };

    setSaving(true);
    setFormError('');
    try {
      if (editingTask) await updateTask(editingTask.id, payload);
      else await createTask(payload);
      closeForm();
      setReloadKey((key) => key + 1);
    } catch (saveError) {
      setFormError(saveError.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="page-container">
      <div className="tasks-page-heading">
        <PageHeader
          eyebrow="Espacio de trabajo"
          title="Tareas"
          description="Organiza el trabajo y sigue el progreso del equipo."
        />
        <button className="primary-button" onClick={openCreateForm}>Nueva tarea <span aria-hidden="true">＋</span></button>
      </div>

      {formOpen && (
        <form className="task-form-card" onSubmit={handleSubmit}>
          <div className="task-form-heading">
            <div>
              <span className="task-id">{editingTask ? `Tarea #${editingTask.id}` : 'Nueva tarea'}</span>
              <h2>{editingTask ? 'Editar tarea' : 'Crear tarea'}</h2>
            </div>
            <button className="icon-button" type="button" aria-label="Cerrar formulario" onClick={closeForm}>×</button>
          </div>

          <div className="task-form-grid">
            <label className="task-field task-field-wide">
              <span>Título</span>
              <input
                autoFocus
                required
                maxLength={120}
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
                placeholder="¿Qué hay que hacer?"
              />
            </label>
            <label className="task-field task-field-wide">
              <span>Descripción <small>Opcional</small></span>
              <textarea
                rows="3"
                value={form.description}
                onChange={(event) => setForm({ ...form, description: event.target.value })}
                placeholder="Agrega detalles para el equipo"
              />
            </label>
            <label className="task-field">
              <span>Responsable</span>
              <select
                value={form.assignee_id}
                onChange={(event) => setForm({ ...form, assignee_id: event.target.value })}
                disabled={membersLoading}
              >
                <option value="">Sin asignar</option>
                {editingTask?.assignee_id != null && !members.some((member) => member.id === editingTask.assignee_id) && (
                  <option value={String(editingTask.assignee_id)}>Integrante #{editingTask.assignee_id} (no disponible)</option>
                )}
                {members.map((member) => (
                  <option key={member.id} value={String(member.id)}>{member.name}</option>
                ))}
              </select>
              {membersLoading && <small>Cargando integrantes…</small>}
              {membersError && <small className="field-note-error">No se pudieron cargar los integrantes. Puedes guardar la tarea sin asignar.</small>}
            </label>
            <label className="task-field">
              <span>Estado</span>
              <select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })}>
                <option>Pendiente</option>
                <option>En proceso</option>
                <option>Terminada</option>
              </select>
            </label>
            <label className="task-field">
              <span>Prioridad</span>
              <select value={form.priority} onChange={(event) => setForm({ ...form, priority: event.target.value })}>
                <option>Baja</option>
                <option>Media</option>
                <option>Alta</option>
              </select>
            </label>
          </div>

          {formError && <p className="form-error" role="alert">{formError}</p>}
          <div className="task-form-actions">
            <button className="secondary-button" type="button" onClick={closeForm} disabled={saving}>Cancelar</button>
            <button className="primary-button" type="submit" disabled={saving}>
              {saving ? 'Guardando…' : editingTask ? 'Guardar cambios' : 'Crear tarea'}
            </button>
          </div>
        </form>
      )}

      <div className="task-filters" aria-label="Filtros de tareas">
        <label className="task-filter-field">
          <span>Estado</span>
          <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
            <option value="">Todos los estados</option>
            <option>Pendiente</option>
            <option>En proceso</option>
            <option>Terminada</option>
          </select>
        </label>
        <label className="task-filter-field">
          <span>Responsable</span>
          <select
            value={assigneeFilter}
            onChange={(event) => setAssigneeFilter(event.target.value)}
            disabled={membersLoading || Boolean(membersError)}
          >
            <option value="">Todos los responsables</option>
            {members.map((member) => (
              <option key={member.id} value={String(member.id)}>{member.name}</option>
            ))}
          </select>
        </label>
        {(statusFilter || assigneeFilter) && (
          <button
            className="clear-filters-button"
            onClick={() => {
              setStatusFilter('');
              setAssigneeFilter('');
            }}
          >
            Limpiar filtros
          </button>
        )}
        {membersError && <span className="filter-note-error">No se pudieron cargar los responsables.</span>}
      </div>

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
          <h2>{statusFilter || assigneeFilter ? 'No hay tareas con estos filtros' : 'Aún no hay tareas'}</h2>
          <p>{statusFilter || assigneeFilter ? 'Prueba cambiando o limpiando los filtros.' : 'Crea una tarea para que el equipo pueda empezar a trabajar.'}</p>
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
                <div className="task-card-actions">
                  <span className={`task-badge ${statusClass(task.status)}`}>{task.status}</span>
                  <button className="secondary-button task-edit-button" onClick={() => openEditForm(task)}>Editar</button>
                </div>
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
