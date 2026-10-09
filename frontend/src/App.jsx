import { Navigate, Route, Routes } from 'react-router-dom';
import AppLayout from './app/layouts/AppLayout.jsx';
import DashboardPage from './features/dashboard/pages/DashboardPage.jsx';
import TasksPage from './features/tasks/pages/TasksPage.jsx';
import TeamPage from './features/team/pages/TeamPage.jsx';
import NotFoundPage from './pages/NotFoundPage.jsx';

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Navigate to="/tareas" replace />} />
        <Route path="resumen" element={<DashboardPage />} />
        <Route path="tareas" element={<TasksPage />} />
        <Route path="equipo" element={<TeamPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
