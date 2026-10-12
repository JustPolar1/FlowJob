import { useEffect, useState } from 'react';
import PageHeader from '../../../components/PageHeader.jsx';
import { getMembers } from '../services/memberApi.js';

function initials(name) {
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0])
    .join('')
    .toUpperCase();
}

export default function TeamPage() {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError('');
    getMembers({ signal: controller.signal })
      .then(setMembers)
      .catch((loadError) => {
        if (loadError.name !== 'AbortError') setError(loadError.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [reloadKey]);

  return (
    <section className="page-container">
      <PageHeader
        eyebrow="Personas"
        title="Equipo"
        description="Consulta quién forma parte del espacio de trabajo."
      />
      {loading && <p className="tasks-feedback" role="status">Cargando integrantes…</p>}

      {!loading && error && (
        <div className="tasks-feedback tasks-error" role="alert">
          <p>{error}</p>
          <button className="secondary-button" onClick={() => setReloadKey((key) => key + 1)}>
            Reintentar
          </button>
        </div>
      )}

      {!loading && !error && members.length === 0 && (
        <div className="empty-state compact-empty-state">
          <span className="empty-icon" aria-hidden="true">♧</span>
          <h2>Aún no hay integrantes</h2>
          <p>Los integrantes registrados en el servicio aparecerán aquí y podrán asignarse a las tareas.</p>
        </div>
      )}

      {!loading && !error && members.length > 0 && (
        <div className="member-grid" aria-label="Integrantes disponibles">
          {members.map((member) => (
            <article className="member-card" key={member.id}>
              <span className="avatar member-avatar" aria-hidden="true">{initials(member.name)}</span>
              <div className="member-card-copy">
                <span className="member-id">Integrante #{member.id}</span>
                <h2>{member.name}</h2>
                <span className="member-availability"><i aria-hidden="true" /> Disponible para asignación</span>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
