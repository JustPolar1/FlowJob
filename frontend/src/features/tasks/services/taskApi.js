async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let message = 'No se pudo completar la solicitud.';
    try {
      const body = await response.json();
      if (typeof body.detail === 'string') message = body.detail;
    } catch {
      // Keep the default message when the response has no JSON body.
    }
    throw new Error(message);
  }

  return response.status === 204 ? null : response.json();
}

export function getTasks({ signal, status, assigneeId } = {}) {
  const params = new URLSearchParams();
  if (status) params.set('status', status);
  if (assigneeId) params.set('assignee_id', assigneeId);
  const queryString = params.toString();
  const query = queryString ? `?${queryString}` : '';
  return requestJson(`/api/tasks${query}`, { signal });
}

export function getMembers({ signal } = {}) {
  return requestJson('/api/members', { signal });
}

export function createTask(task) {
  return requestJson('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
}

export function updateTask(taskId, task) {
  return requestJson(`/api/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
}
