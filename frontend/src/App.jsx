
import { useEffect, useState } from "react";
import { getProjects } from "./services/api";
import "./App.css";

function App() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects();
        setProjects(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);

  if (loading) {
    return <main className="container">Loading projects...</main>;
  }

  if (error) {
    return (
      <main className="container">
        <h1>Notion Project Dashboard</h1>
        <p className="error">Failed to load projects: {error}</p>
      </main>
    );
  }

  return (
    <main className="container">
      <header className="header">
        <div>
          <h1>Notion Project Dashboard</h1>
          <p>Manage and track your projects.</p>
        </div>

        <span className="project-count">
          {projects.length} Projects
        </span>
      </header>

      <section className="project-list">
        {projects.length === 0 ? (
          <p>No projects found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Potential</th>
                <th>IDE</th>
                <th>Skills</th>
              </tr>
            </thead>

            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td className="project-name">
                    {project.name || "Untitled project"}
                  </td>
                  <td>{project.status || "—"}</td>
                  <td>{project.priority || "—"}</td>
                  <td>{project.potential || "—"}</td>
                  <td>{project.ide?.join(", ") || "—"}</td>
                  <td>{project.skills?.join(", ") || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}

export default App;
