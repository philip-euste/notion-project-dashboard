
const API_URL = import.meta.env.VITE_API_URL;

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(
      error?.detail || `Request failed: ${response.status}`
    );
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function getProjects() {
  const response = await fetch(`${API_URL}/api/projects/`);
  return handleResponse(response);
}

export async function createProject(project) {
  const response = await fetch(`${API_URL}/api/projects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(project),
  });

  return handleResponse(response);
}

export async function updateProject(id, updates) {
  const response = await fetch(`${API_URL}/api/projects/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  });

  return handleResponse(response);
}

export async function deleteProject(id) {
  const response = await fetch(`${API_URL}/api/projects/${id}`, {
    method: "DELETE",
  });

  return handleResponse(response);
}
