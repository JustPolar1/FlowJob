export async function getTasks({ signal } = {}) {
  const response = await fetch('/api/tasks', { signal });

  if (!response.ok) {
    let message = 'No se pudieron cargar las tareas.';
    try {
      const body = await response.json();
      if (typeof body.detail === 'string') message = body.detail;
    } catch {
      // Keep the default message when the response has no JSON body.
    }
    throw new Error(message);
  }

  return response.json();
}
