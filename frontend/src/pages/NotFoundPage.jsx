import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <main className="not-found">
      <span className="not-found-code">404</span>
      <h1>No encontramos esa página</h1>
      <p>Puede que el enlace haya cambiado o que la dirección esté incompleta.</p>
      <Link className="primary-link" to="/tareas">Volver a tareas</Link>
    </main>
  );
}
