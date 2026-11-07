const API_URL = import.meta.env.VITE_API_URL;

export async function getProjects() {
  const response = await fetch(`${API_URL}/api/projects/`);

  if (!response.ok) {
    throw new Error(`Failed to fetch projects: ${response.status}`);
  }

  return response.json();
}
