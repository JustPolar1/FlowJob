async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let message = 'No se pudieron cargar los integrantes.';
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

export function getMembers({ signal } = {}) {
  return requestJson('/api/members', { signal });
}
